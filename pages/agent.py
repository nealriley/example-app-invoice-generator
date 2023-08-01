import streamlit as st
from audiorecorder import audiorecorder
import openai
import os

st.title("Helpful Agent")
audio = audiorecorder("Press to Speak", "Press to stop...")

# Initialize the chat messages history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, I'm an assistant that can help you answer basic questions. Please ask your question and I'd be happy to help."}
    ]

if len(audio) > 0:
    # To play audio in frontend:
    # st.audio(audio.tobytes())
    
    # To save audio to a file:
    wav_file = open("audio.mp3", "wb")
    wav_file.write(audio.tobytes()) 
    wav_file = open("audio.mp3", "rb")
    # Set your model ID
    model_id = "whisper-1"

    response = openai.Audio.transcribe(
        api_key=os.environ["OPENAI_API_KEY"],
        model=model_id,
        file=wav_file
    )
    print(response)
    st.session_state.messages.append({"role": "user", "content": response['text']})

    
# display the existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Prompt for user input and save
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

# If last message is not from assistant, we need to generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    # Call LLM
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            r = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            )
            response = r.choices[0].message.content
            st.write(response)

    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
