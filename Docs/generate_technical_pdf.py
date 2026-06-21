from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "Docs"
IMG = DOCS / "images"
OUT = DOCS / "左涵俊-四川大学-开局一课客户端大作业.pdf"
FALLBACK_OUT = DOCS / "左涵俊-四川大学-开局一课客户端大作业-新版.pdf"


def register_fonts():
    for font in [
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path(r"C:\Windows\Fonts\simsun.ttc"),
    ]:
        if font.exists():
            pdfmetrics.registerFont(TTFont("CN", str(font)))
            pdfmetrics.registerFont(TTFont("CN-Bold", str(font)))
            return
    raise RuntimeError("No Chinese font found in C:\\Windows\\Fonts")


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="CN-Bold",
            fontSize=22,
            leading=30,
            alignment=TA_CENTER,
            spaceAfter=14,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            fontName="CN",
            fontSize=10.5,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#444444"),
            spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="CN-Bold",
            fontSize=15,
            leading=21,
            textColor=colors.HexColor("#1F4E79"),
            spaceBefore=12,
            spaceAfter=7,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="CN-Bold",
            fontSize=12.5,
            leading=18,
            textColor=colors.HexColor("#333333"),
            spaceBefore=8,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="CN",
            fontSize=9.5,
            leading=15,
            firstLineIndent=18,
            alignment=TA_LEFT,
            spaceAfter=5,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName="CN",
            fontSize=9.3,
            leading=14,
            leftIndent=14,
            firstLineIndent=-8,
            spaceAfter=3,
        ),
        "caption": ParagraphStyle(
            "caption",
            fontName="CN",
            fontSize=8.2,
            leading=11,
            textColor=colors.HexColor("#555555"),
            alignment=TA_CENTER,
            spaceBefore=3,
            spaceAfter=7,
        ),
        "table": ParagraphStyle(
            "table",
            fontName="CN",
            fontSize=8.4,
            leading=12,
        ),
    }


def p(text, style):
    return Paragraph(escape(text), style)


def bullet(text):
    return p("- " + text, ST["bullet"])


def figure(num, caption, max_width=16.2 * cm, max_height=8.8 * cm):
    path = IMG / f"figure_{num:02d}.png"
    if not path.exists():
        return []
    im = Image(str(path))
    ratio = min(max_width / im.imageWidth, max_height / im.imageHeight)
    im.drawWidth = im.imageWidth * ratio
    im.drawHeight = im.imageHeight * ratio
    return [KeepTogether([im, p(f"图 {num}: {caption}", ST["caption"])])]


def data_table(data, widths):
    tbl = Table(data, colWidths=widths, repeatRows=1)
    tbl.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "CN"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.2),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#999999")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return tbl


def add_figures(story, items):
    for num, caption in items:
        story.extend(figure(num, caption))


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("CN", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(2 * cm, 1.2 * cm, "左涵俊-四川大学-开局一课客户端大作业")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"第 {doc.page} 页")
    canvas.restoreState()


register_fonts()
ST = build_styles()
story = []

story.append(p("左涵俊-四川大学-开局一课客户端大作业技术说明", ST["title"]))
story.append(p("UE5 First Person 多人协作清理训练场 Demo", ST["subtitle"]))

story.append(p("1. 项目概述", ST["h1"]))
story.append(p("本项目基于 Unreal Engine 5.7 官方 First Person 模板开发，实现了一个可演示的多人协作清理训练场 Demo。玩家进入训练场后使用第一人称射线武器攻击敌人；敌人会在服务器端寻找最近的存活玩家，使用 NavMesh 追击并播放攻击动画；敌人被击败后增加队伍分数，达到目标数量后所有玩家看到胜利提示。", ST["body"]))
story.append(p("Demo 支持单人模式和本地 Listen Server 双人联机模式。多人测试时，一个客户端选择创建房间，另一个客户端选择加入游戏，人数达到 2 人后由 Lobby 自动切换到战斗关卡。", ST["body"]))

