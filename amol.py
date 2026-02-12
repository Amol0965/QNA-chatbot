from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Optional LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Initialize FastAPI app
app = FastAPI(title="Qwen3 Chatbot API")

# Request body model
class QuestionRequest(BaseModel):
    question: str

# Create Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries."),
        ("user", "Question: {question}")
    ]
)

# Load Ollama Model (Qwen3 4B)
llm = Ollama(model="qwen3:4b")

# Output parser
output_parser = StrOutputParser()

# Create chain
chain = prompt | llm | output_parser


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Qwen3 FastAPI chatbot is running"}


# Chat endpoint
@app.post("/ask")
def ask_question(request: QuestionRequest):
    response = chain.invoke({"question": request.question})
    return {"response": response}
