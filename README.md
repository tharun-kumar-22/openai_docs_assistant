# TTZ.KT AI - OpenAI RAG Platform

**ENHANCED FINAL VERSION v10.0** - Multi-Format Document Intelligence with GPT-5

## 🌟 What's New in v10.0

### ✨ GPT-5 Models Added!
- **gpt-5** 🌟 - Most advanced AI from 2025
- **gpt-5-turbo** 🚀 - Fast GPT-5 variant
- **gpt-5-mini** ⚡ - Efficient GPT-5
- **30+ total models** available

### Enhanced Features (from v9.0)
- **General Chat Mode** - Chat works WITH or WITHOUT documents
- **Edit Button** - Edit any user message and regenerate response
- **Retry Button** - Regenerate AI responses with one click
- **Copy Button** - Copy AI responses to clipboard instantly
- **Auto-Initialize** - Engine starts automatically on launch
- **Better UI** - Cleaner icon buttons with smooth hover effects

## 🚀 Core Features

### Dual Mode Operation
1. **Chat Mode** (No documents)
   - General AI conversation
   - Knowledge Q&A
   - Creative writing
   - Coding help
   - ANY topic discussion

2. **Document Q&A Mode** (With documents)
   - Ask questions about uploaded files
   - Get answers with source citations
   - Multi-document analysis
   - Cross-reference information

### File Support (13+ Formats)
- **Documents**: PDF, DOCX, DOC, TXT, RTF, MD
- **Spreadsheets**: CSV, XLSX, XLS, ODS
- **Images**: PNG, JPG, JPEG, BMP, TIFF, GIF (with OCR)
- **Data**: JSON, XML, YAML, YML

### Security & Privacy
- ✅ **Memory-only processing** - no permanent storage
- ✅ **Temporary files deleted immediately**
- ✅ **Only vector embeddings in memory**
- ✅ **Cloud AI with local data control**

## 📖 Quick Start

### Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup API key
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here

# 3. Run
streamlit run app.py
```

### First Steps

1. **Start Chatting Immediately**
   - No setup needed!
   - Just type and chat with AI
   - Upload documents anytime for document Q&A

2. **Or Upload Documents**
   - Click "Drop files here"
   - Select any supported format
   - Click "🚀 Process Documents"
   - Start asking questions about your files

## 🎯 How to Use

### General Chat (No Documents)
```
You: What's the capital of France?
AI: Paris is the capital of France...

You: Write a Python function to sort a list
AI: Here's a Python sorting function...
```

### Document Q&A (With Documents)
```
[Upload PDF document]

You: What are the main topics in this document?
AI: Based on the document, the main topics are...
📚 [Shows source citations]

You: Summarize page 5
AI: Page 5 discusses... [with source]
```

### Enhanced UI Features

#### ✎ Edit Button
- Click edit icon next to any user message
- Modify your question
- Click "Send" to regenerate response
- Entire conversation rebuilds from that point

#### ↻ Retry Button
- Click retry icon on any AI response
- Regenerates answer using same question
- Great for getting alternative perspectives

#### ⎘ Copy Button
- One-click copy of AI responses
- Paste anywhere you need
- Perfect for documentation or notes

## 🤖 Model Selection

### Recommended Models

**For Latest Technology (2025):**
- **gpt-5** 🌟 - Most advanced AI
- **gpt-5-turbo** - Fast GPT-5
- **gpt-5-mini** - Efficient GPT-5

**For Most Users:**
- **gpt-4o-mini** ⭐ - Fast, smart, affordable (RECOMMENDED)
- **gpt-4o** - Most capable multimodal

**For Complex Reasoning:**
- **o1-mini** - Efficient reasoning
- **o3-mini** - Latest reasoning model
- **o1** - Deep reasoning capabilities

**For Budget:**
- **gpt-3.5-turbo** - Most affordable
- **gpt-3.5-turbo-0125** - Latest 3.5

### Hot Model Switching
- Select any model from dropdown
- Click "🔄 Switch Model"
- Continue conversation without reprocessing
- Preserves all documents and chat history

## 📁 File Processing

### Memory-Only Processing
```
Upload → Create Temp File → Process → Delete Temp
                               ↓
                        Vector Embeddings
                        (RAM only)