story.append(p("2. 作业要求对应关系", ST["h1"]))
requirements = [
    [p("作业要求", ST["table"]), p("实现内容", ST["table"])],
    [p("会移动和攻击玩家的敌人", ST["table"]), p("敌人服务器端索敌，使用 AI MoveTo 追击玩家，并在攻击范围内播放攻击动画和造成伤害。", ST["table"])],
    [p("玩家可以击败敌人", ST["table"]), p("玩家左键射击调用 ServerFire，服务器执行射线检测和 Apply Damage，敌人血量归零后销毁。", ST["table"])],
    [p("基础得分和胜利机制", ST["table"]), p("GameMode 修改 GameState 中的 TeamScore，达到 TargetScore 后设置 GameWon，HUD 显示胜利。", ST["table"])],
    [p("多人网络对战", ST["table"]), p("Listen Server 模式，伤害、AI、死亡、得分和胜利由服务器权威处理，并通过 Replication/RPC 同步。", ST["table"])],
]
story.append(data_table(requirements, [5.1 * cm, 11.1 * cm]))

story.append(p("3. GitHub 链接与多人网络实现要点", ST["h1"]))
story.append(p("GitHub 仓库：https://github.com/Left-Jun/Left_Jun-Unreal-Afterclasswork_Tencent2026", ST["body"]))
story.append(p("Demo 视频随提交文件一同上传，文件名为 左涵俊-四川大学-开局一课客户端大作业.mp4。", ST["body"]))
story.append(p("项目使用 Listen Server 模式进行多人演示。服务器负责敌人 AI、伤害、死亡、重生、得分和胜利判定；客户端负责本地输入、UI 显示和本地射击视觉反馈。", ST["body"]))
for item in [
    "玩家射击：客户端输入后调用 ServerFire，由服务器执行射线检测和伤害。",
    "射击反馈：客户端本地执行 LocalFireVisual 绘制射线，避免等待网络往返。",
    "敌人 AI：敌人在服务器 Authority 分支中定时索敌和移动，位置通过 Actor Replication 同步。",
    "敌人攻击动画：使用 Multicast RPC 播放攻击动画，保证所有窗口表现一致。",
    "玩家死亡 UI：服务器判定死亡后调用 ClientShowDeathMenu，只在死亡玩家自己的客户端显示死亡菜单。",
    "玩家重生：复活按钮调用 ServerRespawn，由服务器恢复玩家状态并传送到 PlayerStart。",
    "分数与胜利：保存在 GameState 中并复制给所有客户端。",
]:
    story.append(bullet(item))

story.append(PageBreak())
story.append(p("4. 玩家系统", ST["h1"]))
story.append(p("4.1 服务器权威射击", ST["h2"]))
story.append(p("玩家射击基于 First Person 模板扩展。按下鼠标左键后，客户端先执行 LocalFireVisual，在本地绘制射线反馈；随后调用 ServerFire RPC，由服务器根据玩家第一人称摄像机位置和朝向执行 Line Trace By Channel。命中目标后，服务器调用 Apply Damage，对敌人造成 25 点伤害。", ST["body"]))
story.append(p("这种设计将即时视觉反馈和权威伤害判定分离：客户端能立刻看到开火射线，真正的命中和伤害由服务器统一确认。", ST["body"]))
add_figures(story, [(19, "ServerFire 射线伤害"), (23, "LocalFireVisual 本地射击反馈")])
story.append(p("4.2 玩家受伤、死亡与重生", ST["h2"]))
story.append(p("玩家角色维护 Health、MaxHealth 和 IsDead 变量，其中 Health 与 IsDead 设置为 Replicated。敌人攻击玩家时由服务器调用 Apply Damage。玩家角色在 Event AnyDamage 中先判断 IsDead，避免死亡后重复扣血；若仍存活，则将血量 Clamp 到 0 - MaxHealth 范围内。", ST["body"]))
story.append(p("当 Health <= 0 时，服务器设置 IsDead = true，并调用 ClientShowDeathMenu。该事件设置为 Run on Owning Client，因此死亡菜单只会出现在死亡玩家自己的窗口中，而不会错误显示在服务器或其他客户端窗口。", ST["body"]))
add_figures(story, [(20, "玩家扣血与死亡判断"), (21, "客户端显示死亡菜单"), (22, "服务器重生逻辑")])
story.append(p("4.3 HUD 创建与输入恢复", ST["h2"]))
story.append(p("玩家 BeginPlay 中恢复输入模式、隐藏鼠标并创建 HUD。该步骤解决了从主菜单或死亡界面切换到战斗地图后输入模式仍停留在 UI 状态的问题。", ST["body"]))
add_figures(story, [(24, "玩家 BeginPlay 初始化"), (25, "玩家蓝图总览")])

