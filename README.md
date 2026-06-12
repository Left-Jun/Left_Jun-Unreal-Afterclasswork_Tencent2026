# Left_Jun-Unreal-Afterclasswork_Tencent2026

UE5 First Person 模板改造项目，用于“开局一课客户端大作业”。

## 项目信息

- 作者：左涵俊
- 项目名称：左涵俊_开局一课客户端大作业
- Unreal Engine 版本：5.7
- GitHub 仓库：https://github.com/Left-Jun/Left_Jun-Unreal-Afterclasswork_Tencent2026
- 作业提交形式：Demo 视频 + PDF 技术说明
- 截止时间：2026 年 6 月 21 日北京时间 23:59

## 作业目标

基于 UE5 官方 First Person 模板实现一个游戏 Demo，包含：

- 会移动并攻击玩家的敌人
- 玩家击败敌人的战斗逻辑
- 基础得分和游戏胜利机制
- 多人网络对战或联机演示

## 当前开发计划

1. 搭建项目仓库、Git LFS 和说明文档。
2. 实现单机战斗闭环：玩家射击、敌人受伤死亡、敌人追击和攻击玩家。
3. 增加刷怪器、分数统计、胜利条件和 UI。
4. 改造为多人网络版本：服务器伤害判定、分数同步、敌人复制、胜利状态同步。
5. 录制 Demo 视频并整理 PDF 技术说明。

## 运行方式

1. 使用 Unreal Engine 5.7 打开 `左涵俊_开局一课客户端大作业.uproject`。
2. 打开主地图后点击 Play 进行本地测试。
3. 多人测试时，在 Play 设置中将 `Number of Players` 设为 2，并使用 `Play As Listen Server`。

## 仓库说明

本仓库使用 Git LFS 管理 UE5 二进制资源，例如 `.uasset` 和 `.umap` 文件。首次克隆后建议执行：

```powershell
git lfs install
git lfs pull
```

本地生成目录如 `DerivedDataCache/`、`Intermediate/`、`Saved/` 不提交到仓库。
