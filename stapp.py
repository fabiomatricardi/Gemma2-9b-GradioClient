import streamlit as st
from gradio_client import Client
import datetime
import random
import string
from time import sleep
import tiktoken

# for counting the tokens in the prompt and in the result
#context_count = len(encoding.encode(yourtext))
encoding = tiktoken.get_encoding("r50k_base") 


modelname = "gemma-2-9b-it"
# Set the webpage title
st.set_page_config(
    page_title=f"Your LocalGPT ✨ with {modelname}",
    page_icon="🌟",
    layout="wide")

if "hf_model" not in st.session_state:
    st.session_state.hf_model = "gemma-2-9b-it"
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "repeat" not in st.session_state:
    st.session_state.repeat = 1.35

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.1

if "maxlength" not in st.session_state:
    st.session_state.maxlength = 500

if "speed" not in st.session_state:
    st.session_state.speed = 0.0

def writehistory(filename,text):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(text)
        f.write('\n')
    f.close()

def genRANstring(n):
    """
    n = int number of char to randomize
    """
    N = n
    res = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=N))
    return res

# create THE SESSIoN STATES
if "logfilename" not in st.session_state:
## Logger file
    logfile = f'{genRANstring(5)}_log.txt'
    st.session_state.logfilename = logfile
    #Write in the history the first 2 sessions
    writehistory(st.session_state.logfilename,f'{str(datetime.datetime.now())}\n\nYour own LocalGPT with 🌀 {modelname}\n---\n🧠🫡: You are a helpful assistant.')    
    writehistory(st.session_state.logfilename,f'🌀: How may I help you today?')

@st.cache_resource
def create_client():   
    print('loading the API gradio client for gemma-2-9b-it')
    yourHFtoken = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # put here you HF token
    client = Client("huggingface-projects/gemma-2-9b-it", hf_token=yourHFtoken)  
    return client

#AVATARS
av_us = 'user.png'  # './man.png'  #"🦖"  #A single emoji, e.g. "🧑‍💻", "🤖", "🦖". Shortcodes are not supported.
av_ass = 'assistant2.png'   #'./robot.png'
# Set a default model


### START STREAMLIT UI
st.image('Gemma-2-Banner.original.jpg', )
st.markdown("*powered by Streamlit & Gradio_client*", unsafe_allow_html=True )
st.markdown('---')


# CREATE THE SIDEBAR
with st.sidebar:
    st.image('banner.png', use_column_width=True)
    st.session_state.temperature = st.slider('Temperature:', min_value=0.0, max_value=1.0, value=0.1, step=0.02)
    st.session_state.maxlength = st.slider('Length reply:', min_value=150, max_value=2000, 
                                           value=500, step=50)
    st.session_state.repeat = st.slider('Repeat Penalty:', min_value=0.0, max_value=2.0, value=1.35, step=0.01)
    st.markdown(f"**Logfile**: {st.session_state.logfilename}")
    statspeed = st.markdown(f'💫 speed: {st.session_state.speed}  t/s')
    btnClear = st.button("Clear History",type="primary", use_container_width=True)

client = create_client()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"],avatar=av_us):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"],avatar=av_ass):
            st.markdown(message["content"])
# Accept user input
if myprompt := st.chat_input("What is an AI model?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": myprompt})
    # Display user message in chat message container
    with st.chat_message("user", avatar=av_us):
        st.markdown(myprompt)
        usertext = f"user: {myprompt}"
        writehistory(st.session_state.logfilename,usertext)
        # Display assistant response in chat message container
    with st.chat_message("assistant",avatar=av_ass):
        message_placeholder = st.empty()
        #time_placeholder = st.empty()
        with st.spinner("Gemma2 is thinking..."):
            full_response = ""
            start = datetime.datetime.now()
            res  =  client.submit(
                    message=myprompt,
                    max_new_tokens=st.session_state.maxlength,
                    temperature=st.session_state.temperature,
                    top_p=0.9,
                    top_k=50,
                    repetition_penalty=st.session_state.repeat,
                    api_name="/chat"
                    )
            
            for r in res:
                full_response=r
                #delta = datetime.datetime.now() - start
                message_placeholder.markdown(r+ "✨")
                delta = datetime.datetime.now() -start       
                totalseconds = delta.total_seconds()
                prompttokens = len(encoding.encode(myprompt))
                assistanttokens = len(encoding.encode(full_response))
                totaltokens = prompttokens + assistanttokens  
                st.session_state.speed = totaltokens/totalseconds   
                statspeed.markdown(f'💫 speed: {st.session_state.speed:.2f}  t/s')                    
            
            delta = datetime.datetime.now() - start
            totalseconds = delta.total_seconds()
            prompttokens = len(encoding.encode(myprompt))
            assistanttokens = len(encoding.encode(full_response))
            totaltokens = prompttokens + assistanttokens
            speed = totaltokens/totalseconds
            statspeed.markdown(f'💫 speed: {st.session_state.speed:.2f}  t/s')
            toregister = full_response + f"""
```

🧾 prompt tokens: {prompttokens}
📈 generated tokens: {assistanttokens}
⏳ generation time: {delta}
💫 speed: {st.session_state.speed:.3f}  t/s
```"""    
            message_placeholder.markdown(toregister)
            asstext = f"assistant: {toregister}"
            writehistory(st.session_state.logfilename,asstext)       
        st.session_state.messages.append({"role": "assistant", "content": toregister})
