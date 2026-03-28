import streamlit as st
import requests

# 1. Page Config
st.set_page_config(page_title="AI Ved", layout="wide")

# 2. Simple & Fast CSS
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    section[data-testid="stSidebar"] { background-color: #111; color: white; }
    section[data-testid="stSidebar"] * { color: white !important; }
    .stTextInput>div>div>input { border-radius: 20px !important; border: 1px solid #dfe1e5 !important; }
    .stButton>button { background-color: #FF4B4B; color: white; border-radius: 20px; width: 100%; border: none; font-weight: bold; }
    .res-box { padding: 20px; border-radius: 10px; background-color: #f8f9fa; border-left: 5px solid #FF4B4B; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar - Sirf Search History
with st.sidebar:
    st.title("📜 Search History")
    st.write("---")
    if "history" not in st.session_state: st.session_state.history = []
    
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()

    for h in reversed(st.session_state.history[-5:]):
        st.caption(f"🕒 {h['question'][:30]}...")

# 4. Main Body
st.markdown("<h1 style='text-align: center;'>AI Ved</h1>", unsafe_allow_html=True)

# API Keys
G_KEY = "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"
T_KEY = "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"

# Search Box
query = st.text_input("", placeholder="Search here...", label_visibility="collapsed")

if st.button("Search") or (query and st.session_state.get('last_q') != query):
    if query:
        st.session_state.last_q = query
        with st.status("Exploring...", expanded=False):
            try:
                # Web Search
                url_s = "https://api.tavily.com/search"
                res_s = requests.post(url_s, json={"api_key": T_KEY, "query": query, "max_results": 3}).json()
                context = "\n".join([r['content'] for r in res_s.get('results', [])])
                
                # AI Logic
                url_a = "https://api.groq.com/openai/v1/chat/completions"
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": f"You are AI Ved. Context: {context}. Answer in Hinglish clearly."},
                        {"role": "user", "content": query}
                    ]
                }
                res_a = requests.post(url_a, json=payload, headers={"Authorization": f"Bearer {G_KEY}"}).json()
                answer = res_a['choices'][0]['message']['content']
                
                st.session_state.history.append({"question": query, "answer": answer})
                
                # Display Results
                st.markdown(f"<div class='res-box'><strong>Result:</strong><br>{answer}</div>", unsafe_allow_html=True)
            except:
                st.error("Bhai API limit shayad khatam ho gayi hai, thodi der baad try kar.")

st.markdown("<p style='text-align: center; margin-top: 50px; font-size: 12px; color: #888;'>Built by Gamer Ved</p>", unsafe_allow_html=True)
