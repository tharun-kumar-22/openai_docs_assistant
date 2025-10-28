import streamlit as st
import os
from dotenv import load_dotenv
from rag_engine_with_vision import RAGEngineWithVision
import time

load_dotenv()

FORMAT_ICONS = {
    'pdf': '📕', 'docx': '📘', 'doc': '📘', 'txt': '📄', 'rtf': '📋', 'md': '📄',
    'csv': '📊', 'xlsx': '📈', 'xls': '📈', 'ods': '📊',
    'png': '🖼️', 'jpg': '🖼️', 'jpeg': '🖼️', 'bmp': '🖼️', 'tiff': '🖼️', 'gif': '🖼️',
    'json': '💾', 'xml': '💾', 'yaml': '💾', 'yml': '💾'
}

st.set_page_config(
    page_title="TTZ.KT AI - OpenAI 2025",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3rem;
        font-weight: bold;
    }
    .model-info {
        background: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .memory-badge {
        background: #4CAF50;
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    div[data-testid="column"] button {
        background: transparent !important;
        border: none !important;
        color: #999 !important;
        font-size: 1.1rem !important;
        padding: 0.3rem 0.4rem !important;
        min-height: auto !important;
        height: auto !important;
        width: auto !important;
        box-shadow: none !important;
        transition: color 0.2s ease !important;
    }
    div[data-testid="column"] button:hover {
        color: #000 !important;
        background: transparent !important;
    }
    div[data-testid="column"] button[title="Edit"],
    div[data-testid="column"] button[title="Retry"],
    div[data-testid="column"] button[title="Copy"] {
        font-size: 1.8rem !important;
    }
</style>
""", unsafe_allow_html=True)

if 'rag_engine' not in st.session_state:
    st.session_state.rag_engine = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'document_processed' not in st.session_state:
    st.session_state.document_processed = False
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = []
if 'current_model' not in st.session_state:
    st.session_state.current_model = "gpt-4o-mini"
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = os.getenv("OPENAI_API_KEY", "")

st.markdown('<h1 style="color: red; text-align: center;">Ready To Go TTZ.KT AI Platform 2025</h1>', unsafe_allow_html=True)
st.markdown("### *Files Assistant + General Chat - OpenAI Powered*")
st.markdown('<span class="memory-badge">💾 Memory Only - Cloud AI</span>', unsafe_allow_html=True)
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Configuration")
    
    if not api_key:
        st.error("⚠️ OpenAI API key not found!")
        st.info("Please set OPENAI_API_KEY in your .env file")
        st.stop()
    else:
        st.success("✅ API Key Loaded")
    
    st.markdown("---")
    
    st.subheader("🤖 Select AI Model")
    
    available_models = {
        "🌟 GPT-5 (Latest 2025)": [
            "gpt-5",
            "gpt-5-mini",
            "gpt-5-nano"
        ],
        "⭐ GPT-4o (Recommended)": [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4o-2024-08-06",
            "gpt-4o-mini-2024-07-18"
        ],
        "🎯 o-Series (Reasoning)": [
            "o1",
            "o1-mini",
            "o3",
            "o3-mini",
            "o4-mini"
        ],
        "🔷 GPT-4 Turbo": [
            "gpt-4-turbo",
            "gpt-4-turbo-2024-04-09",
            "gpt-4-turbo-preview"
        ],
        "💎 GPT-4": [
            "gpt-4",
            "gpt-4-0613"
        ],
        "💰 GPT-3.5 (Budget)": [
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-0125"
        ]
    }
    
    all_models = []
    model_labels = []
    for category, models in available_models.items():
        for model in models:
            all_models.append(model)
            clean_category = category.split(" (")[0]
            model_labels.append(f"{clean_category}: {model}")
    
    selected_model_idx = st.selectbox(
        "Choose your model",
        range(len(all_models)),
        format_func=lambda i: model_labels[i],
        index=all_models.index(st.session_state.current_model) if st.session_state.current_model in all_models else 0
    )
    
    selected_model = all_models[selected_model_idx]
    
    model_info = {
        "gpt-5": "🌟 Most advanced AI (2025)",
        "gpt-5-mini": "⚡ Efficient GPT-5",
        "gpt-5-nano": "🚀 Fastest GPT-5 (low latency)",
        "gpt-4o": "⭐ Multimodal flagship",
        "gpt-4o-mini": "⚡ Fast & efficient",
        "o1": "🧠 Deep reasoning",
        "o1-mini": "💡 Efficient reasoning",
        "o3": "🔥 Latest reasoning",
        "o3-mini": "🔥 Mini Latest reasoning",
        "o4-mini": "🔥 Mini Latest reasoning",
        "gpt-4-turbo": "🚀 High performance",
        "gpt-4": "💎 Original GPT-4",
        "gpt-3.5-turbo": "💰 Budget-friendly"
    }
    
    info_text = "📋 OpenAI model"
    for key, info in model_info.items():
        if selected_model.startswith(key):
            info_text = info
            break
    
    st.markdown(f'<div class="model-info">📌 {info_text}</div>', unsafe_allow_html=True)
    
    if selected_model != st.session_state.current_model:
        if st.session_state.rag_engine:
            try:
                st.session_state.rag_engine.switch_model(selected_model)
                st.session_state.current_model = selected_model
                st.success(f"✅ Switched to {selected_model}")
            except Exception as e:
                st.error(f"❌ Failed: {str(e)}")
        else:
            st.session_state.current_model = selected_model
    
    st.markdown("---")
    
    st.subheader("📤 Upload Documents")
    st.caption("💡 Supports 13+ formats: PDF, Word, Excel, Images, JSON, XML, etc.")
    
    uploaded_files = st.file_uploader(
        "Drag and drop files here",
        type=['pdf', 'docx', 'doc', 'txt', 'rtf', 'csv', 'xlsx', 'xls', 'ods',
              'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'gif',
              'json', 'xml', 'yaml', 'yml', 'md'],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        if st.button("🚀 Process Documents", type="primary"):
            if not st.session_state.rag_engine:
                st.session_state.rag_engine = RAGEngineWithVision(
                    openai_api_key=api_key,
                    model=st.session_state.current_model,
                    vision_model="gpt-4o-mini"
                )
            
            all_chunks = []
            with st.status("Processing documents...", expanded=True) as status:
                for idx, uploaded_file in enumerate(uploaded_files, 1):
                    st.write(f"📄 Processing {idx}/{len(uploaded_files)}: {uploaded_file.name}")
                    try:
                        chunks = st.session_state.rag_engine.process_uploaded_file(uploaded_file)
                        all_chunks.extend(chunks)
                        st.write(f"✅ {uploaded_file.name}: {len(chunks)} chunks")
                    except Exception as e:
                        st.error(f"❌ {uploaded_file.name}: {str(e)}")
                
                if all_chunks:
                    st.write(f"🔨 Creating vectorstore ({len(all_chunks)} total chunks)...")
                    st.session_state.rag_engine.create_vectorstore(all_chunks)
                    st.write("🔗 Setting up chain...")
                    st.session_state.rag_engine.setup_chain()
                    st.session_state.processed_files = st.session_state.rag_engine.processed_documents.copy()
                    status.update(label="✅ Processing complete!", state="complete")
                    st.session_state.document_processed = True
                else:
                    status.update(label="❌ No documents processed", state="error")
    
    st.markdown("---")
    st.subheader("📊 System Status")
    
    if st.session_state.rag_engine:
        st.success("✅ Engine Ready")
        
        if st.session_state.processed_files:
            with st.expander("📂 Processed Files"):
                for file in st.session_state.processed_files:
                    ext = file.split('.')[-1].lower()
                    icon = FORMAT_ICONS.get(ext, '🔎')
                    st.caption(f"{icon} {file}")
        else:
            st.warning("🟡 No files")
        
        st.info(f"💬 {len(st.session_state.chat_history)} messages")
    else:
        st.error("🔴 Offline")
    
    if st.session_state.document_processed:
        st.markdown("---")
        if st.button("🔄 Reset", type="secondary"):
            st.session_state.chat_history = []
            st.session_state.document_processed = False
            st.session_state.processed_files = []
            if st.session_state.rag_engine:
                st.session_state.rag_engine.clear_documents()
            st.rerun()

st.markdown("---")

if not st.session_state.rag_engine:
    with st.spinner("Initializing engine..."):
        st.session_state.rag_engine = RAGEngineWithVision(
            openai_api_key=api_key,
            model=st.session_state.current_model,
            vision_model="gpt-4o-mini"
        )
    st.rerun()

if st.session_state.document_processed:
    st.info(f"🤖 **{st.session_state.current_model}** | {len(st.session_state.processed_files)} file(s) | 💾 Memory Only")
else:
    st.info(f"💬 **Chat Mode** | 🤖 {st.session_state.current_model} | Upload documents for document Q&A")

for idx, message in enumerate(st.session_state.chat_history):
    with st.chat_message(message["role"]):
        if st.session_state.edit_mode and st.session_state.edit_index == idx:
            edited_text = st.text_area(
                "Edit message:",
                value=message["content"],
                height=100,
                key=f"edit_area_{idx}",
                label_visibility="collapsed"
            )
            col1, col2, col3 = st.columns([0.8, 0.8, 8.4])
            with col1:
                if st.button("Send", key=f"send_{idx}", type="primary"):
                    st.session_state.edit_mode = False
                    st.session_state.edit_index = None
                    
                    st.session_state.chat_history = st.session_state.chat_history[:idx]
                    
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": edited_text
                    })
                    
                    with st.spinner(f"🤔 {st.session_state.current_model} thinking..."):
                        try:
                            response = st.session_state.rag_engine.ask_question(edited_text)
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": response["answer"],
                                "sources": response.get("source_documents", [])
                            })
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    
                    st.rerun()
            with col2:
                if st.button("Cancel", key=f"cancel_{idx}"):
                    st.session_state.edit_mode = False
                    st.session_state.edit_index = None
                    st.rerun()
        else:
            st.markdown(message["content"])
            
            if message["role"] == "user":
                col1, col2 = st.columns([0.5, 9.5])
                with col1:
                    if st.button("✎", key=f"edit_{idx}", help="Edit"):
                        st.session_state.edit_mode = True
                        st.session_state.edit_index = idx
                        st.rerun()
            
            elif message["role"] == "assistant":
                col1, col2, col3 = st.columns([0.5, 0.5, 9])
                with col1:
                    if st.button("↻", key=f"retry_{idx}", help="Retry"):
                        if idx > 0 and st.session_state.chat_history[idx-1]["role"] == "user":
                            user_msg = st.session_state.chat_history[idx-1]["content"]
                            st.session_state.chat_history = st.session_state.chat_history[:idx]
                            with st.spinner("Regenerating..."):
                                try:
                                    response = st.session_state.rag_engine.ask_question(user_msg)
                                    st.session_state.chat_history.append({
                                        "role": "assistant",
                                        "content": response["answer"],
                                        "sources": response.get("source_documents", [])
                                    })
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
                with col2:
                    copy_id = f"copy_text_{idx}"
                    button_html = f"""
                    <button onclick="copyToClipboard_{idx}()" style="
                        background: transparent;
                        border: none;
                        color: #999;
                        font-size: 1.8rem;
                        cursor: pointer;
                        padding: 0.3rem 0.4rem;
                    " title="Copy">⎘</button>
                    <script>
                    function copyToClipboard_{idx}() {{
                        const text = {repr(message["content"])};
                        navigator.clipboard.writeText(text).then(function() {{
                            alert('✅ Copied to clipboard!');
                        }}).catch(function(err) {{
                            console.error('Copy failed:', err);
                        }});
                    }}
                    </script>
                    """
                    st.components.v1.html(button_html, height=40)
                
                if "sources" in message and message["sources"]:
                    with st.expander("📚 Sources"):
                        for source_idx, source in enumerate(message["sources"], 1):
                            source_file = source.metadata.get('source', 'Unknown')
                            source_page = source.metadata.get('page', 'N/A')
                            file_ext = source_file.split('.')[-1].lower() if '.' in source_file else ''
                            icon = FORMAT_ICONS.get(file_ext, '🔎')
                            st.caption(f"**{source_idx}.** {icon} {source_file} (Page: {source_page})")
                            st.caption(f"_{source.page_content[:200]}..._")

if not st.session_state.edit_mode:
    if prompt := st.chat_input("Chat or ask about documents..."):
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })
        
        with st.chat_message("user"):
            st.markdown(prompt)
            col1, col2 = st.columns([0.5, 9.5])
            user_idx = len(st.session_state.chat_history) - 1
            with col1:
                if st.button("✎", key=f"edit_immediate_{user_idx}", help="Edit"):
                    st.session_state.edit_mode = True
                    st.session_state.edit_index = user_idx
                    st.rerun()
        
        with st.chat_message("assistant"):
            with st.spinner(f"🤔 {st.session_state.current_model} thinking..."):
                try:
                    response = st.session_state.rag_engine.ask_question(prompt)
                    
                    st.markdown(response["answer"])
                    
                    sources = response.get("source_documents", [])
                    if sources:
                        with st.expander("📚 Sources"):
                            for idx, source in enumerate(sources, 1):
                                source_file = source.metadata.get('source', 'Unknown')
                                source_page = source.metadata.get('page', 'N/A')
                                file_ext = source_file.split('.')[-1].lower() if '.' in source_file else ''
                                icon = FORMAT_ICONS.get(file_ext, '🔎')
                                st.caption(f"**{idx}.** {icon} {source_file} (Page: {source_page})")
                                st.caption(f"_{source.page_content[:200]}..._")
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response["answer"],
                        "sources": sources
                    })
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")

st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🚀 TTZ.KT AI - OpenAI 2025")
with col2:
    st.caption(f"🤖 {st.session_state.current_model if st.session_state.rag_engine else 'No model'}")
with col3:
    st.caption("v10.0 FINAL - GPT-5 + Enhanced UI")
