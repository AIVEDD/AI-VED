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
    .stButton>button { background-color: #FF4B4B; color: white; border-radius: 20px; width: 100%; border: none; font-weight: bold; height: 45px; }
    
    /* Result Box - Direct Visibility */
    .res-box { 
        padding: 25px; 
        border-radius: 15px; 
        background-color: #f0f2f6; 
        border-left: 8px solid #FF4B4B; 
        margin-top: 30px;
        color: #111;
        font-size: 18px;
        line-height: 1.6;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
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
        st.caption(f"🕒 {h['question'][:30]}...")

# 4. Main Body
st.markdown("<h1 style='text-align: center; color: #111;'>AI Ved</h1>", unsafe_allow_html=True)

# API Keys
G_KEY = "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"
T_KEY = "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"

# Search Box
query = st.text_input("", placeholder="Kuch bhi puchiye...", label_visibility="collapsed")

if st.button("Search"):
    if query:
        # Simple spinner jo apne aap khatam ho jayega
        with st.spinner("Searching for you..."):
            try:
                # 1. Web Search
                url_s = "https://api.tavily.com/search"
                res_s = requests.post(url_s, json={"api_key": T_KEY, "query": query, "max_results": 3}).json()
                context = "\n".join([r['content'] for r in res_s.get('results', [])])
                
                # 2. AI Response
                url_a = "https://api.groq.com/openai/v1/chat/completions"
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": f"You are AI Ved. Context: {context}. Answer in Hinglish clearly and direct."},
                        {"role": "user", "content": query}
                    ]
                }
                res_a = requests.post(url_a, json=payload, headers={"Authorization": f"Bearer {G_KEY}"}).json()
                answer = res_a['choices'][0]['message']['content']
                
                # Save to history
                st.session_state.history.append({"question": query, "answer": answer})
                
                # 3. Direct Display (No Click Needed)
                st.markdown(f"""
                <div class='res-box'>
                    <h3 style='margin-top:0; color:#FF4B4B;'>AI Ved Result:</h3>
                    {answer}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error("Bhai thodi der baad try karo, limit shayad khatam hai.")
    else:
        st.warning("Pehle kuch likh toh lo bhai!")

st.markdown("<p style='text-align: center; margin-top: 100px; color: #888;'>Built by Gamer Ved</p>", unsafe_allow_html=True)
