# from dotenv import load_dotenv
# from langchain.chains import LLMChain, TransformChain, SequentialChain
# import os
# from langchain.prompts import PromptTemplate
# import openai
# from langchain_openai import ChatOpenAI

# class MODEL:
#     load_dotenv()
#     def __init__(self):
#         # 객체 생성
#         self.llm = ChatOpenAI(model="gpt-4")
#         self.prompt_template = PromptTemplate(
#             template="generate interactive story",
#             input_variables=[]
#         )
#         self.c = LLMChain(llm=self.llm, output_key="result", prompt=self.prompt_template)
#         self.chain = SequentialChain(chains = [self.c], output_variables=["result"],input_variables=[])
#     def start_story(self):
#         for s in self.chain.stream({"topic": "멀티모달"}):
#     # 스트림에서 받은 데이터의 내용을 출력합니다. 줄바꿈 없이 이어서 출력하고, 버퍼를 즉시 비웁니다.
#             print(s["result"], end="", flush=True)
#         return self.chain.invoke(input={})["result"]
