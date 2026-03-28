import streamlit as st
import requests
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="Ved AI Voice Search", page_icon="🎙️", layout="wide")

# 2. Voice Recognition Logic (JavaScript)
voice_js = """
<script>
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'hi-IN'; // Hindi aur English dono samajh lega

function startRecording() {
    recognition.start();
}

recognition.onresult = (event) => {
    const speechToText = event.results[0][0].transcript;
    // Streamlit ke input box mein value bhej raha hai
    parent.postMessage({type: 'voice_input', text: speechToText}, "*");
};
</script>
<button onclick="startRecording()" style="background-color: #FF4B4B; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; width: 100%; font-weight: bold;">
    🎤 Bol Kar Search Karein
</button>
"""

# 3. Sidebar
with st.sidebar:
    st.title("🎮 Gamer Ved AI")
    st.markdown("---")
    st.info("Bikramganj's First Voice AI Search Engine")
    
    # Voice Button in Sidebar
    components.html(voice_js, height=60)
    st.caption("Tip: Mic button dabakar Hindi ya English mein bolein.")

    if "history" not in st.session_state:
        st.session_state.history = []
    
    st.subheader("📜 Recent History")
    for chat in reversed(st.session_state.history[-5:]):
        st.write(f"🔹 {chat['question'][:25]}...")

# 4. Main Interface
st.title("🎙️ AI Voice Search Engine")
st.caption("Niche likhein ya side se Mic use karein.")

# Keys
GROQ_KEY = "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"
TAVILY_KEY = "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"

# Input Area
query = st.text_input("", placeholder="Ask Ved AI...", key="search_input")

if st.button("Search") or (query and "last_query" not in st.session_state):
    if query:
        with st.status("Searching...", expanded=False) as status:
            try:
                # Web Search
                url_s = "https://api.tavily.com/search"
                data_s = {"api_key": TAVILY_KEY, "query": query, "max_results": 4}
                res_s = requests.post(url_s, json=data_s).json()
                
                context = ""
                for r in res_s.get('results', []):
                    context += f"\nSource: {r['url']}\nContent: {r['content']}\n"
                
                # AI Analysis
                url_a = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {GROQ_KEY}"}
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": f"Answer based on: {context}. Use Hinglish. Professional but friendly."},
                        {"role": "user", "content": query}
                    ]
                }
                res_a = requests.post(url_a, json=payload, headers=headers).json()
                answer = res_a['choices'][0]['message']['content']
                
                status.update(label="Ready!", state="complete")
                
                # Save & Display
                st.session_state.history.append({"question": query, "answer": answer})
                st.markdown("### 📝 Jawab:")
                st.write(answer)
                
            except Exception as e:
                st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Built by <b>Gamer Ved</b> | Voice Enabled AI</p>", unsafe_allow_html=True)
