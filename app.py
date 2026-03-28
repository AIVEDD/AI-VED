import streamlit as st
import requests
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="AI Ved", layout="centered")

# 2. Simple & Clean CSS
st.markdown("""
    <style>
    /* Pure Black/Dark Background */
    .main { background-color: #ffffff; color: #000000; }
    
    /* Sidebar text fix - Pure White */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Clean Search Input */
    .stTextInput>div>div>input {
        border-radius: 25px !important;
        padding: 12px 20px !important;
        border: 1px solid #dfe1e5 !important;
    }

    /* Red Search Button */
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 20px;
        padding: 5px 25px;
        border: none;
    }
    
    /* Result Box */
    .res-box {
        padding: 10px;
        border-top: 1px solid #eee;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.title("Ask AI Ved")
    st.write("---")
    
    # Simple Mic
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
    <button onclick="startVoice()" style="width:100%; padding:10px; border-radius:10px; background:#FF4B4B; color:white; border:none; cursor:pointer;">🎙️ Tap to Speak</button>
    """
    components.html(voice_js, height=60)
    
    if "history" not in st.session_state: st.session_state.history = []
    for h in reversed(st.session_state.history[-3:]):
        st.caption(f"🕒 {h['question'][:25]}...")

# 4. Main Body
st.markdown("<h1 style='text-align: center;'>AI Ved</h1>", unsafe_allow_html=True)

# API Keys
GROQ_KEY = "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"
TAVILY_KEY = "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"

query = st.text_input("", placeholder="Search here...", label_visibility="collapsed")

if st.button("Search"):
    if query:
        # Simple "Exploring..." Loader
        with st.status("Exploring...", expanded=False):
            try:
                # Web Search
                url_s = "https://api.tavily.com/search"
                res_s = requests.post(url_s, json={"api_key": TAVILY_KEY, "query": query, "max_results": 3}).json()
                context = "\n".join([r['content'] for r in res_s.get('results', [])])
                
                # AI
                url_a = "https://api.groq.com/openai/v1/chat/completions"
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": f"You are AI Ved. Context: {context}. Language: Hinglish."},
                        {"role": "user", "content": query}
                    ]
                }
                res_a = requests.post(url_a, json=payload, headers={"Authorization": f"Bearer {GROQ_KEY}"}).json()
                answer = res_a['choices'][0]['message']['content']
                st.session_state.history.append({"question": query, "answer": answer})
                
                st.markdown("<div class='res-box'>", unsafe_allow_html=True)
                st.write(answer)
                st.markdown("</div>", unsafe_allow_html=True)
            except:
                st.error("Error! Try again later.")

st.markdown("<br><p style='text-align: center; color: #999; font-size: 12px;'>Built by Gamer Ved</p>", unsafe_allow_html=True)
                        
