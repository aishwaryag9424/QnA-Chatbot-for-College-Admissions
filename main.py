import streamlit as st
from palm_text1 import get_qa_chain, create_vector_db
from PIL import Image
from streamlit_chat import message
from langchain.vectorstores import FAISS



# Load image from file
img = Image.open("UTA.png")
new_size = (150, 150)
img = img.resize(new_size)
st.image(img)
#set the title
st.markdown("<h1 style='text-align: center; color: black;'>UTA Admissions Q&A Chatbot</h1>", unsafe_allow_html=True)

#add button to load the csv data 
create_vector_db()
print('vector db created! start the conversation!')
def conversation_chat(query):
    chain = get_qa_chain()
    result = chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["text"]))
    return result["text"]

def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about UTA 🤗"]
        
    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hello!"]


def display_chat_history():
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="Ask about UTA Admissions", key='input')
            submit_button = st.form_submit_button(label='Send')
            

        if submit_button and user_input:
            output = conversation_chat(user_input)

            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")

# Initialize session state
initialize_session_state()
# Display chat history
display_chat_history()
