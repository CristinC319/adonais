import streamlit as st
from streamlit_chat import message

from chains import load_chain, load_topic_chain
from scrape import get_ads

'''
Streamlit main (streamlit run main.py)
'''

st.set_page_config(page_icon="💬", page_title="Adonais", initial_sidebar_state="expanded")

st.markdown(
    "<h1 style='text-align: left;font:Clarkson;'>Adonais</h1>",
    unsafe_allow_html=True)

# Langchain ---------------------------------------------

chain = load_chain()
topic_chain = load_topic_chain()

# Chat ---------------------------------------------

if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = ["Hey!"]

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hello! Ask me anything."]

response_container = st.container() # chat history container
container = st.container() # user history container

with container:
    
    with st.form(key='my_form', clear_on_submit=True): 
        
        user_input = st.text_input("Query:", placeholder="Ask a question here", key='input') 
        submit_button = st.form_submit_button(label='Send')
    
# Main ---------------------------------------------

if 'topics' not in st.session_state:
    st.session_state.topics = [] 

def get_topics(topic_results): 
    ''''
    tasks: 
    * how many topics to keep at a time
    * set (all unique)
    * what format do the topics come from the LLM - if it sucks then don't change the state
    '''

    topics = st.session_state.topics

    for top in topic_results:
        topics.append(top)

    st.session_state.topics = topics[-5:]

    return topics


if submit_button and user_input:
    
    # Response from LLM
    output = chain.run(input=user_input)

    # run topic chain on the query & response
    topic_results = topic_chain.run({'query': user_input, 'response': output})

    # (1) get list (set) of topics from state 
    topic_list = get_topics()

    # (2) get serp results
    ad_list = get_ads(topic_list)

    # add adds to state - same with topics / how to deal with existing ads and what to kick out 


    # Update chat states
    st.session_state['history'].append((user_input, output))
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)


# displaying history
if st.session_state['generated']:
    
    with response_container:
        
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="identicon")
            message(st.session_state["generated"][i], key=str(i), avatar_style="shapes")

# Rendering sidebar ---------------------------------------------

if 'ad1' not in st.session_state:
    st.session_state.ad1 = "ex1.png"
    st.session_state.ad2 = "ex1.png"
    st.session_state.ad3 = "ex1.png"
    st.session_state.ad4 = "ex1.png"
    st.session_state.ad5 = "ex1.png"


st.sidebar.header("Ad1")
st.sidebar.image(st.session_state.ad1, width=200)
st.sidebar.write("desc")

st.sidebar.header("Ad2")
st.sidebar.image(st.session_state.ad2, width=200)

st.sidebar.header("Ad3")
st.sidebar.image(st.session_state.ad3, width=200)

st.sidebar.header("Ad4")
st.sidebar.image(st.session_state.ad4, width=200)

st.sidebar.header("Ad5")
st.sidebar.image(st.session_state.ad5, width=200)
