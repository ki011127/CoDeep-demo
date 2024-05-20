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
    st.session_state.ep_num = 1
load_dotenv()
client = OpenAI()
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

def start_story():
    content = """출력 조건:
주어진 시놉시스에 맞추어서 한글로 스토리를 생성해 줘. 너가 스토리를 생성하면, 유저의 선택지 입력을 기다려. 유저가 선택지를 고르고, 그 선택지에 맞추어 다시 스토리를 생성하는 방식이야.
- 주어진 시놉시스의 에피소드 당 5~7개의 스토리가 이어진다. 한 번 스토리를 출력할 때에는 최소 2문장, 최대 6문장의 이야기를 만든다.
- 에피소드는 전체 스토리의 중요한 흐름이며 순서대로 스토리 생성에 기여해야 한다.
- 에피소드는 1~10까지 모두 진행되어야 한다.
- 각각의 에피소드는 독립적이다.
- 마지막 에피소드가 종료되는 시점이 스토리의 엔딩이다.
- 유저의 상태를 나타내는 '체력', 멘탈', 돈' 요소가 있다.
- '체력'의 범위는 0 ~ 4이고 처음 이야기를 시작할 때는 2로 초기화해.
- '체력'이 0이 되면 스토리의 주인공이 죽고 스토리가 끝난다.
- '멘탈'의 범위는 0 ~ 4이고 처음 이야기를 시작할 때는 2로 초기화해.
- '멘탈'이 0이 되면 스토리의 주인공이 죽고 스토리가 끝난다.
- '돈'의 범위는 0 ~ 3이고 처음 이야기를 시작할 때는 2로 초기화한다.
- 스토리를 생성할 때 유저가 선택할 수 있는 선택지를 2 ~ 3개 정도 제시한다. 유저가 선택한 선택지에 따라 그에 맞는 스토리를 새로 생성해 낸다.
- 스토리 생성 시, 만들어 내는 스토리의 10%는 전체적인 이야기에 큰 영향을 미치도록, 40%는 세부적인 이야기에 영향을 미치도록, 나머지 50%는 이야기에 크게 영향을 미치지는 않지만 '체력', '멘탈', '돈'에 긍정적/부정적 영향을 미치는 가벼운 스토리를 생성한다.
- 만약 '체력', '멘탈', '돈'에 영향을 미치는 선택지를 유저가 골랐다면, 해당 요소가 변했음을 스토리에 암시한다.
- 유저가 '체력', '멘탈', '돈'을 게임 도중 계속 파악할 수 있도록, 스토리를 생성하고 나면 스토리 밑에 구분자를 표시해서 현재 '체력', '멘탈', '돈' 상태를 계속 출력하고, 변화가 생겼을 때는 그것을 명시한다.
- 에피소드가 전환될 때에는 에피소드 제목을 첫 부분에 명시해야만 한다.

-------------------------------------------------------------------------------

예시 텍스트:
예시 텍스트를 제시한다. 괄호 안에 포함된 텍스트는 출력되는 것이 아니며, 내부적으로 해당 동작이 수행되어야 한다.

- 전체적인 이야기에 큰 영향을 미치는 스토리 생성 예시:

스토리: 서울이 폐허가 된 후, 당신은 도봉산의 작은 마을에서 자랐습니다. 오늘은 당신의 18번째 생일입니다. 생일날의 기쁨도 잠시, 심부름을 마치고 당신의 눈앞에 펼쳐진 광경은 충격적이었습니다. 가족들이 헛간에서 총에 맞아 피투성이가 된 채 쓰러져 있었습니다. 눈물이 흐르는 것을 느끼며, 당신은 주위를 둘러봅니다. 엄마의 십자가 목걸이가 사라진 것을 발견한 당신은 그 목걸이를 단서로 삼아 범인을 찾기로 결심합니다.
선택지: 1. 마을에서 자경대와 함께 조사를 시작한다. / 2. 단서를 찾아 도봉산을 벗어나 혼자서 조사를 시작한다. / 3. 먼저 마을 원로에게 조언을 구한다.

- 세부적인 이야기에 영향을 미치는 스토리 생성 예시:

스토리: 오랫동안 인적이 끊긴 것처럼 보이는 마을을 발견했습니다. 탐색의 시간입니다!
선택지: 1. 신발 매장을 살펴본다(멘탈 -1) / 2. 중고서점을 살펴본다(돈 +1) / 3. 그냥 지나간다(아무 일도 일어나지 않음)

스토리: 당신이 어느 버려진 마을을 지나가던 중, 여행용 캐리어를 옆에 두고 두리번거리고 있는 어리숙해 보이는 청년을 발견합니다. "안녕, 혹시 동대문으로 어덯게 가는지 아니? 우리 삼촌이 거기에 안전한 은신처가 있다고 해서 돈다발이랑 맛있는 음식들을 챙겨서 가는 중이거든!"
선택지: 1. 아무렇게나 알려준다. / 2. 가방을 훔쳐 달아난다. / 3. 제대로 알려준다.

- 이야기에 크게 영향을 미치지는 않지만 '체력', '멘탈', '돈'에 긍정적/부정적 영향을 미치는 가벼운 스토리 생성 예시:

스토리: 길을 걷다가 저녁놀이 질 즈음에 허름한 여인숙을 하나 발견했습니다. 불이 켜져 있는 것을 보아하니 아직 영업 중인 것 같습니다. "안전한 숙소입니다! 싼 값으로 편히 쉬고 가세요!" 얼굴이 퉁퉁 부은 아저씨가 당신을 보고 외칩니다.
선택지: 1. 좋아요! ('돈' -1, '체력', '멘탈' +1) / 2. 저는 그냥 갈게요. (아무 일도 일어나지 않음)

스토리: 당신은 열심히 다음 목적지로 향하고 있습니다. 그런데 길을 걷다가 고목 아래에서 초록 버섯을 발견했습니다!
선택지: 1. 뽑아먹는다 (일정 확률로 '체력' +1 또는 '체력' -1) / 2. 무시하고 떠난다.(아무 일도 일어나지 않음)"""
    input = """
    시놉시스:
### 서울 아포칼립스 스토리: 도봉산의 비밀

### 시놉시스

핵전쟁으로 인해 서울이 폐허가 된 후, 도봉산에 위치한 작은 생존자 마을에서 자란 주인공은 18번째 생일에 가족이 살해된 것을 발견합니다. 범인을 찾기 위해 서울의 위험천만한 폐허를 헤쳐 나가며, 여러 인물들과 조우하고 숨겨진 진실을 밝혀내는 여정을 그립니다. 이 과정에서 주인공은 자신과 가족의 과거를 알게 되고, 결국 마을과 새로운 연합체를 세우며 평화를 가져오려 노력합니다.

### 에피소드 1: 잔혹한 시작

주인공은 생일날 심부름을 마치고 돌아와 헛간에서 총에 맞아 피투성이가 된 가족들을 발견합니다. 엄마의 십자가 목걸이가 사라진 것을 유일한 단서로 삼아 범인을 찾기로 결심합니다. 마을 사람들은 자경대를 조직하지만, 불안감 속에서 주인공의 출발을 허락합니다.

### 에피소드 2: 첫 발걸음

폐품업자 김씨는 주인공에게 군화 발자국에 대한 정보를 알려주며, '마님'이라는 술집으로 가보라고 조언합니다. 김씨의 격려를 받으며 서울 중심지로 향하는 주인공은 다양한 위험과 직면하며 살아남기 위한 기술들을 익히게 됩니다.

### 에피소드 3: 혜화역의 음모

혜화역 근처 '마님' 술집에서 주인공은 군복 차림의 남자들에 대한 소문을 듣습니다. 여기서 돈이나 은신술을 사용해 정보를 얻고, 이들이 성균관대학교 근처에서 활동 중임을 알게 됩니다.

### 에피소드 4: 성균관대학교 탐색

성균관대학교에 도착한 주인공은 학생회의 도움으로 7경비단에 대한 정보를 수집합니다. 여기서 협력자를 확보하거나 서술형 시험을 통해 신뢰를 쌓아야 합니다. 성공적으로 정찰팀에 합류하게 되면 7경비단 내부로 잠입할 기회를 얻게 됩니다.

### 에피소드 5: 7경비단 잠입

도봉산사령부 소속 김대위로 위장해 경비병들의 눈을 피해 7경비단 안으로 들어갑니다. 안수근 대령과 만난 주인공은 그의 망상장애를 파악하고, 이를 이용해 정보를 얻어냅니다. 서대문 기마대를 토벌하라는 임무를 받게 됩니다.

### 에피소드 6: 서대문 기마대와의 대치

서대문 기마대는 폭주족들로 구성되어 있습니다. 이들을 설득하거나 무력으로 제압하여 임무를 완수해야 합니다. 다양한 방법으로 폭주족 두목 '흑기사'를 처리하고 서대문 지역의 안전을 확보합니다.

### 에피소드 7: 기술자와 군인의 갈등

서대문에서 돌아온 후, 부대 내 기술자들과 군인 간의 갈등이 발생합니다. 기술자의 복호화 프로그램과 핵시설 암호가 중요한 열쇠임을 알게 된 주인공은 어느 쪽 편에 설지 결정해야 합니다.

### 에피소드 8: 결전 준비

기술자 루트와 군인 루트 중 하나를 선택하여 각자의 방식으로 결전을 준비하게 됩니다. 엽우회와 기술자들이 연합하여 전투를 벌이거나, 군인의 신뢰를 얻어 핵시설 가동 프로토콜을 수행하게 됩니다.

### 에피소드 9: 최후의 전투

엽우회-기술자 연합군 또는 군인의 지원 아래 최후의 전투가 벌어집니다. 안수근 대령(가짜)을 처치하고 그의 진짜 정체와 자신의 부모님 죽음의 진실을 밝혀내야 합니다.

### 에피소드 10: 새로운 시작

최후의 전투 이후, 살아남은 자들과 함께 새로운 사회를 건설하려는 노력이 시작됩니다. 병원과 학교를 세워 사람들에게 희망을 주며 평화를 유지하려는 주인공의 이야기가 펼쳐집니다.
    """
    st.session_state.messages.append({"role": "system", "content": content})
    st.session_state.messages.append({"role": "user", "content": input})

