from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from pathlib import Path
import os
import sys

PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))
from src.components import client, llm, embeddings, TRANSACTION_COLLECTION, llm_gpt_4
from chatbot.ingest import vector_store_transactions, ATLAS_VECTOR_SEARCH_INDEX_NAME

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

def answer_question_from_context(context: str, question: str):
    """
    Function to answer a question based purely on the provided context using LangChain.
    
    Args:
        context (str): The context string that provides information.
        question (str): The question to be answered based on the context.

    Returns:
        str: The answer generated by the LLM based on the context.
    """

    # Define the prompt template
    prompt_template = PromptTemplate.from_template(
    """Given the following context:
    {context}
    
    You are a highly professional and courteous assistant. You always greet the user warmly and respond in a structured and polite manner.  
    Carefully analyze all the provided context before answering the question. Ensure that your response is based solely on the given information.  
    If the requested information is not available in the context, kindly say,  
    "I'm sorry, but I don't have that information at the moment."  

    The transactions provided to you are only for the last two months, **January and February 2025**.  
    If the user asks about transactions from any other months, kindly respond with:  
    *"I was developed by CQAI Engineers as a demo product in February 2025. The transactions I have access to are only for the last two months, January and February 2025. Please ask me about these months, as I do not have records for other periods."*  

    If the user inquires about savings plans, cards, or loans, politely provide a brief response using "I recommend" instead of "You are eligible." Additionally, kindly guide them to visit the specific section from the left panel of the platform to check their eligibility and book the product.  

    Please note that dates are provided in the format YYYY-MM-DD.  

    Question: {question}  
    Answer:  
    """
)


    # Convert prompt template into a runnable sequence
    chain = prompt_template | llm_gpt_4

    # Invoke the chain with correct inputs
    answer = chain.invoke({"context": context, "question": question})

    return answer
