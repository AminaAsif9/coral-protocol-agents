"""
LLM utility functions for the ClimeAI agent.
"""
import os
from typing import List, Optional
from langchain_core.tools import BaseTool
from langchain_core.language_models import BaseLanguageModel
from langchain_community.chat_models.fake import FakeListChatModel
from langchain_core.messages import AIMessage

# Import different LLM providers based on availability
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    GOOGLE_GENAI_AVAILABLE = True
except ImportError:
    GOOGLE_GENAI_AVAILABLE = False

try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    from langchain_mistralai import ChatMistralAI
    MISTRAL_AVAILABLE = True
except ImportError:
    MISTRAL_AVAILABLE = False

def get_llm_instance_with_tools(tools: Optional[List[BaseTool]] = None) -> BaseLanguageModel:
    """
    Get an LLM instance with tools bound to it.
    
    Args:
        tools: List of LangChain tools to bind to the LLM
        
    Returns:
        An LLM instance with tools bound
    """
    # Try to get API keys for different providers
    google_api_key = os.getenv("GOOGLE_API_KEY")
    groq_api_key = os.getenv("GROQ_API_KEY")
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    
    # Try to initialize LLMs in order of preference
    if GOOGLE_GENAI_AVAILABLE and google_api_key:
        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)
        # For Google's Gemini, we need to use the tools parameter
        if tools:
            llm = llm.bind(tools=tools)
        return llm
    
    if GROQ_AVAILABLE and groq_api_key:
        llm = ChatGroq(model_name="llama3-70b-8192", api_key=groq_api_key)
        # For Groq, we need to use the tools parameter
        if tools:
            llm = llm.bind(tools=tools)
        return llm
    
    if MISTRAL_AVAILABLE and mistral_api_key:
        llm = ChatMistralAI(model="mistral-large-latest", mistral_api_key=mistral_api_key)
        # For Mistral, we need to use the tools parameter
        if tools:
            llm = llm.bind(tools=tools)
        return llm
    
    # Fallback to a fake LLM for testing
    return FakeListChatModel(responses=[AIMessage(content="This is a test response from a fake LLM.")])
