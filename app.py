import streamlit as st
import requests
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="AI Ved", page_icon="🤖", layout="wide")

# 2. Professional Dark Theme CSS
st.markdown("""
    <style>
    /* Main Background */
    .main { background-color: #0e1117; color: white; }
    
    /* Sidebar styling to make text WHITE */
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        color: white !important;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {
        color: white !important;
    }

    /* Search Input Box */
    .stTextInput>div>div>input {
        background-color: #1a1c23 !important;
        color: white !important;
        border: 1px solid #3e4451 !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }

    /* Search Button */
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        border: none;
    }

    /* Answer Card */
    .answer-box {
        background-color: #1a1c23;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #FF4B4B;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar - Ask AI Ved & Mic
with st.sidebar:
    st.markdown("<h1 style='color: white;'>🙋‍♂️ Ask AI Ved</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Stylish Neon Mic Button
    voice_js = """
    <script>
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'hi-IN';
    function startVoice() { recognition.start(); }
    recognition.onresult = (e) => {
        const transcript = e.results[0][0].transcript;
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: transcript}, '*');
    };
    </script>
    <div style="text-align: center; background: #1a1c23; padding: 20px; border-radius: 15px; border: 1px solid #3e4451;">
        <button onclick="startVoice()" style="background: #FF4B4B; border: none; border-radius: 50%; width: 70px; height: 70px; cursor: pointer; box-shadow: 0 0 15px #FF4B4B;">
            <span style="font-size: 35px;">🎙️</span>
        </button>
        <p style="color: white; margin-top: 15px; font-weight: bold; font-family: sans-serif;">Tap to Speak</p>
    </div>
    """
    components.html(voice_js, height=160)
    
    if "history" not in st.session_state: st.session_state.history = []
    st.markdown("<h3 style='color: white;'>Recent</h3>", unsafe_allow_html=True)
    for h in reversed(st.session_state.history[-3:]):
        st.caption(f"🕒 {h['question'][:25]}...")

# 4. Main UI - AI Ved
st.markdown("<h1 style='text-align: center; color: white;'>AI Ved</h1>", unsafe_allow_html=True)

# API Keys
GROQ_KEY = "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"
TAVILY_KEY = "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"

# Search Bar
query = st.text_input("", placeholder="Search here...", label_visibility="collapsed")

if st.button("Search"):
    if query:
        with st.spinner("Exploring..."):
            try:
                # 1. Search Logic
                url_s = "https://api.tavily.com/search"
                res_s = requests.post(url_s, json={"api_key": TAVILY_KEY, "query": query, "max_results": 3}).json()
                context = "\n".join([r['content'] for r in res_s.get('results', [])])
                
                # 2. AI Response Logic
                url_a = "https://api.groq.com/openai/v1/chat/completions"
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": f"You are AI Ved. Answer using context: {context}. Mix of Hindi and English."},
                        {"role": "user", "content": query}
                    ]
                }
                res_a = requests.post(url_a, json=payload, headers={"Authorization": f"Bearer {GROQ_KEY}"}).json()
                answer = res_a['choices'][0]['message']['content']
                
                st.session_state.history.append({"question": query, "answer": answer})
                
                # Result Container
                st.markdown(f"""
                <div class="answer-box">
                    <h4 style="color: #FF4B4B; margin:0;">AI Ved Result:</h4>
                    <p style="color: white; font-size: 16px; line-height: 1.6; margin-top:10px;">{answer}</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error("Error! API limit khatam ho sakti hai.")
    else:
        st.warning("Pehle kuch likho toh bhai!")

# Footer
st.markdown("<br><hr><p style='text-align: center; color: grey;'>Built by Gamer Ved</p>", unsafe_allow_html=True)
