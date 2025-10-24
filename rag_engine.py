import os 
import time     
import tempfile                                         
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain   
from langchain.memory import ConversationBufferMemory      
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

# Document loaders for different formats
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

try:
    from langchain_community.document_loaders import UnstructuredImageLoader
    IMAGE_SUPPORT = True
except ImportError:
    IMAGE_SUPPORT = False


class RAGEngine:
    """
    Multi-Format RAG Engine with General Chat Mode
    ✅ Works with OR without documents
    ✅ Memory-only processing
    ✅ 13+ file formats
    ✅ o-series temperature handling
    """
    
    def __init__(self, openai_api_key, model="gpt-4o-mini"):
        """Initialize RAG Engine with OpenAI API key and model selection"""
        print(f"[RAG Engine] Initializing with model: {model}")
        self.openai_api_key = openai_api_key
        self.model = model
        self.vectorstore = None
        self.chain = None
        self.llm = None
        self.chat_llm = None  # For general chat without documents
        self.memory = None
        self.processed_documents = []
        
        # Use OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=openai_api_key
        )
        
        # Initialize chat LLM immediately for general chat
        self._init_chat_llm()
        
        print("[RAG Engine] Multi-format support enabled")
        print("[RAG Engine] Memory-only processing (no disk storage)")
        print(f"[RAG Engine] Image support: {'✅ Enabled' if IMAGE_SUPPORT else '⚠️ Disabled'}")
        print("[RAG Engine] General chat mode: ✅ Available")
        print("[RAG Engine] Ready!")
    
    def _get_temperature(self, model_name):
        """
        Get the correct temperature for a model.
        - o-series models (o1, o3) require temperature=1
        - GPT-5 models use temperature=0.8 (optimal for latest model)
        - All other models use temperature=0.7
        """
        if model_name.startswith("o1") or model_name.startswith("o3"):
            print(f"[Temperature] Using temperature=1 for reasoning model: {model_name}")
            return 1.0
        elif model_name.startswith("gpt-5"):
            print(f"[Temperature] Using temperature=0.8 for GPT-5: {model_name}")
            return 0.8
        else:
            return 0.7
    
    def _init_chat_llm(self):
        """Initialize LLM for general chat (without documents)"""
        temperature = self._get_temperature(self.model)
        
        self.chat_llm = ChatOpenAI(
            model=self.model,
            temperature=temperature,
            openai_api_key=self.openai_api_key
        )
        print(f"[Chat LLM] Initialized for general chat (temperature={temperature})")
    
    def _chat_direct(self, message):
        """Direct chat without document retrieval"""
        if not self.chat_llm:
            self._init_chat_llm()
        
        try:
            response = self.chat_llm.invoke(message)
            return {
                "answer": response.content,
                "source_documents": []
            }
        except Exception as e:
            print(f"[ERROR] Chat failed: {e}")
            raise
    
    def _detect_file_type(self, file_name):
        """Detect file type based on extension"""
        ext = os.path.splitext(file_name)[1].lower()
        return ext.lstrip('.')
    
    def _load_document_by_type(self, file_path):
        """Load document using appropriate loader based on file type"""
        file_type = self._detect_file_type(file_path)
        file_name = os.path.basename(file_path)
        
        print(f"[Loader] Type: {file_type.upper()} | File: {file_name}")
        
        try:
            # PDF files
            if file_type == 'pdf':
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
            
            # Image files
            elif file_type in ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'gif']:
                if IMAGE_SUPPORT:
                    loader = UnstructuredImageLoader(file_path)
                    return loader.load()
                else:
                    print(f"[Warning] Image support not available. Install 'unstructured[local-inference]' for OCR.")
                    from langchain.schema import Document
                    return [Document(
                        page_content=f"[Image file: {file_name}. Image processing requires additional dependencies.]",
                        metadata={"source": file_name, "type": "image"}
                    )]
            
            # Unsupported format
            else:
                print(f"[Warning] Unsupported file type: {file_type}")
                from langchain.schema import Document
                return [Document(
                    page_content=f"[Unsupported file format: {file_type}]",
                    metadata={"source": file_name, "type": "unsupported"}
                )]
        
        except Exception as e:
            print(f"[Error] Failed to load {file_name}: {str(e)}")
            from langchain.schema import Document
            return [Document(
                page_content=f"[Error loading file: {file_name}]",
                metadata={"source": file_name, "type": "error", "error": str(e)}
            )]
    
    def process_uploaded_file(self, uploaded_file):
        """
        Process a file directly from Streamlit's UploadedFile object
        MEMORY-ONLY: No permanent disk storage
        Creates temporary file, processes it, deletes it immediately
        Returns chunks ready for vectorstore
        """
        file_name = uploaded_file.name
        file_type = self._detect_file_type(file_name)
        
        print(f"[Memory Processing] File: {file_name} | Type: {file_type.upper()}")
        start_time = time.time()
        
        tmp_path = None
        try:
            # Create temporary file (will be deleted after processing)
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp_file:
                # Write uploaded content to temp file
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            print(f"[Memory] Temp file created: {tmp_path}")
            
            # Load document using appropriate loader
            documents = self._load_document_by_type(tmp_path)
            
            # Delete temp file IMMEDIATELY after loading
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
                print(f"[Memory] Temp file deleted: {tmp_path}")
            
            if not documents:
                print(f"[Warning] No content extracted from {file_name}")
                return []
            
            print(f"[Memory Processing] Loaded {len(documents)} section(s) in {time.time() - start_time:.2f}s")
            
            # Split into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            
            chunks = text_splitter.split_documents(documents)
            
            # Update metadata to include original filename
            for chunk in chunks:
                chunk.metadata['source'] = file_name
            
            print(f"[Memory Processing] Created {len(chunks)} chunks from {file_name}")
            
            self.processed_documents.append(file_name)
            return chunks
            
        except Exception as e:
            # Ensure temp file is deleted even on error
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
                print(f"[Memory] Temp file deleted (error cleanup): {tmp_path}")
            
            print(f"[Error] Failed to process {file_name}: {str(e)}")
            raise
    
    def process_document(self, file_path):
        """
        Legacy method - Process a document from file path
        Use process_uploaded_file() for memory-only processing
        """
        print(f"[Processing] Loading: {file_path}")
        start_time = time.time()
        
        try:
            # Load document using appropriate loader
            documents = self._load_document_by_type(file_path)
            
            if not documents:
                print(f"[Warning] No content extracted from {file_path}")
                return []
            
            print(f"[Processing] Loaded {len(documents)} section(s) in {time.time() - start_time:.2f}s")
            
            # Split into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            
            chunks = text_splitter.split_documents(documents)
            print(f"[Processing] Created {len(chunks)} chunks")
            
            self.processed_documents.append(os.path.basename(file_path))
            return chunks
            
        except Exception as e:
            print(f"[Error] Failed to process {file_path}: {str(e)}")
            raise
    
    def create_vectorstore(self, chunks):
        """Create FAISS vectorstore from document chunks"""
        print(f"[Vectorstore] Creating from {len(chunks)} chunks...")
        start_time = time.time()
        
        try:
            if not chunks:
                raise ValueError("No chunks provided for vectorstore creation")
            
            self.vectorstore = FAISS.from_documents(
                documents=chunks,
                embedding=self.embeddings
            )
            print(f"[Vectorstore] Created in {time.time() - start_time:.2f}s")
            print(f"[Vectorstore] Total vectors: {self.vectorstore.index.ntotal}")
            print(f"[Vectorstore] Storage: Memory only (no disk files)")
            
        except Exception as e:
            print(f"[Error] Failed to create vectorstore: {str(e)}")
            raise
    
    def setup_chain(self):
        """Setup the conversational retrieval chain with current model"""
        if not self.vectorstore:
            raise ValueError("Vectorstore not initialized. Process documents first.")
        
        print(f"[Chain] Setting up conversational chain with model: {self.model}...")
        
        try:
            # Get correct temperature for this model
            temperature = self._get_temperature(self.model)
            
            # Initialize LLM with current model and appropriate temperature
            self.llm = ChatOpenAI(
                model=self.model,
                temperature=temperature,
                openai_api_key=self.openai_api_key
            )
            
            # Setup memory
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="answer"
            )
            
            # Create retrieval chain
            self.chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vectorstore.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 4}
                ),
                memory=self.memory,
                return_source_documents=True,
                verbose=False
            )
            
            print(f"[Chain] Ready with {self.model} (temperature={temperature})!")
            
        except Exception as e:
            print(f"[Error] Failed to setup chain: {str(e)}")
            raise
    
    def switch_model(self, new_model):
        """
        Switch to a different OpenAI model without reprocessing documents
        Updates both chat LLM and RAG LLM (if documents loaded)
        Automatically uses correct temperature for the model
        """
        print(f"[Model Switch] Switching from {self.model} to {new_model}...")
        old_model = self.model
        self.model = new_model
        
        try:
            # Get correct temperature for new model
            temperature = self._get_temperature(new_model)
            
            # Update chat LLM (always available for general chat)
            self.chat_llm = ChatOpenAI(
                model=new_model,
                temperature=temperature,
                openai_api_key=self.openai_api_key
            )
            print(f"[Model Switch] Chat LLM updated (temperature={temperature})")
            
            # Update RAG LLM only if documents are loaded
            if self.vectorstore:
                self.llm = ChatOpenAI(
                    model=new_model,
                    temperature=temperature,
                    openai_api_key=self.openai_api_key
                )
                
                # Ensure memory exists
                if not self.memory:
                    self.memory = ConversationBufferMemory(
                        memory_key="chat_history",
                        return_messages=True,
                        output_key="answer"
                    )
                
                # Recreate chain with new LLM (keeps same vectorstore and memory)
                self.chain = ConversationalRetrievalChain.from_llm(
                    llm=self.llm,
                    retriever=self.vectorstore.as_retriever(
                        search_type="similarity",
                        search_kwargs={"k": 4}
                    ),
                    memory=self.memory,
                    return_source_documents=True,
                    verbose=False
                )
                print(f"[Model Switch] RAG chain updated")
            
            print(f"[Model Switch] Successfully switched to {new_model} (temperature={temperature})!")
            
        except Exception as e:
            # Rollback to old model if switch fails
            print(f"[Error] Failed to switch model: {str(e)}")
            self.model = old_model
            raise
    
    def ask_question(self, question):
        """
        Ask a question - works with OR without documents
        - If documents loaded: Uses RAG chain for document-aware responses
        - If no documents: Uses direct chat for general conversation
        """
        print(f"\n{'='*60}")
        print(f"[QUERY] {question}")
        print(f"{'='*60}")
        
        total_start = time.time()
        
        try:
            # If no documents loaded, use direct chat
            if not self.chain:
                print("[INFO] No documents loaded - using general chat mode")
                return self._chat_direct(question)
            
            # When documents ARE loaded, use RAG chain
            response = self.chain.invoke({"question": question})
            
            total_time = time.time() - total_start
            
            sources = response.get("source_documents", [])
            print(f"\n[INFO] Retrieved {len(sources)} chunks in {total_time:.2f}s")
            print(f"[INFO] Total response time: {total_time:.2f}s")
            
            # Show what was retrieved (for debugging)
            for i, doc in enumerate(sources, 1):
                preview = doc.page_content[:150].replace('\n', ' ')
                print(f"  Chunk {i}: {preview}...")
            
            print(f"{'='*60}\n")
            
            return {
                "answer": response["answer"],
                "source_documents": sources
            }
            
        except Exception as e:
            print(f"[ERROR] Query failed: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def clear_documents(self):
        """Clear all processed documents and vectorstore (keeps chat LLM for general chat)"""
        self.vectorstore = None
        self.chain = None
        self.llm = None
        self.memory = None
        self.processed_documents = []
        print("[RAG Engine] All documents cleared (memory freed)")
        print("[RAG Engine] General chat mode still available")
    
    def get_stats(self):
        """Get current system statistics"""
        return {
            "model": self.model,
            "documents_processed": len(self.processed_documents),
            "vectorstore_size": self.vectorstore.index.ntotal if self.vectorstore else 0,
            "chain_ready": self.chain is not None,
            "chat_ready": self.chat_llm is not None,
            "storage_type": "memory_only"
        }
    
    def get_supported_formats(self):
        """Get list of supported file formats"""
        return {
            "documents": ["pdf", "docx", "doc", "txt", "rtf", "md"],
            "spreadsheets": ["csv", "xlsx", "xls", "ods"],
            "images": ["png", "jpg", "jpeg", "bmp", "tiff", "gif"] if IMAGE_SUPPORT else [],
            "data": ["json", "xml", "yaml", "yml"]
        }
