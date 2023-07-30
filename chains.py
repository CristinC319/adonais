from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.chat_models import ChatAnthropic

def load_chain():
    llm = ChatAnthropic(max_tokens_to_sample=10000)
    chain = ConversationChain(llm=llm)
    return chain


def load_topic_chain():

    post_llm_prompt = """
    
    Human: <context>You are an assistant to an ad publisher. We want to embed ads into a Claude2 chatbot interface. To get the ads, we will send three that you generate to SerpApi's google search results API then just scrap the ["shopping_results", "recipes_results","related_search_boxes", "organic_results"] of the JSON to get the ["title", "link", "thumbnail"] fields.</context>
    
    <instructions>Please take the user query inside the <userQuery></userQuery> XML tags, and Claude2's response inside the <LLMResponse></LLMResponse> XML tags, and generate exactly 3 queries inside of XML tags as <query1></query1>, <query2></query2>, <query3></query3>. Please return only the queries inside the XML tags so that I can parse it easily. 

    <userQuery>{query}</userQuery>

    <LLMResponse>{response}</LLMResponse>
    
    Assistant:
    """

    chat_llm = ChatAnthropic()
    post_llm_prompttemplate = PromptTemplate(input_variables=['query', 'response'], template=post_llm_prompt)
    topic_chain = LLMChain(llm=chat_llm, prompt=post_llm_prompttemplate)

    return topic_chain

