import streamlit as st
import requests
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="AI Ved", page_icon="🤖", layout="wide")

# 2. Stylish CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextInput>div>div>input {
        background-color: #1a1c23 !important;
        color: white !important;
        border: 1px solid #3e4451 !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
    }
    .answer-box {
        background-color: #1a1c23;
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #FF4B4B;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar - Ask AI Ved
with st.sidebar:
    st.title("🙋‍♂️ Ask AI Ved")
    st.markdown("---")
    
    # Voice/Mic Button Component
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
    <div style="text-align: center;">
        <button onclick="startVoice()" style="background: none; border: 2px solid #FF4B4B; border-radius: 50%; padding: 15px; cursor: pointer;">
            <span style="font-size: 30px;">🎙️</span>
        </button>
        <p style="color: white; margin-top: 10px; font-size: 14px;">Click Mic to Speak</p>
    </div>
    """
    components.html(voice_js, height=120)
    
    if "history" not in st.session_state: st.session_state.history = []
    st.subheader("Recent")
    for h in reversed(st.session_state.history[-3:]):
        st.caption(f"• {h['question'][:20]}...")

# 4. Main UI - AI Ved
st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>AI Ved</h1>", unsafe_allow_html=True)

# Keys
GROQ_KEY = "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"
TAVILY_KEY = "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"

# Search Layout
query = st.text_input("", placeholder="Search here...", label_visibility="collapsed")

if st.button("Search"):
    if query:
        # User ki demand ke mutabiq "Exploring..." likha aayega
        with st.spinner("Exploring..."):
            try:
                # Search
                url_s = "https://api.tavily.com/search"
                res_s = requests.post(url_s, json={"api_key": TAVILY_KEY, "query": query, "max_results": 3}).json()
                context = "\n".join([r['content'] for r in res_s.get('results', [])])
                
                # AI Response
                url_a = "https://api.groq.com/openai/v1/chat/completions"
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": f"You are AI Ved. Answer based on: {context}. Use Hinglish."},
                        {"role": "user", "content": query}
                    ]
                }
                res_a = requests.post(url_a, json=payload, headers={"Authorization": f"Bearer {GROQ_KEY}"}).json()
                answer = res_a['choices'][0]['message']['content']
                
                st.session_state.history.append({"question": query, "answer": answer})
                
                # Result Display
                st.markdown(f"""
                <div class="answer-box">
                    <h4 style="color: #FF4B4B; margin-top:0;">AI Ved says:</h4>
                    <p style="font-size: 16px; line-height: 1.6;">{answer}</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error("Kuch problem aa gayi hai, thodi der baad try karein.")
    else:
        st.warning("Pehle kuch likho toh sahi!")

# Footer
st.markdown("<p style='text-align: center; margin-top: 50px; opacity: 0.5;'>Built by Gamer Ved</p>", unsafe_allow_html=True)
    
