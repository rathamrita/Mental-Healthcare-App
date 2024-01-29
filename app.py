import streamlit as st

from embedchain import App


@st.cache_resource
def embedchain_bot():
    return App()


st.title("💬 Mental Health Care")
st.caption("🚀 An Embedchain app powered by OpenAI!")
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """
        How I can manage stress at work?\n
        Can you tell me more about mindfulness meditation.\n
        How is depression diagnosed and treated?.\n
        What are some effective coping strategies for anxiety? :)
        """,
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything!"):
    app = embedchain_bot()

    if prompt.startswith("/add"):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
        prompt = prompt.replace("/add", "").strip()
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Adding to knowledge base...")
            app.add(prompt)
            message_placeholder.markdown(f"Added {prompt} to knowledge base!")
            st.session_state.messages.append({"role": "assistant", "content": f"Added {prompt} to knowledge base!"})
            st.stop()

    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        msg_placeholder.markdown("Thinking...")
        full_response = ""

        for response in app.chat(prompt):
            msg_placeholder.empty()
            full_response += response

        msg_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
