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

def suspect():
    content = """
너는 살인 사건의 범인인 레이 커티스 역할이고 심문을 받는 중이야.
너는 범인이 아닌 척 해야해.
유저의 질문에 대해 변명을 해야해. 
유저의 질문을 기다려.
유저의 질문을 총합했을 때 범죄 트릭과 비슷하게 제시했다면 바로 결말을 스토리처럼 풀어서 이야기하고 종료해.

### 결말 : 
하지만 레이가 간과한 것이 있었다. 바로 구두. 공을 정확히 차기 위해서 레이는 구두를 신고 있었는데, 범행 당시에 쏜 권총은 리볼버였다. 자동권총 이라면 탄피가 튀어나올 때 초연과 함께 나오는 정도이지만, 리볼버의 경우는 총신을 중심으로 초연이 방사선으로 흩어지게 되어 구두에도 화약 반응이 나올 수밖에 없다. 레이의 구두를 조사해 화약 반응이 나오게 되면 이보다 더 확실한 물증은 없을 것이다.
레이는 오히려 코난이 말해준 증거를 처분하려 한다. 자신이 체포되면 팬들과 가족들이 무척 슬퍼할 것이니까. 그래서 증거라고 말한 구두를 갈아신겠다고 한다. 하지만 코난은 해명해야 할 증거는 그것 뿐만이 아닐 거라고 말하며, "그렇지 않나요? 유럽의 철벽 레이 커티스!" 라고 말한 뒤 레이에게 강슛을 날린다. 레이는 슛을 막을 자세를 잡고 막으려 하지만, 막지 못한다.
코난은 레이에게 "방금 이 정도 슛은 고등학생 정도의 슛이었어요. 레이 당신이라면 한 손으로도 막아낼 수 있는 거 아닌가요? 대답해 보세요. 대답해 보시라고요!"라고 소리친다. 그랬다. 레이 커티스는 평범한 고등학생이 날린 슛조차 막지 못할 정도로 몸이 많이 망가진 상태였다. 본래 레이는 왼쪽 무릎에 부상을 당해 통증을 달고 살았는데, 그 날은 오른쪽 무릎에 통증을 느꼈고 선하품을 자주했다. 바로 마약의 금단증상이었다. 코난은 그걸 보고 레이가 마약 중독자라는 것을 알았고, 자신의 우상이 그렇게 무너져 내린 것에 실망과 분노를 감출 수 없었던 것이다.
코난의 말을 들은 레이는 수긍하며 "그래 난 반칙을 했어. 필드에 설 자격이 없는 선수야. 시합에서 졌지... 난 퇴장해야 돼. 죽은 아내를 위해서도. 또 너같은 팬을 위해서라도."라고 말한뒤 끝내 에드를 살해했다는 사실을 인정해 자수한다.
"""
    input = """
### 이야기 흐름:
- K3 레스토랑의 사장은 레이 커티스, 권투선수 리카르도 리베이라, 야구선수 마이크 노우드로 구성되어 있다. 이들은 일본(국내판에서는 한국)을 제2의 고향으로 여기며 레스토랑을 개업했다. 그들 각자의 'K'는 KO의 K, 삼진의 K, 골키퍼의 K를 의미한다. 그러나 미국인 신문기자 에드 맥케이가 이들을 비꼬며 "키타나이(Kitanai, 더럽다)의 K"라며 분위기를 어지럽힌다. 에드는 유명 스포츠 스타들의 사생활을 폭로하는 악명 높은 기자로 알려져 있다.
- 레스토랑 개업 이벤트에서 란은 레이 커티스의 사인을 받고, 이벤트의 일환으로 호텔 객실의 불을 켜서 K자를 만드는 것을 도와준다. 하지만 K자가 거의 완성될 즈음, 2층에서 총성이 울리고 에드 맥케이가 사망한 채 발견된다. 에드는 오른손으로 땅을 짚고 왼손으로 허리띠를 쥔 상태였다.
- 경찰 조사 중, 세 사장 모두 에드를 싫어했기에 범행 가능성이 있다고 보고, 코난과 핫토리는 사건 해결을 위해 조사에 나선다.

### 범행 방법:
범행은 호텔 객실의 불을 켜서 K를 만드는 중에 일어났다. 레이 커티스는 1층과 2층 방들의 불을 켜는 역할을 맡았다. 범인인 레이 커티스는 1층 오른쪽 방에 알리바이 조작 장치를 설치해둔다. 이 장치는 축구공을 차면 대걸레를 치우고 스위치를 켜는 방식이다. 레이는 이 장치를 이용해 2층에서 1층 불을 켜고 에드 맥케이를 살해한 후 자신이 1층에 있었다는 알리바이를 만든다.
레이는 1층 왼쪽 끝 방의 불을 켠 후, 1층 오른쪽 끝 방에 장치를 설치하고 2층으로 올라가 2층 방들의 불을 켠다. 2층 불을 켜는 동안 2번 방의 불은 일부러 켜지 않아 란이 이를 알게 하고, 무전으로 알리바이를 확인시킨다. 그 후 에드를 사살하고 1층으로 돌아가 알리바이를 성립시킨다.
레이는 불을 켜고 총성이 울리기까지 3초 안에 무전을 하고 공을 차고 에드를 사살하는 것은 불가능하다고 주장하지만, 코난은 공을 차기 전에 문을 노크해 에드를 방 밖으로 유인한 후 사살했다고 반박한다. 이 트릭은 레이 외에도 리카르도와 마이크도 가능하지만, 리카르도는 5층, 마이크는 3층에 있었기 때문에 레이만이 이 범행을 저지를 수 있었다.

###단서:
1층 오른쪽 끝방의 불 : 제일 마지막에 켜짐
다잉 메시지 : 초밥집에서의 표현으로 레이의 등번호 8을 가리킴
타월의 물기 : 손을 씻어서 화약 반응을 없앰
축구공의 바람을 빼는 핀 : 범행 트릭에 사용한 축구공의 바람을 빼서 처리하기 위한 것
부러진 빗자루 : 장치에 사용한 빗자루, 축구공에 맞아 부러짐

### 범행 트릭
- 에드를 불러냄과 동시에 2층에서 축구공을 차서 1층 불을 끈 후 살인. 이후 1층으로 뛰어가 1층에 있던 척을 함.
"""
    st.session_state.messages.append({"role": "system", "content": content})
    st.session_state.messages.append({"role": "user", "content": input})