story.append(PageBreak())
story.append(p("5. 敌人系统", ST["h1"]))
story.append(p("5.1 敌人受伤与死亡", ST["h2"]))
story.append(p("敌人蓝图 BP_EnemyCharacter 在 Event AnyDamage 中处理受伤逻辑。该逻辑通过 Switch Has Authority 保证只在服务器端扣减敌人生命值。敌人血量小于等于 0 后，调用 BP_DemoGameMode.EnemyKilled 增加队伍分数，然后销毁敌人 Actor。", ST["body"]))
story.append(p("该设计确保敌人死亡、得分和胜利判断都由服务器统一处理，避免多个客户端分别计算造成状态不一致。", ST["body"]))
add_figures(story, [(11, "敌人受伤与死亡")])
story.append(p("5.2 服务器端索敌与移动", ST["h2"]))
story.append(p("敌人 BeginPlay 中在 Authority 分支启动定时器，周期性调用 UpdateEnemy。UpdateEnemy 遍历所有 BP_FirstPersonCharacter，跳过 IsDead 为 true 的玩家，选择最近的存活玩家作为 TargetPlayer，并使用 AI MoveTo 追击。地图中放置 Nav Mesh Bounds Volume，使敌人能够基于 NavMesh 寻路。", ST["body"]))
add_figures(story, [(12, "敌人选择最近存活玩家"), (13, "敌人追击与攻击入口")])
story.append(p("5.3 攻击动画与延迟伤害", ST["h2"]))
story.append(p("敌人进入攻击范围后，使用 LastAttackTime 和 AttackCooldown 控制攻击频率。攻击触发时调用 Multicast_PlayAttack，让所有客户端都能看到攻击动画。动画播放后延迟约 0.35 秒，再检查目标有效且在攻击范围内，然后执行 Apply Damage。", ST["body"]))
add_figures(story, [(14, "敌人攻击延迟伤害"), (15, "敌人攻击动画 Multicast")])
story.append(p("5.4 敌人动画蓝图", ST["h2"]))
story.append(p("ABP_Enemy 使用 Try Get Pawn Owner、Get Velocity 和 Vector Length 计算敌人移动速度，并写入 Speed。AnimGraph 中使用 BS_Idle_Walk_Run 混合空间实现待机、行走、奔跑切换，攻击动画通过 DefaultSlot 叠加播放。", ST["body"]))
add_figures(story, [(16, "敌人蓝图总览"), (17, "敌人动画图表"), (18, "敌人动画 Speed 更新")])

story.append(PageBreak())
story.append(p("6. 联机、得分、胜利与大厅", ST["h1"]))
story.append(p("玩家启动程序后首先进入主菜单。单人游戏直接打开战斗关卡；多人游戏通过控制台命令 open /Game/Demo/Lvl_Lobby?listen 创建 Listen Server；加入游戏通过 open 127.0.0.1 连接本机服务器。", ST["body"]))
story.append(p("在 Lobby 中，BP_LobbyGameMode 通过 PostLogin 统计 GameState.PlayerArray 人数。当玩家数量达到 2 时，服务器执行 servertravel /Game/Demo/Lvl_FirstPerson，将所有客户端切换到战斗地图。", ST["body"]))
story.append(p("进入战斗地图后，玩家协作击败敌人。敌人追击最近的存活玩家，靠近后播放攻击动画并扣除玩家生命值。玩家死亡后会显示死亡菜单，可以点击复活按钮回到出生点。队伍击败 5 名敌人后，所有玩家 HUD 显示游戏胜利。", ST["body"]))
story.append(p("BP_DemoGameMode 中实现 EnemyKilled 函数。敌人死亡时，服务器调用该函数，获取 BP_DemoGameState 并将 TeamScore + 1。当 TeamScore >= TargetScore 时，服务器将 GameWon 设置为 true。GameState 中的 TeamScore、TargetScore 和 GameWon 设置为 Replicated，使所有客户端 HUD 都能同步显示击杀进度和胜利提示。", ST["body"]))
add_figures(story, [(8, "GameMode 击杀得分逻辑"), (9, "Lobby PostLogin 跳转逻辑")])

