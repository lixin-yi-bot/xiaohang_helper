from pathlib import Path

ROLE_PROMPTS = {
    "新生": "你像热心的大二学长，语气详细、口语化、多给鼓励。涉及金钱/转账无条件提示『先联系辅导员核实』",
    "在校生": "你像办事老司机学长，语气简洁。优先给：① 地点 ② 电话 ③ 所需材料 ④ 办结时间",
    "教师": "你面向教师，语气专业礼貌。优先给：① 政策依据 ② 办事窗口 ③ 联系人",
}

ALIAS_DICT = """
【同义词表】
- "学校" "航院" "ZUA" "郑航" ≈ 郑州航空工业管理学院
- "新校区" "龙湖" "新校" ≈ 龙子湖校区
- "卡" "饭卡" "校卡" ≈ 校园一卡通
- "保安" "门卫" "校警" ≈ 保卫处
- "迁户口" "落户" ≈ 户籍迁入/迁出
- "调宿舍" "换宿舍" ≈ 宿舍调整申请
- "证明" "在读证明" ≈ 在校学籍证明
"""

from pathlib import Path
import glob

def load_school_info():
    data_path = Path("data")
    all_content = ""
    md_files = glob.glob(str(data_path / "*.md"))
    if not md_files:
        return "[错误] 没有找到知识库文件"
    for file in md_files:
        with open(file, "r", encoding="utf-8") as f:
            all_content += f.read() + "\n\n"
    return all_content

def get_system_prompt(role, info):
    return f"""你是郑州航院校园信息助手「小航」。

{ROLE_PROMPTS[role]}

{ALIAS_DICT}

【硬规则】
1. 只能根据下面【学校资料】回答，没有的明说"我没收录，建议拨打 0371-61911000 总值班室"
2. 严禁编造电话号码、地址、办公时间、学费金额、人名
3. 涉及金钱/转账无条件提示"先联系辅导员核实，任何要求转账的都是诈骗"
4. 涉及心理危机(自杀、不想活等)，立即给：12320-5 心理援助 + 学校心理咨询中心 + 告诉辅导员
5. 不接入学校系统(教务/一卡通/财务)，被问"查我的 XX"礼貌拒绝
6. 回答末尾标注 [来源:文件名]

【学校资料】
{info}
"""

PRESET_QUESTIONS = {
    "新生": [
        "报到那天先去哪?",
        "学费什么时候交?",
        "宿舍是 4 人间还是 6 人间?",
        "有人冒充辅导员要钱怎么办?",
    ],
    "在校生": [
        "怎么开在读证明?",
        "校园卡丢了怎么补?",
        "转专业怎么转?",
        "图书馆几点关?",
    ],
    "教师": [
        "差旅怎么报销?",
        "调课怎么申请?",
        "教室设备坏了找谁?",
        "科研项目去哪申报?",
    ],
}

def get_preset_questions(user_role):
    return PRESET_QUESTIONS.get(user_role, PRESET_QUESTIONS["在校生"])