#!/usr/bin/env python3
"""Standalone Scan Context Lite node for ROS 2 LaserScan topics."""

from collections import deque
import math
from typing import Deque, List, Sequence, Tuple

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan

Descriptor = List[List[float]]
RingKey = List[float]


class ScanContextLiteNode(Node):
    def __init__(self) -> None:
        super().__init__("scan_context_lite")

        self.declare_parameter("scan_topic", "/scan")
        self.declare_parameter("ring_count", 20)
        self.declare_parameter("sector_count", 60)
        self.declare_parameter("history_size", 300)
        self.declare_parameter("min_valid_points", 30)
        self.declare_parameter("min_loop_gap", 20)
        self.declare_parameter("key_distance_threshold", 1.0)
        self.declare_parameter("desc_distance_threshold", 0.15)

        self.scan_topic = str(self.get_parameter("scan_topic").value)
        self.ring_count = max(1, int(self.get_parameter("ring_count").value))
        self.sector_count = max(1, int(self.get_parameter("sector_count").value))
        self.min_valid_points = max(
            0, int(self.get_parameter("min_valid_points").value)
        )
        self.min_loop_gap = max(0, int(self.get_parameter("min_loop_gap").value))
        self.key_distance_threshold = float(
            self.get_parameter("key_distance_threshold").value
        )
        self.desc_distance_threshold = float(
            self.get_parameter("desc_distance_threshold").value
        )
        history_size = max(1, int(self.get_parameter("history_size").value))

        self.frame_index = 0
        self.history: Deque[Tuple[int, Descriptor, RingKey]] = deque(
            maxlen=history_size
        )

        self.subscriber = self.create_subscription(
            LaserScan,
            self.scan_topic,
            self._on_scan,
            qos_profile_sensor_data,
        )

        self.get_logger().info(
            "scan_context_lite ready: topic=%s ring_count=%d sector_count=%d "
            "history_size=%d min_loop_gap=%d"
            % (
                self.scan_topic,
                self.ring_count,
                self.sector_count,
                history_size,
                self.min_loop_gap,
            )
        )

    def _on_scan(self, msg: LaserScan) -> None:
        self.frame_index += 1

        descriptor, valid_points = self._build_descriptor(msg)
        if valid_points < self.min_valid_points:
            self.get_logger().warn(
                "frame=%d skipped: valid_points=%d < min_valid_points=%d"
                % (self.frame_index, valid_points, self.min_valid_points)
            )
            return

        ring_key = self._build_ring_key(descriptor)
        match = self._find_best_match(descriptor, ring_key)

        if match is None:
            self.get_logger().info(
                "frame=%d db=%d valid_points=%d no loop candidate"
                % (self.frame_index, len(self.history), valid_points)
            )
        else:
            candidate_frame, key_distance, desc_distance, shift = match
            yaw_deg = 360.0 * shift / float(self.sector_count)
            if desc_distance <= self.desc_distance_threshold:
                self.get_logger().info(
                    "frame=%d match_frame=%d key_dist=%.3f desc_dist=%.3f "
                    "shift=%d yaw_offset_deg=%.1f loop_candidate=yes"
                    % (
                        self.frame_index,
                        candidate_frame,
                        key_distance,
                        desc_distance,
                        shift,
                        yaw_deg,
                    )
                )
            else:
                self.get_logger().info(
                    "frame=%d match_frame=%d key_dist=%.3f desc_dist=%.3f "
                    "shift=%d yaw_offset_deg=%.1f loop_candidate=no"
                    % (
                        self.frame_index,
                        candidate_frame,
                        key_distance,
                        desc_distance,
                        shift,
                        yaw_deg,
                    )
                )

        self.history.append((self.frame_index, descriptor, ring_key))

    def _build_descriptor(self, msg: LaserScan) -> Tuple[Descriptor, int]:
        descriptor: Descriptor = [
            [0.0 for _ in range(self.sector_count)]
            for _ in range(self.ring_count)
        ]
        valid_points = 0

        angle_span = msg.angle_max - msg.angle_min
        if angle_span <= 0.0:
            angle_span = math.tau
        sector_width = angle_span / float(self.sector_count)

        range_min = float(msg.range_min)
        range_max = float(msg.range_max)
        range_span = max(range_max - range_min, 1e-6)
        ring_width = range_span / float(self.ring_count)

        for index, distance in enumerate(msg.ranges):
            if not math.isfinite(distance):
                continue
            if distance < range_min or distance > range_max:
                continue

            angle = msg.angle_min + index * msg.angle_increment
            sector = int((angle - msg.angle_min) / sector_width)
            if sector < 0:
                continue
            if sector >= self.sector_count:
                sector = self.sector_count - 1

            ring = int((distance - range_min) / ring_width)
            if ring < 0:
                continue
            if ring >= self.ring_count:
                ring = self.ring_count - 1

            # Closer points get a higher score so occupied structure stands out.
            score = 1.0 - (distance - range_min) / range_span
            if score > descriptor[ring][sector]:
                descriptor[ring][sector] = score
            valid_points += 1

        return descriptor, valid_points

    def _build_ring_key(self, descriptor: Descriptor) -> RingKey:
        return [max(row) if row else 0.0 for row in descriptor]

    def _find_best_match(
        self,
        query_descriptor: Descriptor,
        query_key: RingKey,
    ) -> Tuple[int, float, float, int] | None:
        best_match: Tuple[int, float, float, int] | None = None

        for candidate_frame, candidate_descriptor, candidate_key in self.history:
            if self.frame_index - candidate_frame < self.min_loop_gap:
                continue

            key_distance = self._vector_distance(query_key, candidate_key)
            if key_distance > self.key_distance_threshold:
                continue

            desc_distance, shift = self._circular_descriptor_distance(
                query_descriptor,
                candidate_descriptor,
            )

            if best_match is None or desc_distance < best_match[2]:
                best_match = (
                    candidate_frame,
                    key_distance,
                    desc_distance,
                    shift,
                )

        return best_match

    def _circular_descriptor_distance(
        self,
        a: Descriptor,
        b: Descriptor,
    ) -> Tuple[float, int]:
        best_distance = float("inf")
        best_shift = 0

        for shift in range(self.sector_count):
            total = 0.0
            compared = 0

            for row_a, row_b in zip(a, b):
                if shift == 0:
                    shifted_row = row_b
                else:
                    shifted_row = row_b[-shift:] + row_b[:-shift]

                for value_a, value_b in zip(row_a, shifted_row):
                    if value_a == 0.0 and value_b == 0.0:
                        continue
                    total += abs(value_a - value_b)
                    compared += 1

            if compared == 0:
                continue

            distance = total / float(compared)
            if distance < best_distance:
                best_distance = distance
                best_shift = shift

        return best_distance, best_shift

    @staticmethod
    def _vector_distance(a: Sequence[float], b: Sequence[float]) -> float:
        total = 0.0
        for value_a, value_b in zip(a, b):
            delta = value_a - value_b
            total += delta * delta
        return math.sqrt(total)


def main() -> None:
    rclpy.init()
    node = ScanContextLiteNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
