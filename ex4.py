from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chatting" not in st.session_state:
    st.session_state.chatting = []
if "init" not in st.session_state:
    st.session_state.init = 0
if "story_count" not in st.session_state:
    st.session_state.story_count = 0
if "ep_num" not in st.session_state:
    st.session_state.ep_num = 1

load_dotenv()
client = OpenAI()
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

def start_story():
    content = """
이야기 흐름대로 이야기를 생성하며, 하나의 이야기 흐름 문장 당 5~6개의 에피소드가 생성된다. 하나의 에피소드씩 생성하고, 각 에피소드를 출력한 뒤에 유저의 선택지를 기다려야 한다. 만약 이야기 흐름이 7문장으로 주어졌다면 35~42개의 에피소드를 만들어야 한다. 주인공은 코난을 1인칭으로 두도록 한다. 
선택지를 생성할 떄는 절반의 확률로 스토리에 전혀 영향을 주지 않는 "대답" 형식으로 선택지를 제공한다. 이때 이전 질문은 주인공에게 무언가를 물어보는 형식이 바람직하다. (예를 들어 음식이 어떠냐는 질문에 "좋네요", "그저 그래요", "흠..."과 같은 대답). 그리고 나머지 절반은 스토리에 영향을 주긴 하지만 미미하게 미치도록 "행동" 형식으로 작성한다.

범인이 밝혀지기 전에 결정적 단서의 절반 이상을 유저가 기록했다면 기존 이야기 흐름대로 이야기가 진행되고, 절반 이상 유저가 기록하지 못하였다면 코난이 범인을 밝히지 못하고 사건은 미궁 속으로 빠져들었다는 식으로 이야기를 끝맺음한다.
"""
    input = """
이야기 흐름:
- 코난은 핫토리 헤이지에게 오사카의 레스토랑 개업 소식을 듣고 방문을 결정한다.
- 레스토랑에서 유명 스포츠 스타들이 모여 있는 것을 발견한다.
- 신문기자 에드 맥케이가 나타나 스타들의 과거를 폭로하며 갈등을 일으킨다.
- 에드 맥케이가 살해된 채 발견된다.
- 코난과 친구들이 사건을 조사하며, 세 명의 용의자가 존재한다.
- 코난이 여러 단서를 통해 범인 레이 커티스를 밝혀낸다.
- 레이 커티스가 에드를 살해한 동기를 설명하고 자백한다.

단서:
1층 오른쪽 끝방의 불 (단서1)
구두의 화약 반응 (단서2)
다잉 메시지 (단서3)
타월의 물기 (단서4)
축구공의 핀 (단서5)

범행 트릭:
대걸레와 축구공을 이용해 알리바이를 만들고, 1층에 있는 것처럼 보이게 하여 에드를 살해함.

범인 이름:
레이 커티스
    """
    st.session_state.messages.append({"role": "system", "content": content})
    st.session_state.messages.append({"role": "user", "content": input})

        
def page1():
    st.title("페이지 1")
    for message in st.session_state.chatting:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "image" in message:
                st.image(message["image"], width=500)
    if st.session_state.init == 0:
        st.session_state.init = 1
        start_story()
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.chatting.append({"role": "assistant", "content": response})
        st.session_state.messages.append({"role": "assistant", "content": response})
    if prompt := st.chat_input():
        flag = 0
        ep = ""
        with st.chat_message("user"):
            st.markdown(prompt)
        if st.session_state.init == 1:
            st.session_state.init = 2
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.chatting.append({"role": "user", "content": prompt})
        else:
            st.session_state.messages[3] = {"role": "user", "content": prompt}
            st.session_state.chatting.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.chatting.append({"role": "assistant", "content": response})
        st.session_state.messages[2] = {"role": "assistant", "content": response}

# 현재 페이지에 따라 해당 함수 호출
page1()