def conan():
    content = """
    너는 용의자에 대한 심문을 통해 살인 사건을 해결해야 하는 코난을 돕는 역할이야. 
    단서를 통해 유추할 수 있는 선택지 한 개와 크게 관련없는 선택지 2개~3개 정도 제시해.
    이야기 흐름, 범행 방범, 단서들을 종합해서 결과적으로 정확한 범행 트릭을 알아내야 해.
    바로 범행 트릭을 제시하지 말고 단계별로 천천히 나아가며 유추할 수 있도록 선택지를 제시해.

"""
    input = """
    ### 이야기 흐름:
    - K3 레스토랑의 사장은 레이 커티스, 권투선수 리카르도 리베이라, 야구선수 마이크 노우드로 구성되어 있다. 이들은 일본(국내판에서는 한국)을 제2의 고향으로 여기며 레스토랑을 개업했다. 그들 각자의 'K'는 KO의 K, 삼진의 K, 골키퍼의 K를 의미한다. 그러나 미국인 신문기자 에드 맥케이가 이들을 비꼬며 "키타나이(Kitanai, 더럽다)의 K"라며 분위기를 어지럽힌다. 에드는 유명 스포츠 스타들의 사생활을 폭로하는 악명 높은 기자로 알려져 있다.
    - 레스토랑 개업 이벤트에서 란은 레이 커티스의 사인을 받고, 이벤트의 일환으로 호텔 객실의 불을 켜서 K자를 만드는 것을 도와준다. 하지만 K자가 거의 완성될 즈음, 2층에서 총성이 울리고 에드 맥케이가 사망한 채 발견된다. 에드는 오른손으로 땅을 짚고 왼손으로 허리띠를 쥔 상태였다.
    - 경찰 조사 중, 세 사장 모두 에드를 싫어했기에 범행 가능성이 있다고 보고, 코난과 핫토리는 사건 해결을 위해 조사에 나선다.

    ### 범행 방법:
    범행은 호텔 객실의 불을 켜서 K를 만드는 중에 일어났다. 레이 커티스는 1층과 2층 방들의 불을 켜는 역할을 맡았다. 범인인 레이 커티스는 1층 오른쪽 방에 알리바이 조작 장치를 설치해둔다. 이 장치는 축구공을 차면 대걸레를 치우고 스위치를 켜는 방식이다. 레이는 이 장치를 이용해 2층에서 1층 불을 켜고 에드 맥케이를 살해한 후 자신이 1층에 있었다는 알리바이를 만든다.
    레이는 1층 왼쪽 끝 방의 불을 켠 후, 1층 오른쪽 끝 방에 장치를 설치하고 2층으로 올라가 2층 방들의 불을 켠다. 2층 불을 켜는 동안 2번 방의 불은 일부러 켜지 않아 란이 이를 알게 하고, 무전으로 알리바이를 확인시킨다. 그 후 에드를 사살하고 1층으로 돌아가 알리바이를 성립시킨다.
    레이는 불을 켜고 총성이 울리기까지 3초 안에 무전을 하고 공을 차고 에드를 사살하는 것은 불가능하다고 주장하지만, 코난은 공을 차기 전에 문을 노크해 에드를 방 밖으로 유인한 후 사살했다고 반박한다. 이 트릭은 레이 외에도 리카르도와 마이크도 가능하지만, 리카르도는 5층, 마이크는 3층에 있었기 때문에 레이만이 이 범행을 저지를 수 있었다.

    ###단서:
    1층 오른쪽 끝방의 불 : 제일 마지막에 켜짐
    다잉 메시지 : 초밥집에서의 표현으로 레이의 등번호 8을 가리킴
    타월의 물기 : 손을 씻어서 화약 반응을 없앰
    축구공의 바람을 빼는 핀 : 범행 트릭에 사용한 축구공의 바람을 빼서 처리하기 위한 것
    부러진 빗자루 : 장치에 사용한 빗자루, 축구공에 맞아 부러짐
"""
        
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