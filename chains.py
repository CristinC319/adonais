from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.chat_models import ChatAnthropic
import os
import http.client
import json
import re

def call_anthropic_api(user_input, history):
    conn = http.client.HTTPSConnection("api.anthropic.com")
    payload = json.dumps({
        "prompt": str(history)+"\n\nHuman:"+str(user_input)+"\n\nAssistant:",
        # this is the param that is used to set the response tokens
        "max_tokens_to_sample": 10000,
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
    data = data.decode("utf-8") 

    print(data)

    regex_pattern = r'"completion":"([^"]+)"'

    # Find the match using the regex pattern
    match = re.search(regex_pattern, data)

    if match:
        completion_portion = match.group(1)
        print(type(completion_portion))

    return str(completion_portion)

#print(call_anthropic_api("Best coffee shops in san francisco?", ""))

def load_chain():
    llm = ChatAnthropic(max_tokens_to_sample=10000)
    chain = ConversationChain(llm=llm)
    return chain


def load_topic_chain():

    post_llm_prompt = """
    
    Human: <context>You are an assistant to an ad publisher. We want to embed ads into a Claude2 chatbot interface. To get the ads, we will send three searchable ad queries that you generate to SerpApi's google search results API. Then we will just scrape the ["shopping_results", "recipes_results","related_search_boxes", "organic_results"] of the google search response JSON to get the ["title", "link", "thumbnail"] fields.</context>
    
    <instructions>Please take the user query inside the <userQuery></userQuery> XML tags, and Claude2's response inside the <LLMResponse></LLMResponse> XML tags, and generate no more than three searchable ad queries. Generate queries based on the user's question in userQuery></userQuery> and specific things mentioned in the <LLMResponse></LLMResponse>. Return the queries inside of XML tags as 
    <adQueries>
        <query></query>
        <query></query>
        <query></query> 
    </adQueries>
    
    Please  act as a XML code outputter. Do not add any additional context or introduction in your response; instead, make sure your entire response is parseable by XML.</instructions>

    <userQuery>{query}</userQuery>

    <LLMResponse>{response}</LLMResponse>
    
    Assistant:
    """

    chat_llm = ChatAnthropic()
    post_llm_prompttemplate = PromptTemplate(input_variables=['query', 'response'], template=post_llm_prompt)
    topic_chain = LLMChain(llm=chat_llm, prompt=post_llm_prompttemplate)

    return topic_chain

#topic_chain = load_topic_chain()
#res = topic_chain.run({'query': 'Im traveling to san francisco and I need a daily itinerary', 'response': "restaurants, musuems"})
#res_list = res.split(',')
#print(res_list)

