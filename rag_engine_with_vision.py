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
    
    def __init__(self, openai_api_key, model="gpt-4o-mini", vision_model="gpt-4o-mini"):
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
        
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=openai_api_key
        )
        
        self.vision_llm = ChatOpenAI(
            model=vision_model,
            openai_api_key=openai_api_key,
            max_tokens=1000
        )
        
        temperature = self._get_temperature(model)
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            openai_api_key=openai_api_key
        )
        
        print("[RAG Engine] ✅ Ready with vision support!")
        print("[RAG Engine] ✅ General chat mode enabled!")
    
    def _get_temperature(self, model_name):
        if model_name.startswith("o3") or model_name.startswith("o4"):
            return 1.0
        return 0.7
    
    def _detect_file_type(self, file_name):
        ext = os.path.splitext(file_name)[1].lower()
        return ext.lstrip('.')
    
    def _is_image_file(self, file_type):
        return file_type in ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'tiff']
    
    def _process_image_with_vision(self, image_bytes, file_name):
        print(f"[Vision] Analyzing image: {file_name}")
        start_time = time.time()
        
        try:
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            
            file_type = self._detect_file_type(file_name)
            mime_type = f"image/{file_type if file_type != 'jpg' else 'jpeg'}"
            
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
            
            response = self.vision_llm.invoke([message])
            description = response.content
            
            elapsed = time.time() - start_time
            print(f"[Vision] ✅ Analyzed in {elapsed:.2f}s")
            print(f"[Vision] Extracted {len(description)} chars of description")
            
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
            return Document(
                page_content=f"[IMAGE: {file_name} - Could not process]",
                metadata={"source": file_name, "type": "image", "error": str(e)}
            )
    
    def _load_document_by_type(self, file_path, file_bytes=None):
        file_type = self._detect_file_type(file_path)
        file_name = os.path.basename(file_path)
        
        print(f"[Loader] {file_type.upper()}: {file_name}")
        
        try:
            if self._is_image_file(file_type):
                if file_bytes:
                    return [self._process_image_with_vision(file_bytes, file_name)]
                else:
                    with open(file_path, 'rb') as f:
                        image_bytes = f.read()
                    return [self._process_image_with_vision(image_bytes, file_name)]
            
            elif file_type == 'pdf':
                loader = PyPDFLoader(file_path)
                return loader.load()
            
            elif file_type in ['docx', 'doc']:
                loader = Docx2txtLoader(file_path)
                return loader.load()
            
            elif file_type in ['txt', 'md']:
                loader = TextLoader(file_path, encoding='utf-8')
                return loader.load()
            
            elif file_type == 'rtf':
                loader = UnstructuredRTFLoader(file_path)
                return loader.load()
            
            elif file_type == 'csv':
                loader = CSVLoader(file_path, encoding='utf-8')
                return loader.load()
            
            elif file_type in ['xlsx', 'xls', 'ods']:
                loader = UnstructuredExcelLoader(file_path, mode="elements")
                return loader.load()
            
            elif file_type == 'json':
                loader = JSONLoader(
                    file_path=file_path,
                    jq_schema='.',
                    text_content=False
                )
                return loader.load()
            
            elif file_type == 'xml':
                loader = UnstructuredXMLLoader(file_path)
                return loader.load()
            
            elif file_type in ['yaml', 'yml']:
                loader = TextLoader(file_path, encoding='utf-8')
                return loader.load()
            
            else:
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
        file_name = uploaded_file.name
        file_type = self._detect_file_type(file_name)
        
        print(f"[Memory Processing] {file_name} | {file_type.upper()}")
        start_time = time.time()
        
        tmp_path = None
        try:
            if self._is_image_file(file_type):
                image_bytes = uploaded_file.getvalue()
                documents = [self._process_image_with_vision(image_bytes, file_name)]
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                documents = self._load_document_by_type(tmp_path)
                
                if tmp_path and os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                    tmp_path = None
            
            if not documents:
                print(f"[Warning] No content extracted from {file_name}")
                return []
            
            if self._is_image_file(file_type):
                chunks = documents
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
                search_kwargs={"k": 6}
            ),
            memory=self.memory,
            return_source_documents=True,
            verbose=False
        )
        
        print(f"[Chain] ✅ Ready (temperature={temperature})!")
    
    def switch_model(self, new_model):
        print(f"[Model Switch] {self.model} → {new_model}")
        
        old_model = self.model
        self.model = new_model
        temperature = self._get_temperature(new_model)
        
        try:
            self.llm = ChatOpenAI(
                model=new_model,
                temperature=temperature,
                openai_api_key=self.openai_api_key
            )
            
            if self.vectorstore:
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
            
            print(f"[Model Switch] ✅ Switched to {new_model}")
            
        except Exception as e:
            self.model = old_model
            print(f"[Model Switch] ❌ Failed: {str(e)}")
            raise
    
    def ask_question(self, question):
        print(f"[Query] {question}")
        start_time = time.time()
        
        try:
            if not self.vectorstore or not self.chain:
                print(f"[Mode] General Chat (no documents)")
                
                if not self.llm:
                    raise ValueError("LLM not initialized")
                
                from langchain_core.messages import HumanMessage
                response = self.llm.invoke([HumanMessage(content=question)])
                
                elapsed = time.time() - start_time
                print(f"[Query] ✅ Answered in {elapsed:.2f}s (general chat)")
                
                return {
                    "answer": response.content,
                    "source_documents": [],
                    "mode": "general_chat"
                }
            
            else:
                print(f"[Mode] RAG (using {len(self.processed_documents)} documents)")
                
                response = self.chain.invoke({"question": question})
                
                elapsed = time.time() - start_time
                print(f"[Query] ✅ Answered in {elapsed:.2f}s (RAG mode)")
                
                return {
                    "answer": response["answer"],
                    "source_documents": response.get("source_documents", []),
                    "mode": "rag"
                }
            
        except Exception as e:
            print(f"[Error] Query failed: {str(e)}")
            raise
    
    def clear_documents(self):
        self.vectorstore = None
        self.chain = None
        self.memory = None
        self.processed_documents = []
        print("[RAG Engine] ✅ Documents cleared (general chat still available)")
    
    def get_stats(self):
        return {
            "model": self.model,
            "vision_model": self.vision_model,
            "documents_processed": len(self.processed_documents),
            "vectorstore_size": self.vectorstore.index.ntotal if self.vectorstore else 0,
            "chain_ready": self.chain is not None,
            "general_chat_ready": self.llm is not None,
            "vision_enabled": True
        }
    
    def get_supported_formats(self):
        return {
            "documents": ["pdf", "docx", "doc", "txt", "rtf", "md"],
            "spreadsheets": ["csv", "xlsx", "xls", "ods"],
            "images": ["png", "jpg", "jpeg", "bmp", "gif", "webp", "tiff"],
            "data": ["json", "xml", "yaml", "yml"]
        }