story.append(p("7. UI 系统", ST["h1"]))
story.append(p("7.1 主菜单", ST["h2"]))
story.append(p("WBP_MainMenu 是项目入口界面，包含标题、作者信息、单人游戏、多人游戏和加入游戏按钮。单人按钮使用 Open Level by Name 打开战斗关卡；多人按钮使用 Execute Console Command 创建 Listen Server Lobby；加入按钮连接本机地址。主菜单关卡的 Level Blueprint 在 BeginPlay 中创建该 Widget，并设置 UI Only 输入模式和鼠标显示。", ST["body"]))
add_figures(story, [(6, "主菜单界面"), (7, "主菜单按钮逻辑")])
story.append(p("7.2 战斗 HUD", ST["h2"]))
story.append(p("WBP_DemoHUD 显示本地玩家生命值、队伍击杀数量、胜利提示和准星。HUD 在玩家角色 BeginPlay 中通过 Is Locally Controlled 判断，仅为本地控制的玩家创建，避免服务器或远程角色重复生成 UI。", ST["body"]))
story.append(p("HUD 的 Tick 中使用 Get Owning Player Pawn 读取本地玩家的 Health，并从 BP_DemoGameState 中读取 TeamScore 和 GameWon。这样每个客户端显示的是自己的生命值，同时共享同一份服务器同步的得分与胜利状态。", ST["body"]))
add_figures(story, [(3, "HUD 设计"), (4, "HUD 生命值更新"), (5, "HUD 分数与胜利更新")])
story.append(p("7.3 死亡与复活菜单", ST["h2"]))
story.append(p("WBP_DeathMenu 在玩家死亡时显示，包含 You Died 提示和复活按钮。按钮点击后调用玩家角色的 ServerRespawn，由服务器恢复生命值、重置死亡状态并将玩家传送回出生点；随后本地 Widget 移除自身，并恢复 Game Only 输入模式。", ST["body"]))
add_figures(story, [(1, "死亡菜单设计"), (2, "复活按钮逻辑")])

story.append(PageBreak())
story.append(p("8. 主要资源与关卡", ST["h1"]))
for item in [
    "主菜单关卡：/Game/Demo/Lvl_MainMenu",
    "等待房间关卡：/Game/Demo/Lvl_Lobby",
    "战斗关卡：/Game/Demo/Lvl_FirstPerson",
    "玩家蓝图：/Game/FirstPerson/Blueprints/BP_FirstPersonCharacter",
    "敌人蓝图：/Game/Blueprints/ENEMY/BP_EnemyCharacter",
    "敌人动画蓝图：/Game/Blueprints/ENEMY/ABP_Enemy",
    "游戏规则：/Game/Blueprints/GAME/BP_DemoGameMode",
    "游戏状态：/Game/Blueprints/GAME/BP_DemoGameState",
    "大厅规则：/Game/Blueprints/GAME/BP_LobbyGameMode",
    "UI：WBP_MainMenu、WBP_DemoHUD、WBP_DeathMenu、WBP_LobbyMenu",
]:
    story.append(bullet(item))

story.append(p("9. 打包与测试", ST["h1"]))
story.append(p("项目已配置主菜单为默认地图，并添加窗口化启动设置。为了避免 UE 打包时中文路径和临时 C++ target 造成的问题，项目禁用了未使用的 GameplayStateTree 插件，并将关键蓝图资源迁移到英文目录。打包配置使用 Windows Development 版本进行测试。", ST["body"]))
for item in [
    "打开第一个 exe，点击“多人游戏”创建 Listen Server。",
    "第一个窗口进入 Lobby 等待。",
    "打开第二个 exe，点击“加入游戏”连接 127.0.0.1。",
    "人数达到 2 后，服务器自动切换到战斗关卡。",
    "测试敌人追击、攻击、玩家死亡重生、玩家射击、击杀得分与胜利提示。",
]:
    story.append(bullet(item))

story.append(p("10. 总结", ST["h1"]))
story.append(p("本 Demo 在 UE5 First Person 模板基础上完成了敌人 AI、玩家射击、生命值、死亡复活、得分胜利、UMG 界面和 Listen Server 多人流程。实现过程中采用服务器权威模型处理核心玩法状态，使用 Replication、Server RPC、Client RPC 和 Multicast RPC 分别解决状态同步、本地 UI 和动画表现问题，满足题目对敌人、得分胜利与多人网络对战的要求。", ST["body"]))

def build_pdf(path):
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=1.7 * cm,
        leftMargin=1.7 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.7 * cm,
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)


target = OUT
try:
    with OUT.open("ab"):
        pass
except PermissionError:
    target = FALLBACK_OUT

build_pdf(target)
print(target)
