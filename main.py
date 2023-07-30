import streamlit as st
from streamlit_chat import message

from chains import load_chain, load_topic_chain
from scrape import get_ads

st.set_page_config(
    page_icon="💬", page_title="Adonais", initial_sidebar_state="expanded"
)

st.markdown(
    "<h1 style='text-align: left;font:Clarkson;'>Adonais</h1>", unsafe_allow_html=True
)

# ~/anaconda3/envs/standard/bin/streamlit run main.py
# Langchain ---------------------------------------------

chain = load_chain()
topic_chain = load_topic_chain()

# Chat ---------------------------------------------

if "history" not in st.session_state:
    st.session_state["history"] = []

if "past" not in st.session_state:
    st.session_state["past"] = ["Hey!"]

if "generated" not in st.session_state:
    st.session_state["generated"] = ["Hello! Ask me anything."]

# TODO: Change deafults and add more
if 'ads' not in st.session_state:
    st.session_state['ads'] = [{
        "thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSdi-P3cV4S6XTertu1VclzwmEIGVV_RS2tS5vlF-yUwniA&s=4",
        "title": "Straight to the Gate Access: San Francisco Ferry to Sausalito",
        "link": "https://www.tripadvisor.com/",
    }]
    

response_container = st.container()  # chat history container
container = st.container()  # user history container

with container:
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_input(
            "Query:", placeholder="Ask a question here", key="input"
        )
        submit_button = st.form_submit_button(label="Send")

# Main ---------------------------------------------

if "topics" not in st.session_state:
    st.session_state.topics = []


def get_topics(topic_results):
    """'
    tasks:
    * how many topics to keep at a time
    * set (all unique)
    * what format do the topics come from the LLM - if it sucks then don't change the state
    """

    topics = st.session_state.topics

    for top in topic_results:
        topics.append(top)

    st.session_state.topics = topics[-5:]

    return topics

if submit_button and user_input:
    # Response from LLM
    output = chain.run(input=user_input)

    # run topic chain on the query & response
    topic_results = topic_chain.run({"query": user_input, "response": output})
    topic_results = topic_results.split(",")

    ### OPTIONAL: get location name (default San Francisco rn) as well for scraping

    # (1) get list (set) of topics from state
    topic_list = get_topics(topic_results)
    print(topic_list)

    # (4) IF WE HAVE TIME (LLM again - why is this ad relevant to the chat/ user)

    # Update chat states
    st.session_state["history"].append((user_input, output))
    st.session_state["past"].append(user_input)
    st.session_state["generated"].append(output)

    # serp
    ad_list = get_ads(topic_list)

    st.session_state['ads'] = ad_list

# displaying history
if st.session_state["generated"]:
    with response_container:
        for i in range(len(st.session_state["generated"])):
            message(
                st.session_state["past"][i],
                is_user=True,
                key=str(i) + "_user",
                avatar_style="identicon",
            )
            message(st.session_state["generated"][i], key=str(i), avatar_style="shapes")

# Rendering sidebar ---------------------------------------------

# [title](link)
link_format = "[{}]({})"

# st.sidebar.header("Sponsored")
for ad in st.session_state.ads:
    st.sidebar.image(ad["thumbnail"], width=200)
    st.sidebar.write(link_format.format(ad["title"], ad["link"]))
