import os
import time
import tempfile
import base64
from io import BytesIO
from PIL import Image

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document

# Document loaders
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    CSVLoader,
    UnstructuredExcelLoader,
    JSONLoader,
    UnstructuredXMLLoader,
    UnstructuredRTFLoader
)


class RAGEngineWithVision:
    """RAG Engine with TRUE image understanding via vision models"""
    
    def __init__(self, openai_api_key, model="gpt-4o-mini", vision_model="gpt-4o-mini"):
        """
        Initialize RAG Engine with vision support
        
        Args:
            openai_api_key: Your OpenAI API key
            model: Model for text Q&A (gpt-4o-mini, gpt-4o, etc.)
            vision_model: Model for image understanding (must support vision)
        """
        print(f"[RAG Engine] Initializing...")
        print(f"[RAG Engine] Text Model: {model}")
        print(f"[RAG Engine] Vision Model: {vision_model}")
        
        self.openai_api_key = openai_api_key
        self.model = model
        self.vision_model = vision_model
        self.vectorstore = None
        self.chain = None
        self.llm = None
        self.memory = None
        self.processed_documents = []
        
        # Main embeddings for text
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=openai_api_key
        )
        
        # Vision model for image understanding
        self.vision_llm = ChatOpenAI(
            model=vision_model,
            openai_api_key=openai_api_key,
            max_tokens=1000
        )
        
        print("[RAG Engine] ✅ Ready with vision support!")
    
    def _get_temperature(self, model_name):
        """Get appropriate temperature for model"""
        if model_name.startswith("o3") or model_name.startswith("o4"):
            return 1.0
        return 0.7
    
    def _detect_file_type(self, file_name):
        """Detect file type from extension"""
        ext = os.path.splitext(file_name)[1].lower()
        return ext.lstrip('.')
    
    def _is_image_file(self, file_type):
        """Check if file is an image"""
        return file_type in ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'tiff']
    
    def _process_image_with_vision(self, image_bytes, file_name):
        """
        Process image using vision model to extract meaningful content
        This is the KEY improvement - actually understands images!
        """
        print(f"[Vision] Analyzing image: {file_name}")
        start_time = time.time()
        
        try:
            # Convert to base64
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            
            # Determine image format
            file_type = self._detect_file_type(file_name)
            mime_type = f"image/{file_type if file_type != 'jpg' else 'jpeg'}"
            
            # Ask vision model to describe the image in detail
            prompt = """Analyze this image in detail and provide:

1. **Main Content**: What is the primary subject or purpose of this image?
2. **Text Content**: Any text, labels, captions, or written information visible
3. **Key Details**: Important visual elements, data, diagrams, or information
4. **Context**: What type of document/image is this (chart, diagram, photo, screenshot, etc.)

Be thorough and specific so this description can be used to answer questions about the image."""

            from langchain_core.messages import HumanMessage
            
            message = HumanMessage(
                content=[
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    }
                ]
            )
            
            # Get vision model's analysis
            response = self.vision_llm.invoke([message])
            description = response.content
            
            elapsed = time.time() - start_time
            print(f"[Vision] ✅ Analyzed in {elapsed:.2f}s")
            print(f"[Vision] Extracted {len(description)} chars of description")
            
            # Create document with the vision model's description
            return Document(
                page_content=f"[IMAGE: {file_name}]\n\n{description}",
                metadata={
                    "source": file_name,
                    "type": "image",
                    "processed_with": "vision_model"
                }
            )
            
        except Exception as e:
            print(f"[Vision] ⚠️ Error processing {file_name}: {str(e)}")
            # Fallback to basic placeholder
            return Document(
                page_content=f"[IMAGE: {file_name} - Could not process]",
                metadata={"source": file_name, "type": "image", "error": str(e)}
            )
    
    def _load_document_by_type(self, file_path, file_bytes=None):
        """Load document using appropriate loader"""
        file_type = self._detect_file_type(file_path)
        file_name = os.path.basename(file_path)
        
        print(f"[Loader] {file_type.upper()}: {file_name}")
        
        try:
            # IMAGE FILES - Use vision model!
            if self._is_image_file(file_type):
                if file_bytes:
                    return [self._process_image_with_vision(file_bytes, file_name)]
                else:
                    # Read from file path
                    with open(file_path, 'rb') as f:
                        image_bytes = f.read()
                    return [self._process_image_with_vision(image_bytes, file_name)]
            
            # PDF files
            elif file_type == 'pdf':
                loader = PyPDFLoader(file_path)
                return loader.load()
            
            # Word documents
            elif file_type in ['docx', 'doc']:
                loader = Docx2txtLoader(file_path)
                return loader.load()
            
            # Text files
            elif file_type in ['txt', 'md']:
                loader = TextLoader(file_path, encoding='utf-8')
                return loader.load()
            
            # RTF files
            elif file_type == 'rtf':
                loader = UnstructuredRTFLoader(file_path)
                return loader.load()
            
            # CSV files
            elif file_type == 'csv':
                loader = CSVLoader(file_path, encoding='utf-8')
                return loader.load()
            
            # Excel files
            elif file_type in ['xlsx', 'xls', 'ods']:
                loader = UnstructuredExcelLoader(file_path, mode="elements")
                return loader.load()
            
            # JSON files
            elif file_type == 'json':
                loader = JSONLoader(
                    file_path=file_path,
                    jq_schema='.',
                    text_content=False
                )
                return loader.load()
            
            # XML files
            elif file_type == 'xml':
                loader = UnstructuredXMLLoader(file_path)
                return loader.load()
            
            # YAML files
            elif file_type in ['yaml', 'yml']:
                loader = TextLoader(file_path, encoding='utf-8')
                return loader.load()
            
            # Unsupported format
            else:
                print(f"[Warning] Unsupported file type: {file_type}")
                return [Document(
                    page_content=f"[Unsupported file format: {file_type}]",
                    metadata={"source": file_name, "type": "unsupported"}
                )]
        
        except Exception as e:
            print(f"[Error] Failed to load {file_name}: {str(e)}")
            return [Document(
                page_content=f"[Error loading file: {file_name}]",
                metadata={"source": file_name, "type": "error", "error": str(e)}
            )]
    
    def process_uploaded_file(self, uploaded_file):
        """
        Process uploaded file with VISION SUPPORT for images
        Memory-only: no permanent disk storage
        """
        file_name = uploaded_file.name
        file_type = self._detect_file_type(file_name)
        
        print(f"\n[Processing] {file_name} ({file_type.upper()})")
        start_time = time.time()
        
        tmp_path = None
        try:
            # Get file bytes
            file_bytes = uploaded_file.getvalue()
            
            # For images, process directly with vision (no temp file needed)
            if self._is_image_file(file_type):
                documents = [self._process_image_with_vision(file_bytes, file_name)]
            else:
                # For other files, create temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp_file:
                    tmp_file.write(file_bytes)
                    tmp_path = tmp_file.name
                
                # Load with appropriate loader
                documents = self._load_document_by_type(tmp_path)
                
                # Delete temp file immediately
                if tmp_path and os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                    tmp_path = None
            
            if not documents:
                print(f"[Warning] No content extracted from {file_name}")
                return []
            
            # Split into chunks (images get one chunk, text gets split)
            if self._is_image_file(file_type):
                chunks = documents  # Keep image description as one chunk
                print(f"[Processing] Image processed as 1 chunk")
            else:
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1200,
                    chunk_overlap=300,
                    length_function=len,
                    separators=["\n\n", "\n", " ", ""]
                )
                chunks = text_splitter.split_documents(documents)
                print(f"[Processing] Split into {len(chunks)} chunks")
            
            # Update metadata
            for chunk in chunks:
                chunk.metadata['source'] = file_name
            
            elapsed = time.time() - start_time
            print(f"[Processing] ✅ Completed in {elapsed:.2f}s\n")
            
            self.processed_documents.append(file_name)
            return chunks
            
        except Exception as e:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
            print(f"[Error] Failed to process {file_name}: {str(e)}")
            raise
    
    def create_vectorstore(self, chunks):
        """Create FAISS vectorstore from chunks"""
        print(f"[Vectorstore] Creating from {len(chunks)} chunks...")
        start_time = time.time()
        
        if not chunks:
            raise ValueError("No chunks provided")
        
        self.vectorstore = FAISS.from_documents(
            documents=chunks,
            embedding=self.embeddings
        )
        
        elapsed = time.time() - start_time
        print(f"[Vectorstore] ✅ Created in {elapsed:.2f}s")
        print(f"[Vectorstore] Total vectors: {self.vectorstore.index.ntotal}")
    
    def setup_chain(self):
        """Setup conversational retrieval chain"""
        if not self.vectorstore:
            raise ValueError("Vectorstore not initialized")
        
        print(f"[Chain] Setting up with {self.model}...")
        
        temperature = self._get_temperature(self.model)
        
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=temperature,
            openai_api_key=self.openai_api_key
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 6}  # Retrieve more chunks for better context
            ),
            memory=self.memory,
            return_source_documents=True,
            verbose=False
        )
        
        print(f"[Chain] ✅ Ready (temperature={temperature})!")
    
    def switch_model(self, new_model):
        """Switch to different model without reprocessing"""
        if not self.vectorstore:
            raise ValueError("No documents processed yet")
        
        print(f"[Model Switch] {self.model} → {new_model}")
        
        temperature = self._get_temperature(new_model)
        
        self.llm = ChatOpenAI(
            model=new_model,
            temperature=temperature,
            openai_api_key=self.openai_api_key
        )
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 6}
            ),
            memory=self.memory,
            return_source_documents=True,
            verbose=False
        )
        
        self.model = new_model
        print(f"[Model Switch] ✅ Switched to {new_model}")
    
    def ask_question(self, question):
        """Ask question and get answer with sources"""
        if not self.chain:
            raise ValueError("Chain not initialized")
        
        print(f"[Query] {question}")
        start_time = time.time()
        
        try:
            response = self.chain.invoke({"question": question})
            elapsed = time.time() - start_time
            
            print(f"[Query] ✅ Answered in {elapsed:.2f}s")
            
            return {
                "answer": response["answer"],
                "source_documents": response.get("source_documents", [])
            }
            
        except Exception as e:
            print(f"[Error] Query failed: {str(e)}")
            raise
    
    def clear_documents(self):
        """Clear all processed documents"""
        self.vectorstore = None
        self.chain = None
        self.llm = None
        self.memory = None
        self.processed_documents = []
        print("[RAG Engine] ✅ All documents cleared")
    
    def get_stats(self):
        """Get system statistics"""
        return {
            "model": self.model,
            "vision_model": self.vision_model,
            "documents_processed": len(self.processed_documents),
            "vectorstore_size": self.vectorstore.index.ntotal if self.vectorstore else 0,
            "chain_ready": self.chain is not None,
            "vision_enabled": True
        }
    
    def get_supported_formats(self):
        """Get list of supported formats"""
        return {
            "documents": ["pdf", "docx", "doc", "txt", "rtf", "md"],
            "spreadsheets": ["csv", "xlsx", "xls", "ods"],
            "images": ["png", "jpg", "jpeg", "bmp", "gif", "webp", "tiff"],  # Now FULLY supported!
            "data": ["json", "xml", "yaml", "yml"]
        }
