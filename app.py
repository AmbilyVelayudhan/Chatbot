import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
import os

genai.configure(api_key="AIzaSyDEZ50oxRmA8RctqGwtEvnbRtAWnsude_o")  

model = genai.GenerativeModel("gemini-1.5-flash-latest")

st.set_page_config(page_title="Voice Mental Health Chatbot", layout="centered")
st.title("🧠 Mental Health Chatbot (with Voice Support)")
st.write("Hi, I'm here to listen and support you. Speak or type how you're feeling.")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak.")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            st.success(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            st.warning("Listening timed out.")
        except sr.UnknownValueError:
            st.warning("Could not understand audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
    return ""


if st.button("🎤 Speak Now"):
    voice_text = recognize_speech()
    if voice_text:
        st.session_state.chat_history.append(("You", voice_text))
        try:
            response = model.generate_content(
                f"You are a kind and understanding mental health chatbot. Respond supportively to:\n\n{voice_text}"
            )
            bot_reply = response.text
        except Exception as e:
            bot_reply = "Sorry, something went wrong."

        st.session_state.chat_history.append(("Bot", bot_reply))


text_input = st.text_input("Or type your message here:")

if text_input:
    st.session_state.chat_history.append(("You", text_input))
    try:
        response = model.generate_content(
            f"You are a kind and understanding mental health chatbot. Respond supportively to:\n\n{text_input}"
        )
        bot_reply = response.text
    except Exception as e:
        bot_reply = "Sorry, something went wrong."

    st.session_state.chat_history.append(("Bot", bot_reply))


st.markdown("---")
for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧍 You:** {msg}")
    else:
        st.markdown(f"**🤖 Bot:** {msg}")


st.markdown("---")
st.markdown("💬 This is a support chatbot and not a substitute for professional medical advice.")
