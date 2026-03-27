import streamlit as st
import requests

# Page Settings
st.set_page_config(page_title="Gamer Ved AI", page_icon="🔍")
st.title("🚀 Gamer Ved AI Search Engine")

# Keys
GROQ_KEY = "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"
TAVILY_KEY = "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"

query = st.text_input("Aap kya janna chahte hain?", placeholder="Yahan apna sawal likhein...")

if st.button("Search Karein"):
    if query:
        with st.spinner("Internet par dhoond raha hoon..."):
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
                    {"role": "system", "content": f"Answer based on: {context}. Use Hinglish (Hindi + English)."},
                    {"role": "user", "content": query}
                ]
            }
            res_a = requests.post(url_a, json=payload, headers=headers).json()
            
            st.subheader("Jawab:")
            st.write(res_a['choices'][0]['message']['content'])
    else:
        st.warning("Pehle kuch likho bhai!")
      
