import os
from google.generativeai import GenerativeModel
from dotenv import load_dotenv
from langchain.llms import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()
os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")

llm=ChatGoogleGenerativeAI(
    model_name="gemini-2.5-pro",
    temperature=0.5,
)

system_prompt="""
Takes a question as input, sends it to the AI model,
    and returns the model's reply.
"""

prompt=PromptTemplate(
    input_variables=["question"],
    template=system_prompt
)

chain=LLMChain(
    llm=llm,
    prompt=prompt
)

def ask_ai(question):
    """
    Takes a question as input, sends it to the AI model,
    and returns the model's reply.
    """
    return chain.run(question)