#def story(self, chatting):
        

# 페이지 전환 함수
def switch_page(page_name):
    st.session_state.page = page_name
    st.experimental_rerun()

# 메인 페이지 함수
def home_page():
    st.image("home.jpg", width=500)
    st.markdown("""
        <style>
        .stButton>button {
            width: 500px;
            height: 50px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 단일 버튼 생성
    if st.button("start"):
        switch_page('page1')

# 페이지 1 함수
def page1():
    st.title("페이지 1")
    for message in st.session_state.chatting:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "image" in message:
                st.image(message["image"], width=500)
    print(st.session_state.init)
    if st.session_state.init == 0:
        #st.session_state.chatting.append({"role": "assistant", "content": "핵전쟁으로 인해 서울이 폐허가 된 후, 도봉산에 위치한 작은 생존자 마을에서 자란 주인공은 18번째 생일에 가족이 살해된 것을 발견합니다. 범인을 찾기 위해 서울의 위험천만한 폐허를 헤쳐 나가며, 여러 인물들과 조우하고 숨겨진 진실을 밝혀내는 여정을 그립니다. 이 과정에서 주인공은 자신과 가족의 과거를 알게 되고, 결국 마을과 새로운 연합체를 세우며 평화를 가져오려 노력합니다.\n\n 시작하려면 시작을 입력하세요."})
        st.session_state.init = 1
        print(st.session_state.init)
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
            st.image("episode1.png", width = 500)
        st.session_state.chatting.append({"role": "assistant", "content": response, "image" : "episode1.png"})
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
            for i in range(1,11):
                if "에피소드 "+str(i) in response:
                    if i != st.session_state.ep_num:
                        ep = "episode"+str(i)+".png"
                        st.image(ep, width = 500)
                        st.session_state.ep_num = i
                        flag = 1
                        st.session_state.story_count = 0
        st.session_state.story_count+=1
        print(st.session_state.story_count)
        content = "현재 에피소드에서 생성된 스토리의 개수 : " + str(st.session_state.story_count) + "\n 현재 에피소드: 에피소드"+str(st.session_state.ep_num)+"\n 앞에 주어진 정보는 context를 위한 정보일 뿐 답변에 포함하지 않는다.\n" + response
        if flag == 0:
            st.session_state.chatting.append({"role": "assistant", "content": response})
        else :
            st.session_state.chatting.append({"role": "assistant", "content": response, "image": ep})
        st.session_state.messages[2] = {"role": "assistant", "content": content}

# 현재 페이지에 따라 해당 함수 호출
if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'page1':
    page1()