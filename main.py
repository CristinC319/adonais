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


if 'ads' not in st.session_state:
    st.session_state['ads'] = [{"thumbnail":"https://ik.imagekit.io/partiful/tr:f-auto,fo-auto,pr-true,w-800,dpr-auto/user/hjjMsPmsF4dMR4r0s1uRb4ryOxV2/dea-LIWFUN6IBTc0pl5OG",
        "title":"Join Anthropic's Hackathon",
        "link":"https://partiful.com/e/WLszTLRL4ftfhEqBtKGD"
        },{"thumbnail":"data:image/jpeg;base64,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",
        "title":"Langchain explained in 13 minutes...",
        "link":"https://www.youtube.com/watch?app=desktop&v=aywZrzNaKjs"
        },{"thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSdi-P3cV4S6XTertu1VclzwmEIGVV_RS2tS5vlF-yUwniA&s=4",
        "title": "Straight to the Gate Access: San Francisco Ferry to Sausalito",
        "link": "https://www.tripadvisor.com/",
        },{"thumbnail":"data:image/jpeg;base64,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"
        ,"title":"6-Month ML/AI Program ",
        "link":"https://www.google.com/aclk?sa=l&ai=DChcSEwjTlv3Yy7WAAxVLGK0GHUT7AagYABAEGgJwdg&ae=2&sig=AOD64_3g-nqwMGsVTbbrizluyeItyB3ZvA&q&adurl&ved=2ahUKEwin1vXYy7WAAxUOJTQIHVVCCYIQ0Qx6BAgKEAM",
        },{"thumbnail":"data:image/png;base64,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",
        "title":"LlamaIndex - Data Framework for LLM Applications",
        "link":"https://www.llamaindex.ai"
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

    st.session_state['ads'] = ad_list.append(st.session_state['ads'])

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
