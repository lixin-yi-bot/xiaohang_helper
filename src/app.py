import requests
import streamlit as st
from pathlib import Path
import time
from prompts import load_school_info, get_system_prompt, get_preset_questions

# ---------------------- 基础配置 ----------------------
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "sk-cjbipdwwtffwjblpqtwlbxroqufmrahtungkkfcwyabxwagy"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# 1、初始化会话历史
if "history" not in st.session_state:
    st.session_state["history"] = []
if "question" not in st.session_state:
    st.session_state["question"] = ""

# ---------------------- 页面主体 ----------------------
st.title("小航 · 郑州航院校园信息助手")

# 身份选择
role = st.selectbox("你是?", ["新生", "在校生", "教师"])

# 提问输入框
question = st.text_input("有啥想问的?", value=st.session_state["question"])

# 提问主按钮
if st.button("提问"):
    if not question.strip():
        st.warning("请输入问题后再提问")
    else:
        school_info = load_school_info()
        if "[错误]" in school_info:
            st.error(school_info)
        else:
            data = {
                "model": "Qwen/Qwen2.5-7B-Instruct",
                "messages": [
                    {"role": "system", "content": get_system_prompt(role, school_info)},
                    {"role": "user", "content": question},
                ],
            }
            start_time = time.time()
            try:
                # 3、加载思考动画spinner
                with st.spinner("小航正在思考..."):
                  response = requests.post(API_URL, headers=HEADERS, json=data, timeout=30)  
                end_time = time.time()
                use_time = round(end_time - start_time, 1)

                if response.status_code == 401:
                    st.error("API Key 无效或已过期，请检查密钥")
                elif response.status_code != 200:
                    st.error(f"API 请求失败，状态码：{response.status_code}")
                else:
                    result = response.json()
                    answer = result["choices"][0]["message"]["content"]
                    st.write(answer)
                    # 6、显示字数+耗时元信息
                    word_num = len(answer)
                    st.caption(f"回答字数：{word_num} 字 · 耗时：{use_time} 秒")

                    # 存入会话历史
                    item = {
                        "time": time.strftime("%H:%M:%S"),
                        "role": role,
                        "question": question,
                        "answer": answer
                    }
                    st.session_state["history"].append(item)

            except requests.exceptions.Timeout:
                st.error("AI 响应超时，请稍后再试")
            except requests.exceptions.ConnectionError:
                st.error("网络连接失败，请检查网络")
            except Exception as e:
                st.error(f"发生错误：{e}")

# ---------------------- 5、三大分类快捷提问Tabs ----------------------
st.divider()
st.subheader("快捷提问")
tab1, tab2, tab3 = st.tabs(["新生指南", "办事流程", "应急防骗"])

with tab1:
    st.markdown("**新生常见问题：**")
    new_q = ["报到那天先去哪？", "学费什么时候交？", "宿舍几人间？", "军训准备啥？", "宿舍怎么分配？", "校园卡怎么领？", "食堂在哪？", "图书馆怎么进？"]
    cols = st.columns(4)
    for idx, q in enumerate(new_q):
        with cols[idx % 4]:
            if st.button(q, key=f"new_{idx}"):
                st.session_state["question"] = q
                st.rerun()

with tab2:
    st.markdown("**办事流程问题：**")
    work_q = ["怎么补办校园卡？", "怎么申请请假？", "奖学金怎么申请？", "怎么开在读证明？", "转专业怎么转？", "图书馆几点关？", "校园卡丢了怎么补？", "差旅怎么报销？"]
    cols = st.columns(4)
    for idx, q in enumerate(work_q):
        with cols[idx % 4]:
            if st.button(q, key=f"work_{idx}"):
                st.session_state["question"] = q
                st.rerun()

with tab3:
    st.markdown("**应急防骗问题：**")
    safe_q = ["冒充辅导员要钱怎么办？", "宿舍被盗找谁？", "电信诈骗怎么举报？", "校园110是多少？", "心理危机找谁帮忙？", "火灾报警电话是多少？", "医疗急救电话是多少？", "遭遇诈骗怎么办？"]
    cols = st.columns(4)
    for idx, q in enumerate(safe_q):
        with cols[idx % 4]:
            if st.button(q, key=f"safe_{idx}"):
                st.session_state["question"] = q
                st.rerun()

# ---------------------- 1、2 问答历史区域+清空按钮 ----------------------
st.divider()
col_left, col_right = st.columns([4, 1])
with col_left:
    st.header("📝 问答历史")
with col_right:
    if st.button("清空历史"):
        st.session_state["history"] = []
        st.rerun()

# 倒序展示最新记录在最上方
history_list = st.session_state["history"]
for item in reversed(history_list):
    st.write(f'[{item["time"]}] {item["role"]} 提问：{item["question"]}')
    st.write(f"回答：{item['answer']}")
    st.caption("---")

# ---------------------- 黄页兜底电话 ----------------------
st.divider()
st.header("📞 电话黄页（静态兜底）")
st.caption("AI 答不上来时，可以直接查这里")
yellow_page = """| 部门 | 电话 |
|------|------|
| 校园 110（保卫处 24h） | 0371-61916110 ⚠ 以官方为准 |
| 学校总值班室 | 0371-61911000 ⚠ 以官方为准 |
| 后勤管理处 | 0371-61912800 ⚠ 以官方为准 |
| 后勤服务热线/物业报修 | 0371-61913110 ⚠ 以官方为准 |
| 校医院急诊（24h） | 0371-61912730 ⚠ 以官方为准 |
| 招生办公室 | 0371-61916161 ⚠ 以官方为准 |
| 信息管理中心（网信中心） | 0371-61912718 ⚠ 以官方为准 |"""
st.markdown(yellow_page)