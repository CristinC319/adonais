from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI, LLMChain, PromptTemplate
import os

'''
Load Langchain Chains
'''

os.environ["OPENAI_API_KEY"]="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"

def load_chain():
    llm = OpenAI(temperature=0)
    chain = ConversationChain(llm=llm)
    return chain


def load_topic_chain():

    post_llm_prompt = """You are an assistant to an ad publisher. 
    Given a user query, and an initial response, use the initial response to generate no more than 3 searchable
    queries that are likely to return sponsored results. Your answer should not contain anything but the queries.
    User query: {query}
    Initial response: {response}"""

    chat_llm = ChatOpenAI(temperature=0)
    post_llm_prompttemplate = PromptTemplate(input_variables=['query', 'response'], template=post_llm_prompt)
    topic_chain = LLMChain(llm=chat_llm, prompt=post_llm_prompttemplate)

    return topic_chain