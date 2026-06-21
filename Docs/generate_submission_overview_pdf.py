from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "Docs"
OUT = DOCS / "左涵俊-四川大学-开局一课客户端大作业-提交简述.pdf"


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
    raise RuntimeError("No Chinese font found")


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="CN-Bold",
            fontSize=21,
            leading=29,
            alignment=TA_CENTER,
            spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            fontName="CN",
            fontSize=10.5,
            leading=15,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#555555"),
            spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="CN-Bold",
            fontSize=14,
            leading=20,
            textColor=colors.HexColor("#1F4E79"),
            spaceBefore=10,
            spaceAfter=6,
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
            fontSize=9.2,
            leading=14,
            leftIndent=15,
            firstLineIndent=-9,
            spaceAfter=3,
        ),
        "table": ParagraphStyle(
            "table",
            fontName="CN",
            fontSize=8.8,
            leading=12.5,
        ),
        "link": ParagraphStyle(
            "link",
            fontName="CN",
            fontSize=9.5,
            leading=14,
            leftIndent=18,
            textColor=colors.HexColor("#0B5394"),
            spaceAfter=5,
        ),
    }


def p(text, style):
    return Paragraph(escape(text), style)


def bullet(text):
    return p("- " + text, ST["bullet"])


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("CN", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(2 * cm, 1.2 * cm, "左涵俊-四川大学-开局一课客户端大作业提交简述")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"第 {doc.page} 页")
    canvas.restoreState()


def file_table():
    rows = [
        [p("提交文件", ST["table"]), p("内容说明", ST["table"])],
        [p("双人联机演示视频", ST["table"]), p("展示双开 exe、创建 Listen Server、加入游戏、进入战斗地图、多人死亡重生与协作击杀。", ST["table"])],
        [p("单人玩法演示视频", ST["table"]), p("展示单人射击、敌人追击攻击、扣血死亡、击杀得分与胜利提示。", ST["table"])],
        [p("技术说明 PDF", ST["table"]), p("详细说明蓝图模块、网络同步、敌人 AI、玩家系统、UI、得分胜利和打包测试。", ST["table"])],
        [p("提交简述 PDF", ST["table"]), p("概述项目背景、提交内容、文档结构与当前完成情况。", ST["table"])],
    ]
    tbl = Table(rows, colWidths=[4.2 * cm, 12 * cm], repeatRows=1)
    tbl.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "CN"),
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


register_fonts()
ST = build_styles()
story = []

story.append(p("左涵俊-四川大学-开局一课客户端大作业提交简述", ST["title"]))
story.append(p("UE5 First Person 多人协作清理训练场 Demo", ST["subtitle"]))

story.append(p("1. 项目与个人说明", ST["h1"]))
story.append(p("本次大作业基于 Unreal Engine 5.7 官方 First Person 模板实现，是我的第一个 UE5 游戏 Demo。此前我主要长期使用 Unity 进行游戏开发，因此本项目也是一次从 Unity 工作流切换到 UE5 蓝图、UMG、Replication 和打包流程的完整实践。", ST["body"]))
story.append(p("项目从创建模板到完成可录制版本总共用时约三天。由于近期时间比较紧，没有来得及进行更完整的美术、关卡和武器系统打磨，因此最终提交的是一个最小可演示版本，重点放在题目要求的核心功能：敌人移动和攻击玩家、玩家击败敌人、得分与胜利机制、以及本地 Listen Server 多人联机流程。", ST["body"]))
story.append(p("GitHub 仓库：", ST["body"]))
story.append(p("https://github.com/Left-Jun/Left_Jun-Unreal-Afterclasswork_Tencent2026", ST["link"]))
story.append(p("个人网站：", ST["body"]))
story.append(p("https://leftjun.com", ST["link"]))

story.append(p("2. 提交文件说明", ST["h1"]))
story.append(file_table())
story.append(Spacer(1, 5))

story.append(p("3. 技术说明 PDF 的结构与内容", ST["h1"]))
for item in [
    "项目概述与作业要求对应关系：说明 Demo 的整体目标，并逐条对应题目要求。",
    "GitHub 链接与多人网络实现要点：列出仓库链接，并概述 Listen Server、Server RPC、Client RPC、Multicast RPC 和 Replication 的分工。",
    "玩家系统：说明玩家射击、服务器权威伤害、客户端本地射线反馈、血量、死亡菜单和服务器重生逻辑。",
    "敌人系统：说明敌人受伤死亡、服务器端索敌、NavMesh 追击、攻击动画、延迟伤害和动画蓝图。",
    "联机、得分、胜利与大厅：说明主菜单、Lobby、PostLogin 人数判断、ServerTravel、GameMode 计分和 GameState 胜利同步。",
    "UI 系统：说明主菜单、战斗 HUD、准星、死亡复活菜单，以及本地玩家 UI 创建和输入模式恢复。",
    "主要资源、关卡、打包与测试：列出关键蓝图和关卡路径，并记录 Development 打包、本地双开 exe 测试流程。",
]:
    story.append(bullet(item))

story.append(p("4. 当前完成情况", ST["h1"]))
story.append(p("当前版本已经完成题目要求的核心闭环：玩家可以射击并击败敌人，敌人会追击和攻击玩家，击杀敌人会增加队伍分数，达到目标后显示胜利；多人模式下支持本地双窗口加入同一 Listen Server，并能同步玩家生命、死亡重生、敌人 AI、攻击表现、得分和胜利状态。", ST["body"]))
story.append(p("如果后续继续完善，我会优先补充更完整的武器系统、敌人生成波次、关卡目标引导、UI 视觉打磨，以及更稳定的联机房间设置流程。", ST["body"]))

doc = SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    rightMargin=1.7 * cm,
    leftMargin=1.7 * cm,
    topMargin=1.6 * cm,
    bottomMargin=1.7 * cm,
)
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUT)
