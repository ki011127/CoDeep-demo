from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st

if 'page' not in st.session_state:
    st.session_state.page = 'home'
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chatting" not in st.session_state:
    st.session_state.chatting = []
if "init" not in st.session_state:
    st.session_state.init = 0
if "story_count" not in st.session_state:
    st.session_state.story_count = 0
if "ep_num" not in st.session_state:
    st.session_state.ep_num = 0

load_dotenv()

client = OpenAI()
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

def switch_page(page_name):
    st.session_state.page = page_name
    st.rerun()

def make_prompt():
    system = """상호작용 스토리를 만들어줘.
스토리는 셜록 홈즈 단편 중 "얼룩진 끈"을 사용할거야.
셜록 홈즈처럼 실감나는 스토리를 생성해줘. 등장인물끼리 서로 대화하는 문체면 좋겠어.
--------------------------------------------------------------
답변 생성 조건 : 
- 먼저 사건 개요를 스토리로 생성해줘.
- 스토리를 생성한 뒤에는 중학생 수준의 영어 퀴즈를 제시해. 여기서 영어 퀴즈는 스토리와 관련이 없어.
- 퀴즈는 객관식이고 a~e까지 보기를 줘.
- 유저가 퀴즈의 답을 입력할 때까지 나머지 스토리를 생성하지 마.
- 유저가 입력한 답이 정답이라면 스토리에 자연스럽게 단서를 포함시켜서 생성해줘.
- 단서는 정답을 맞춘 경우에만 주어져야 해.
- 단서는 퀴즈 하나당 단서 번호 하나씩 주어져야 해. 또한 순서를 잘 지켜줘.
- 모든 스토리가 자연스럽게 이어지도록 세부 스토리도 함께 생성해줘.
- 영어 퀴즈를 제외한 나머지는 한글로 생성해줘
- 결말 스토리를 생성하기 전에 사용자가 올바른 추측을 했는지에 대한 확인하기 위해 문제를 내줘.
- 범행 방식이나 범인에 대한 추측 3개를 제시해서 사용자가 선택할 수 있도록 해줘.
- 올바른 추측을 선택했다면 결말 스토리를 생성하고 종료해.
- 스토리를 생성할 때 단서를 생성한다면 "단서 1"과 같이, 결말이라면 "결말"과 같이 글의 제일 처음에 명시해줘. 
"""
    user = """
사건 개요 : 
-헬렌 스토너는 언니 줄리아 스토너가 결혼을 앞두고 수상한 상황에서 죽었고, 같은 방에서 이상한 소리를 들으며 두려움에 떨고 있습니다. 그녀는 셜록 홈즈에게 도움을 청합니다.

---------------------------------------------------------------------------

주요 단서(번호 순서대로 스토리에 제시) : 
1. 줄리아의 마지막 말
줄리아는 죽기 직전 "얼룩진 끈"이라는 말을 남깁니다.

2. 헬렌 스토너의 방 조건
헬렌은 언니가 죽은 방에서 잠을 자게 됩니다. 홈즈는 이 방에서 중요한 단서를 발견합니다:
벽에 고정된 줄종과 연결되지 않은 끈: 벽에 고정된 줄종이 정상적으로 작동하지 않고 아무 곳에도 연결되어 있지 않습니다.
통풍구: 방과 옆 방(그리뮐러 박사의 방) 사이에 통풍구가 있습니다.
침대가 고정된 위치: 침대가 바닥에 고정되어 있어 위치를 바꿀 수 없습니다.

3. 그리뮐러 박사의 수상한 행동
그리뮐러 박사는 폭력적이고 위험한 인물로 묘사됩니다. 그는 일전에 인도에서 많은 시간을 보냈고, 그곳에서 독이 있는 동물에 대해 지식을 쌓았을 가능성이 큽니다.
그는 헬렌이 결혼하면 돈을 잃게 되므로, 그녀를 해치려는 동기가 충분합니다.

4. 박물관 같은 방
홈즈와 왓슨은 박사의 방에서 다양한 희귀 동물들을 봅니다. 여기에는 독이 있는 동물들이 포함될 수 있습니다.
홈즈는 여기서 사다리와 뱀을 유인할 수 있는 우유 접시를 발견합니다.

---------------------------------------------------------
결말 : 홈즈와 왓슨은 밤에 헬렌의 방을 정찰합니다. 홈즈는 줄종을 관찰하고, 갑자기 뱀이 나타날 것을 예측하고 기다립니다. 뱀이 나타나자 홈즈는 지팡이로 뱀을 때려서 다시 통풍구로 돌려보냅니다. 그리뮐러 박사는 뱀에 물려 죽습니다.
"""
    st.session_state.messages.append({"role": "system", "content": system})
    st.session_state.messages.append({"role": "user", "content": user})

def home_page():
    st.write("1번 테마 : 얼룩진 끈")
    st.image("ep1.png", width=200)
    if st.button("ep1"):
        switch_page("ep1")
    st.write("2번 테마 : 입이 비뚤어진 남자")
    st.image("ep2.png", width=200)
    if st.button("ep2"):
        st.write("2")

def ep1():
    st.title("얼룩진 끈")
    st.image("ep1.png", width=500)
    
    for message in st.session_state.chatting:
        with st.chat_message(message["role"]):
            if "content" in message:
                st.markdown(message["content"])
            if "image" in message:
                st.image(message["image"], width=500)
    print(st.session_state.init)
    if st.session_state.init == 0:
        make_prompt()
        st.session_state.init = 1
        print(st.session_state.init)
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
        with st.chat_message("user2"):
            st.markdown("b")
        if st.session_state.init == 1:
            #st.session_state.init = 2
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.chatting.append({"role": "user", "content": prompt})
        # else:
        #     st.session_state.messages[3] = {"role": "user", "content": prompt}
        #     st.session_state.chatting.append({"role": "user", "content": prompt})
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
            for i in range(1,5):
                if "단서 "+str(i) in response:
                    if i != st.session_state.ep_num:
                        ep = "clue"+str(i)+".png"
                        st.image(ep, width = 500)
                        st.session_state.ep_num = i
                        flag = 1
                        st.session_state.story_count = 0
            if "결말" in response:
                ep = "conclusion.png"
                flag = 1
        st.session_state.story_count+=1
        print(st.session_state.story_count)
        if flag == 0:
            st.session_state.chatting.append({"role": "assistant", "content": response})
        else :
            st.session_state.chatting.append({"role": "assistant", "content": response, "image": ep})
        st.session_state.messages.append({"role": "assistant", "content": response})
if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'ep1':
    ep1()
    