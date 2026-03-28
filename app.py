import streamlit as st
import requests
from streamlit_mic_recorder import mic_recorder

# 1. Page Config
st.set_page_config(page_title="AI Ved", layout="wide")

# 2. Clean CSS
st.markdown("""
    <style>
    section[data-testid="stSidebar"] { background-color: #111; color: white; }
    section[data-testid="stSidebar"] * { color: white !important; }
    .stTextInput>div>div>input { border-radius: 20px !important; }
    .stButton>button { background-color: #FF4B4B; color: white; border-radius: 20px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar - History
with st.sidebar:
    st.title("📜 Search History")
    st.write("---")
    if "history" not in st.session_state: st.session_state.history = []
    
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()

    for h in reversed(st.session_state.history[-5:]):
        st.caption(f"🕒 {h['question'][:25]}...")

# 4. Main UI
st.markdown("<h1 style='text-align: center;'>AI Ved</h1>", unsafe_allow_html=True)

# --- VOICE RECORDER SECTION ---
st.write("🎤 **Tap to Speak:**")
# Ye button direct voice record karke text mein badalne mein help karega
audio = mic_recorder(
    start_prompt="🔴 Start Recording",
    stop_prompt="🟢 Stop & Search",
    key='recorder'
)

# Search box
query = st.text_input("", placeholder="Search here...", key="main_search", label_visibility="collapsed")

# Agar mic se audio milta hai (Note: iske liye aapko 'speech_to_text' function use karna hoga agar aapko direct text chahiye, 
# par simple raste ke liye hum text input hi use karenge jab tak aap manual likhein)

if st.button("Search") or query:
    if query:
        if "last_query" not in st.session_state or st.session_state.last_query != query:
            st.session_state.last_query = query
            with st.status("Exploring...", expanded=False):
                try:
                    G_KEY = "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"
                    T_KEY = "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"
                    
                    # Web Search
                    url_s = "https://api.tavily.com/search"
                    res_s = requests.post(url_s, json={"api_key": T_KEY, "query": query, "max_results": 3}).json()
                    context = "\n".join([r['content'] for r in res_s.get('results', [])])
                    
                    # AI Answer
                    url_a = "https://api.groq.com/openai/v1/chat/completions"
                    payload = {
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": f"You are AI Ved. Context: {context}. Answer in Hinglish."},
                            {"role": "user", "content": query}
                        ]
                    }
                    res_a = requests.post(url_a, json=payload, headers={"Authorization": f"Bearer {G_KEY}"}).json()
                    answer = res_a['choices'][0]['message']['content']
                    
                    st.session_state.history.append({"question": query, "answer": answer})
                    st.markdown("---")
                    st.write(answer)
                except:
                    st.error("Limit exceeded or connection error.")

st.markdown("<p style='text-align: center; margin-top: 50px; font-size: 12px; color: #888;'>Built by Gamer Ved</p>", unsafe_allow_html=True)
