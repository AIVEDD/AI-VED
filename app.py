import streamlit as st
import requests

# Page Configuration
st.set_page_config(page_title="Gamer Ved AI", page_icon="🚀", layout="wide")

# Sidebar mein Chat History dikhayenge
st.sidebar.title("📜 Chat History")

# Initialize History (Agar pehle se nahi hai)
if "history" not in st.session_state:
    st.session_state.history = []

# Clear History Button
if st.sidebar.button("Clear History"):
    st.session_state.history = []
    st.rerun()

# Display History in Sidebar
for i, chat in enumerate(reversed(st.session_state.history)):
    st.sidebar.info(f"Q: {chat['question'][:20]}...")

# Main Page
st.title("Ved AI")

# Keys
GROQ_KEY = "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"
TAVILY_KEY = "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"

query = st.text_input("Aap kya janna chahte hain?", placeholder="Yahan apna sawal likhein...")

if st.button("Search Karein"):
    if query:
        with st.spinner("Internet se dhoond raha hoon..."):
            try:
                # 1. Search Logic
                url_s = "https://api.tavily.com/search"
                data_s = {"api_key": TAVILY_KEY, "query": query, "max_results": 3}
                res_s = requests.post(url_s, json=data_s).json()
                
                context = ""
                for r in res_s.get('results', []):
                    context += f"\nSource: {r['url']}\nContent: {r['content']}\n"
                
                # 2. AI Response Logic
                url_a = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {GROQ_KEY}"}
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": f"Answer based on: {context}. Use Hinglish."},
                        {"role": "user", "content": query}
                    ]
                }
                res_a = requests.post(url_a, json=payload, headers=headers).json()
                answer = res_a['choices'][0]['message']['content']
                
                # History mein save karo
                st.session_state.history.append({"question": query, "answer": answer})
                
                # Jawab dikhao
                st.subheader("Jawab:")
                st.write(answer)
                st.rerun() # Sidebar update karne ke liye
                
            except Exception as e:
                st.error(f"Dhat teri ki! Error aa gaya: {e}")
    else:
        st.warning("Pehle kuch likho toh bhai!")

# Current Chat Display (Sawal ke neeche jawab dikhane ke liye)
if st.session_state.history:
    last_chat = st.session_state.history[-1]
    st.divider()
    st.markdown(f"**Last Search:** {last_chat['question']}")
    st.write(last_chat['answer'])
                
