import streamlit as st
from streamlit import sidebar

from memory import prompt
from utils import get_chat_response
from langchain.memory import ConversationBufferMemory

st.title("👒 专属于你的加藤惠")

with sidebar:
    openai_api_key = st.text_input("请输入OpenAI Key:",type="password")
    st.markdown("[获取OpenAI key](https://platform.openai.com/account/api-keys)")
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "ai", "content": "你好，我叫加藤惠，你也可以叫我惠。"}
    ]
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])
prompt = st.chat_input()
temperature = st.slider("⭐ 请输入视频脚本的创造力（数字越小说明更严谨，反之更多样）", min_value=0.0, max_value=1.0,
                       value=0.5, step=0.1)
if prompt:
    if not openai_api_key:
        st.info("请输入你的OpenAI密钥")
        st.stop()
    st.session_state["messages"].append({"role":"human","content":prompt})
    st.chat_message("human").write(prompt)

    with st.spinner("惠正在思考你说的话..."):
        response = get_chat_response(prompt,st.session_state["memory"],
                                     openai_api_key,temperature)
    msg = {"role":"ai","content":response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)