```

**Benefits:**
- Zero disk footprint
- Enhanced privacy
- Faster cleanup
- Session-based

### Supported Workflows
1. **Single File** - Upload and process one document
2. **Batch Upload** - Process multiple files at once
3. **Mixed Formats** - Upload PDFs, Excel, images together
4. **Incremental** - Add more files anytime

## 🎨 UI Features

### Chat Actions
```
┌─────────────────────────────────┐
│ User: Your question             │
│ [✎]                             │  ← Edit
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ AI: Response here...            │
│ [↻] [⎘]                         │  ← Retry, Copy
│ 📚 [View Sources]               │  ← Source citations
└─────────────────────────────────┘
```

### Status Indicators
- 🟢 Engine Ready
- 📂 Processed Files (expandable)
- 💬 Message Count
- 💾 Memory Only badge

## 🔧 Advanced Features

### Automatic Temperature
- **o1/o3 models**: temperature=1.0 (required)
- **Other models**: temperature=0.7 (optimal)
- Automatically configured per model

### Conversation Memory
- Maintains full chat history
- Context-aware responses
- Follow-up questions work perfectly
- Preserved during model switching

### Source Citations
- See exact document sections
- Page/section numbers
- File type icons
- Preview of source text

## 💡 Tips & Tricks

### Getting Best Results

**In Chat Mode:**
- Ask anything - no restrictions
- Request code, explanations, ideas
- Use for brainstorming
- Get help with any topic

**In Document Q&A Mode:**
- Ask specific questions
- Request summaries
- Find information across files
- Compare documents

### Editing Tips
- Edit typos or unclear questions
- Refine questions for better answers
- Branch conversations in different directions
- Experiment with phrasing

### Model Selection Tips
- **Quick tasks**: gpt-3.5-turbo or gpt-4o-mini
- **Important work**: gpt-4o
- **Deep thinking**: o1 or o3-mini
- **Cost-sensitive**: gpt-3.5-turbo

## 🛠️ Troubleshooting

### Copy Button Not Working
```bash
# Install xclip (Linux) or equivalent
sudo apt-get install xclip  # Linux
# or
brew install pbcopy  # macOS (usually pre-installed)
```

### API Key Issues
```bash
# Check .env file
cat .env

# Should show:
OPENAI_API_KEY=sk-...
```

### Memory Issues
- Process fewer files at once
- Clear documents after use
- Restart if needed

## 📊 System Architecture

```
┌──────────────────────────────────┐
│      Streamlit UI                │
│  (Chat, Edit, Retry, Copy)       │
└──────────┬───────────────────────┘
           │
    ┌──────▼──────┐
    │ RAG Engine  │
    │ Dual Mode:  │
    │ - Chat LLM  │ ← General chat
    │ - RAG Chain │ ← Document Q&A
    └──────┬──────┘
           │
    ┌──────▼──────────┐
    │   OpenAI API    │
    │   - Models      │
    │   - Embeddings  │
    └─────────────────┘
```

## 🆕 Version History

### v10.0 FINAL (Current)
- ✅ GPT-5 models added (3 variants)
- ✅ 30+ OpenAI models total
- ✅ Optimized temperature for GPT-5
- ✅ Latest 2025 AI technology

### v9.0 ENHANCED
- ✅ General chat mode (works without documents)
- ✅ Edit, Retry, Copy buttons
- ✅ Auto-initialize on startup
- ✅ Enhanced UI with icon buttons
- ✅ Smooth hover effects
- ✅ Better status indicators

### v4.1 (Previous)
- Memory-only processing
- 13+ file formats
- Hot model switching
- o-series temperature handling

## 🎯 Use Cases

### Without Documents
- **Learning**: Ask about any topic
- **Coding**: Get programming help
- **Writing**: Generate ideas, content
- **Problem-solving**: Brainstorm solutions

### With Documents
- **Research**: Analyze papers, reports
- **Legal**: Review contracts, agreements
- **Business**: Process invoices, reports
- **Education**: Study guides, notes

## 🌐 Model Comparison

| Model | Speed | Quality | Cost | Best For |
|-------|-------|---------|------|----------|
| gpt-5 | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 💰💰💰💰 | Latest tech |
| gpt-5-turbo | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 💰💰💰 | Fast + quality |
| gpt-5-mini | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | 💰💰 | Efficient |
| gpt-4o-mini | ⚡⚡⚡ | ⭐⭐⭐⭐ | 💰 | Most users |
| gpt-4o | ⚡⚡ | ⭐⭐⭐⭐⭐ | 💰💰💰 | Best quality |
| o3-mini | ⚡⚡ | ⭐⭐⭐⭐ | 💰💰 | Reasoning |
| gpt-3.5-turbo | ⚡⚡⚡⚡ | ⭐⭐⭐ | 💰 | Budget |

## 📝 Keyboard Shortcuts

- **Enter** - Send message
- **Shift+Enter** - New line in message
- **Ctrl+C** - Copy (after clicking copy button)

## 🆘 Support

### Common Issues
1. **"API key not found"** → Check .env file
2. **"Module not found"** → Reinstall requirements
3. **Copy not working** → Install clipboard utilities
4. **Slow responses** → Try different model

### Documentation Links
- [OpenAI Models](https://platform.openai.com/docs/models)
- [LangChain Docs](https://python.langchain.com/)
- [Streamlit Docs](https://docs.streamlit.io/)

## 🎉 Credits

**Built with:**
- Streamlit - Web interface
- LangChain - RAG orchestration
- OpenAI - Language models
- FAISS - Vector storage
- Pyperclip - Clipboard functionality

---

## 🚀 Ready to Start!

```bash
# One command to rule them all
streamlit run app.py
```

**TTZ.KT AI Platform v10.0** - Enhanced with GPT-5, General Chat & Better UI 🎨

Chat freely, analyze documents, edit & retry - with the latest GPT-5 AI!
