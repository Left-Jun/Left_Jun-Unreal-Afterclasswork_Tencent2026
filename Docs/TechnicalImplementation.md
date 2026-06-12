# 技术实现说明

本文档用于记录 UE5 First Person Demo 的实现过程，后续会整理进最终提交 PDF。

## 1. 项目基础

- 项目基于 UE5 官方 First Person 模板创建。
- 当前实现方式以 Blueprint 为主，后续如有需要再添加 C++ 代码。
- 项目使用 GitHub 托管，并使用 Git LFS 管理 UE5 资源文件。

## 2. 玩家系统

计划在 First Person Character 基础上扩展：

- 玩家生命值 `Health` / `MaxHealth`
- 射击伤害逻辑
- 受击和死亡逻辑
- 多人版本中的 Server RPC 开火判定

## 3. 敌人系统

计划创建敌人角色 `BP_EnemyCharacter`：

- 敌人拥有生命值
- 敌人可受到玩家射击伤害
- 敌人死亡后销毁并触发计分
- 敌人 Actor 开启 Replication，保证多人中同步显示

## 4. 敌人 AI

计划创建 `BP_EnemyAIController`：

- 在服务器端寻找最近的玩家
- 使用 NavMesh 和 `AI Move To` 追击玩家
- 进入攻击距离后对玩家造成近战伤害

## 5. 得分与胜利

计划使用：

- `PlayerState` 保存玩家分数和击杀数
- `GameMode` 处理击杀计分和胜利判定
- `GameState` 同步目标分数、游戏结束状态和获胜者信息

基础规则：

- 击败一个敌人获得 10 分
- 玩家达到 100 分时触发胜利

## 6. 多人网络

多人实现原则：

- 伤害、击杀、刷怪、胜利判定由服务器负责
- 客户端输入通过 Server RPC 请求服务器执行
- 分数和游戏状态通过 `PlayerState` / `GameState` 同步
- 敌人和关键 Actor 开启 `Replicates` 与 `Replicate Movement`

## 7. 测试记录

后续记录：

- 单人战斗测试
- 敌人寻路测试
- 得分与胜利 UI 测试
- 双客户端 Listen Server 多人测试
