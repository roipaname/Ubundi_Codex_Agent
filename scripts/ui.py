# ui.py
import streamlit as st
import requests

API_URL = "http://localhost:8000"  # FastAPI backend

st.set_page_config(
    page_title="Ziyanda's Personal Study AI Agent",
    page_icon="👑",
    layout="wide"
)

# --- Royal Blue Theme CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #0f1b3c 0%, #1e3a6f 25%, #2d5aa0 75%, #3d7dd1 100%);
            color: #ffffff;
            
        }
        
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* Header Styling */
        .royal-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(90deg, rgba(15, 27, 60, 0.9), rgba(45, 90, 160, 0.9));
            border-radius: 20px;
            margin-bottom: 2rem;
            border: 2px solid rgba(255, 215, 0, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        .royal-title {
            font-family: 'Playfair Display', serif;
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(45deg, #ffd700, #ffffff, #ffd700);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        
        .royal-subtitle {
            font-family: 'Inter', sans-serif;
            font-size: 1.2rem;
            color: #e6f0fa;
            font-weight: 300;
            letter-spacing: 1px;
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(15, 27, 60, 0.6);
            border-radius: 15px;
            padding: 8px;
            margin-bottom: 2rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 215, 0, 0.2);
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 60px;
            padding: 0px 24px;
            background: linear-gradient(135deg, rgba(30, 96, 145, 0.8), rgba(13, 59, 102, 0.8));
            border-radius: 12px;
            color: #ffffff;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            border: 1px solid rgba(255, 215, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: linear-gradient(135deg, rgba(45, 90, 160, 0.9), rgba(30, 96, 145, 0.9));
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(255, 215, 0, 0.2);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #ffd700, #ffed4e) !important;
            color: #0f1b3c !important;
            font-weight: 600;
            box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4);
        }
        
        /* Card Styling */
        .royal-card {
            background: linear-gradient(135deg, rgba(30, 96, 145, 0.15), rgba(13, 59, 102, 0.15));
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem 0;
            border: 1px solid rgba(255, 215, 0, 0.2);
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }
        
        /* Input Styling */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 215, 0, 0.3);
            border-radius: 12px;
            color: #ffffff;
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            padding: 1rem;
            backdrop-filter: blur(10px);
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #ffd700;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
        }
        
        .stTextInput label {
            color: #ffd700 !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
        }
        
        /* Button Styling */
        .stButton button {
            background: linear-gradient(135deg, #1e6091, #0d3b66);
            color: #ffffff;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
            border-radius: 15px;
            padding: 0.8rem 2rem;
            border: 2px solid rgba(255, 215, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background: linear-gradient(135deg, #ffd700, #ffed4e);
            color: #0f1b3c;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
        }
        
        /* Checkbox Styling */
        .stCheckbox label {
            color: #e6f0fa !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
        }
        
        /* Answer Box Styling */
        .answer-box {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(230, 240, 250, 0.95));
            border: 2px solid rgba(255, 215, 0, 0.4);
            border-radius: 20px;
            padding: 2rem;
            margin: 1.5rem 0;
            color: #0f1b3c;
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            line-height: 1.7;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(10px);
        }
        
        /* File Uploader Styling */
        .stFileUploader label {
            color: #ffd700 !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
        }
        
        .stFileUploader > div > div {
            background: rgba(255, 255, 255, 0.1);
            border: 2px dashed rgba(255, 215, 0, 0.5);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        
        /* Success/Error Messages */
        .stSuccess {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(21, 128, 61, 0.2));
            border: 1px solid rgba(34, 197, 94, 0.5);
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }
        
        .stError {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(185, 28, 28, 0.2));
            border: 1px solid rgba(239, 68, 68, 0.5);
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }
        
        /* Spinner */
        .stSpinner {
            color: #ffd700 !important;
        }
        
        /* Code Section Styling */
        .code-generator {
            background: linear-gradient(135deg, rgba(15, 27, 60, 0.9), rgba(30, 96, 145, 0.9));
            border-radius: 20px;
            padding: 2rem;
            border: 2px solid rgba(255, 215, 0, 0.3);
            margin: 1rem 0;
            backdrop-filter: blur(10px);
        }
        
        .stTextArea textarea {
            background: rgba(0, 0, 0, 0.3);
            border: 2px solid rgba(255, 215, 0, 0.3);
            border-radius: 12px;
            color: #ffffff;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            backdrop-filter: blur(5px);
        }
        
        .stSelectbox label {
            color: #ffd700 !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
        }
        
        /* Hide Streamlit Menu */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Royal Header ---
st.markdown("""
    <div class="royal-header">
        <div class="royal-title">👑 Clarence's Personal AI ChatBot</div>
        <div class="royal-subtitle">Your Personal CV Assistant </div>
    </div>
""", unsafe_allow_html=True)

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🔍 Ask Questions", "📂 Upload Content"])

# --- Tab 1: Ask Questions ---
with tab1:
    st.markdown('<div class="royal-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input("🔎 What would you like to know about Clarence?", key="query_input")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        use_web = st.checkbox("Include Web Search", value=True)
    
    if st.button("🚀 Ask Your Question", key="ask_btn"):
        if query.strip():
            with st.spinner("🤔 Analyzing your question..."):
                try:
                    resp = requests.post(f"{API_URL}/ask", data={"q": query, "use_web": use_web})
                    answer = resp.json().get("answer", "No answer returned.")
                except Exception as e:
                    answer = f"⚠️ Could not connect to backend: {e}"
            
            st.markdown(f'<div class="answer-box">💡 <strong>Answer:</strong><br><br>{answer}</div>', unsafe_allow_html=True)
        else:
            st.warning("Please enter a question first!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Tab 2: Upload Content ---
with tab2:
    st.markdown('<div class="royal-card">', unsafe_allow_html=True)
    
    st.markdown("### 📚 Build Your Knowledge Base")
    st.markdown("Upload your CV notes, PDFs, or documents to enhance the AI's knowledge.")
    
    uploaded_file = st.file_uploader(
        "Choose your file", 
        type=["txt", "pdf", "docx"],
        help="Supported formats: TXT, PDF, DOCX, MD"
    )
    
    if uploaded_file is not None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📤 Upload & Process", key="upload_btn"):
                with st.spinner("🔄 Processing and indexing your document..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.read())}
                        resp = requests.post(f"{API_URL}/add", files=files)
                        chunks_added = resp.json().get('file', 0)
                        st.success(f"✅ Successfully processed! Added {chunks_added} knowledge chunks to your database.")
                    except Exception as e:
                        st.error(f"⚠️ Upload failed: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)



# --- Footer ---
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #e6f0fa; font-family: 'Inter', sans-serif; padding: 1rem;">
        <small>👑 Royal Lecture RAG Agent - Powered by AI Excellence</small>
    </div>
""", unsafe_allow_html=True)