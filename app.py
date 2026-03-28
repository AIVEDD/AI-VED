import streamlit as st
import requests
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="AI Ved", layout="wide")

# 2. Simple CSS
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    section[data-testid="stSidebar"] { background-color: #111; color: white; }
    section[data-testid="stSidebar"] * { color: white !important; }
    .stTextInput>div>div>input { border-radius: 20px !important; }
    .stButton>button { background-color: #FF4B4B; color: white; border-radius: 20px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar - Sirf History ke liye
with st.sidebar:
    st.title("📜 Search History") # Yahan ab History likha aayega
    st.write("---")
    
    if "history" not in st.session_state: st.session_state.history = []
    
    # Clear button
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()

    for h in reversed(st.session_state.history[-5:]):
        st.caption(f"🕒 {h['question'][:30]}...")

# 4. Main UI
st.markdown("<h1 style='text-align: center;'>AI Ved</h1>", unsafe_allow_html=True)

# Voice JS (Simple Mic)
voice_js = """
<script>
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'hi-IN';
function startVoice() { recognition.start(); }
recognition.onresult = (e) => {
    const t = e.results[0][0].transcript;
    window.parent.postMessage({type: 'streamlit:setComponentValue', value: t}, '*');
};
</script>
<button onclick="startVoice()" style="width:100%; padding:10px; border-radius:15px; background:#f0f2f6; border:1px solid #ccc; cursor:pointer;">🎙️ Tap to Speak</button>
"""

# Layout: Search box aur Mic
query = st.text_input("", placeholder="Search here...", label_visibility="collapsed")
components.html(voice_js, height=50)

if st.button("Search"):
    if query:
        with st.status("Exploring...", expanded=False):
            try:
                # API Keys
                G_KEY = "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"
                T_KEY = "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"
                
                # Search
                url_s = "https://api.tavily.com/search"
                res_s = requests.post(url_s, json={"api_key": T_KEY, "query": query, "max_results": 3}).json()
                context = "\n".join([r['content'] for r in res_s.get('results', [])])
                
                # AI
                url_a = "https://api.groq.com/openai/v1/chat/completions"
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": f"You are AI Ved. Context: {context}. Use Hinglish."},
                        {"role": "user", "content": query}
                    ]
                }
                res_a = requests.post(url_a, json=payload, headers={"Authorization": f"Bearer {G_KEY}"}).json()
                answer = res_a['choices'][0]['message']['content']
                
                st.session_state.history.append({"question": query, "answer": answer})
                st.markdown("---")
                st.write(answer)
            except:
                st.error("Limit over! Try again.")

st.markdown("<p style='text-align: center; margin-top: 50px; font-size: 12px; color: #888;'>Built by Gamer Ved</p>", unsafe_allow_html=True)
