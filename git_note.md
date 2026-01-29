🚀 Git 工作流程（四部曲）
1. 准备阶段 - 设置工作环境

# 检查 Git 是否安装成功
git --version

# 配置个人信息（只需设置一次）
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"

# 查看配置信息
git config --list

2. 初始化项目 - 创建本地仓库

# 创建新文件夹并进入
mkdir 项目名称
cd 项目名称

# 初始化 Git 仓库（创建 .git 隐藏文件夹）
git init

# 或者从远程仓库克隆（下载整个项目）
git clone 远程仓库地址  


📝 Git 核心操作（三步走）
第一步：添加文件到暂存区

# 添加单个文件（推荐新手使用）
git add 文件名

# 添加当前目录所有文件
git add .

# 添加所有修改过的文件
git add --all

第二步：保存修改（提交）

# 提交到本地仓库，并添加描述信息
git commit -m "描述这次修改的内容"

# 示例：提交并说明做了什么
git commit -m "修复了登录按钮的bug"
git commit -m "添加了用户注册功能"
git commit -m "更新了首页样式"

第三步：同步到远程仓库

# 第一次推送需要设置远程仓库
git remote add origin 远程仓库地址

# 推送代码到远程仓库（-u 是设置默认推送目标）
git push -u origin 分支名

# 后续推送（如果已设置默认目标）
git push


🌿 分支管理（多个版本同时开发）
分支基本操作

# 查看所有分支（* 表示当前所在分支）
git branch

# 创建新分支
git branch 新分支名

# 切换到指定分支
git checkout 分支名

# 创建并立即切换到新分支
git checkout -b 新分支名

# 重命名当前分支
git branch -m 新分支名

# 删除分支（-d 是安全删除，-D 是强制删除）
git branch -d 分支名


分支合并与同步
 
# 将其他分支的修改合并到当前分支
git merge 要合并的分支名

# 拉取远程仓库的最新代码
git pull

# 拉取指定分支的最新代码
git pull origin 分支名


🔍 查看与比较
查看当前状态
 
# 查看工作区状态（最常用）
git status

# 查看提交历史（按时间倒序）
git log

# 简洁版提交历史
git log --oneline

# 查看文件的具体修改内容
git diff
git diff 文件名


撤销与回退
 
# 撤销文件的修改（回到上次提交的状态）
git checkout -- 文件名

# 取消暂存的文件（从暂存区移除）
git reset 文件名

# 回退到指定版本
git reset --hard 版本号


🔄 远程仓库操作
连接远程仓库
 
# 查看已连接的远程仓库
git remote -v

# 添加新的远程仓库
git remote add origin 仓库地址

# 移除远程仓库连接
git remote remove origin

# 修改远程仓库地址
git remote set-url origin 新地址


推送与拉取

# 推送到远程仓库（更新云端代码）
git push

# 强制推送（谨慎使用，会覆盖远程代码）
git push -f

# 拉取最新代码（下载云端更新）
git pull

# 从远程仓库获取更新但不合并
git fetch


🎯 实际应用场景
场景1：从头开始一个新项目

# 1. 创建项目文件夹
mkdir my-project
cd my-project

# 2. 初始化仓库
git init

# 3. 创建并编辑文件（比如README.md）
echo "# 我的项目" >> README.md

# 4. 添加到暂存区
git add README.md

# 5. 提交到本地仓库
git commit -m "添加项目说明文档"

# 6. 连接到GitHub（或其他平台）
git remote add origin https://github.com/用户名/仓库名.git

# 7. 重命名主分支（如果需要）
git branch -M main

# 8. 推送到远程仓库
git push -u origin main


场景2：参与已有项目

# 1. 下载项目到本地
git clone https://github.com/用户名/项目名.git

# 2. 进入项目文件夹
cd 项目名

# 3. 创建自己的分支（避免影响主分支）
git checkout -b my-feature

# 4. 修改代码...
# 5. 查看修改了哪些文件
git status

# 6. 添加修改的文件
git add .

# 7. 提交修改
git commit -m "完成新功能开发"

# 8. 推送到自己的分支
git push origin my-feature


场景3：修复bug的流程

# 1. 切换到主分支
git checkout main

# 2. 更新到最新版本
git pull

# 3. 创建bug修复分支
git checkout -b fix-bug-001

# 4. 修复bug...
# 5. 提交修复
git add .
git commit -m "修复了登录页面显示问题"

# 6. 推送到远程
git push origin fix-bug-001


📌 实用技巧与小贴士
日常开发习惯
勤提交：每完成一个小功能就提交一次，不要积累太多修改

写好注释：提交信息要清晰明了，方便日后查看

先拉取再推送：在推送前先拉取最新代码，避免冲突

多用分支：新功能、修复bug都在独立分支上进行


常见问题解决

# 如果提交信息写错了
git commit --amend -m "新的提交信息"

# 忘记添加某个文件
git add 忘记的文件
git commit --amend  # 加入到上次提交

# 撤回最近一次提交（但保留修改）
git reset --soft HEAD~1

# 完全撤回最近一次提交（删除修改）
git reset --hard HEAD~1


查看帮助
bash
# 查看某个命令的帮助
git help 命令名
git 命令名 --help

# 示例
git help push
git commit --help


📊 Git 工作流程总结
text
工作目录（你的电脑）
     ↓  git add
暂存区（临时存放）
     ↓  git commit
本地仓库（.git文件夹）
     ↓  git push
远程仓库（GitHub/GitLab等）
     ↑  git pull
本地仓库


💡 记住这个万能公式
当你在一个项目中完成了一些修改：

# 1. 查看状态
git status

# 2. 添加修改
git add .

# 3. 提交修改
git commit -m "描述你的修改"

# 4. 推送到远程
git push