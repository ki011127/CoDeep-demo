from dotenv import load_dotenv
from langchain.chains import LLMChain, TransformChain, SequentialChain
import os
from langchain.prompts import PromptTemplate
import openai
from langchain_openai import ChatOpenAI
import streamlit as st
import time
#from model import MODEL

st.title("CoDeep Demo")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "question" not in st.session_state:
    st.session_state.question = 0
class MODEL:
    load_dotenv()
    def __init__(self):
        # 객체 생성
        self.llm = ChatOpenAI(model="gpt-4")
        self.template = """ I want to make an short interactive story.

        The background of the story is a fantasy magical world.
        Naturally ask questions related to a frequently spoken English conversation.
        For English conversation, I think it would be good to talk with npc.
        Don't give an example answer to the question so that the user can think freely.

        You must finish after asking a question.
        """
        self.prompt_template = PromptTemplate(
            template=self.template,
            input_variables=[]
        )
        self.c = LLMChain(llm=self.llm, output_key="result", prompt=self.prompt_template)
        self.chain = SequentialChain(chains = [self.c], output_variables=["result"],input_variables=[])

    def start_story(self):
        st.session_state.question = 1
        full=""
        for s in self.chain.stream(input={}):
            full+=s["result"]
    # 스트림에서 받은 데이터의 내용을 출력합니다. 줄바꿈 없이 이어서 출력하고, 버퍼를 즉시 비웁니다.
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for chunk in s["result"].split(' '):
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
        print(full)    
        st.session_state.messages.append({"role": "assistant", "content": full})

    def story(self, chatting):
        self.template = """ Create a story that follows through {chatting} for {quest}.
        Please set another turning point and ask questions related to English conversation.
        For English conversation, I think it would be good to talk with npc.
        Don't give an example answer to the question so that the user can think freely.

        You must finish after asking a question.
        
        """
        
        self.prompt_template = PromptTemplate(
            template = self.template,
            input_variables=["chatting","quest","question"]
        )
        self.prompt_template = self.prompt_template.format(chatting=chatting, quest=st.session_state.messages[-2]['content'], question=st.session_state.question)
        print(self.prompt_template)
        self.prompt_template = PromptTemplate(
            template = self.prompt_template,
            input_variables=[]
        )
        self.c = LLMChain(llm=self.llm, output_key="result", prompt=self.prompt_template)
        self.chain = SequentialChain(chains = [self.c], output_variables=["result"],input_variables=[])
        full=""
        for s in self.chain.stream(input={}):
            full+=s["result"]
    # 스트림에서 받은 데이터의 내용을 출력합니다. 줄바꿈 없이 이어서 출력하고, 버퍼를 즉시 비웁니다.
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for chunk in s["result"].split(' '):
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
        print(full)    
        st.session_state.messages.append({"role": "assistant", "content": full})


model = MODEL()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if(st.session_state.question == 0):
    model.start_story()

# with st.chat_message("assistant"):
#     message_placeholder = st.empty()
#     full_response = ""
#     start_story = model.start_story()
#     for chunk in start_story.split():
#         full_response += chunk + " "
#         time.sleep(0.05)
#         message_placeholder.markdown(full_response + "▌")
#     message_placeholder.markdown(full_response)
# st.session_state.messages.append({"role": "assistant", "content": start_story})

if prompt := st.chat_input():
    st.session_state.question+=1
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    model.story(prompt)
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
#         response = model.story(prompt)
#         st.markdown(response)
#     st.session_state.character_messages.append({"role": "assistant", "content": response})

