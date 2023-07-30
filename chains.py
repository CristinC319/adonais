from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.chat_models import ChatAnthropic
import os
import http.client
import json

os.environ['ANTHROPIC_API_KEY']='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'

def call_anthropic_api():
    conn = http.client.HTTPSConnection("api.anthropic.com")
    payload = json.dumps({
        "prompt": "\n\nHuman: where should i go in new york for food \n\nAssistant:",
        # this is the param that is used to set the response tokens
        "max_tokens_to_sample": 150,
        "model": "claude-2"
    })
    headers = {
        'accept': 'application/json',
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json',
        'x-api-key': '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'
    }
    conn.request("POST", "/v1/complete", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

def load_chain():
    llm = ChatAnthropic()
    chain = ConversationChain(llm=llm)
    return chain


def load_topic_chain():

    post_llm_prompt = """You are an assistant to an ad publisher. 
    Given a user query, and an initial response, use the initial response to generate no more than 3 searchable queries that are likely to return sponsored results. Your answer should not contain anything but the queries. The format for the response is query 1,query 2,query 3 with no extra formatting
    User query: {query}
    Initial response: {response}"""

    chat_llm = ChatAnthropic()
    post_llm_prompttemplate = PromptTemplate(input_variables=['query', 'response'], template=post_llm_prompt)
    topic_chain = LLMChain(llm=chat_llm, prompt=post_llm_prompttemplate)

    return topic_chain

#topic_chain = load_topic_chain()
#res = topic_chain.run({'query': 'Im traveling to san francisco and I need a daily itinerary', 'response': "restaurants, musuems"})
#res_list = res.split(',')
#print(res_list)

