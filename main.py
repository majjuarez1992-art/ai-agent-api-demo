from dotenv import load_dotenv
from google import genai 
from typing import TypedDict
import re 
from langgraph.graph import StateGraph, START, END

#Fast Api
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
client=genai.Client()
app=FastAPI()

class AgentRequest(BaseModel):
    question: str
    
class AgentState(TypedDict):
    question: str
    component_id: int | None
    component_status: dict | None
    answer: str | None

def ask_llm(question: str)-> str:
    interaction= client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=question
    )
    return interaction.output_text

def get_component_status( component_id:int)->dict:
    return {
        "component_id":component_id,
        "status":"warning",
        "quality":72 }
    
def create_initial_state(question: str) -> AgentState:
    return{
        "question": question,
        "component_id": extract_component_id(question),
        "component_status": None,
        "answer": None
    }

def agent_node(state: AgentState) -> dict:
    if state["component_status"] is None:
        prompt = state["question"]
    else:
        prompt = f"""
        Pregunta del usuario: {state["question"]}

        Resultado de la herramienta:
        {state["component_status"]}

        Responde al usuario utilizando el resultado de la herramienta.
        """

    answer = ask_llm(prompt)

    return {"answer": answer}
    
def tool_node(state:AgentState)->dict:
    component_id=state["component_id"]
    if component_id is None:
        raise ValueError("component_id is required")
    resultado=get_component_status(component_id)
    return {"component_status": resultado}

def extract_component_id(question: str) -> int |None:
    component_id=re.search(r"\d+", question)
    if component_id:
        return int(component_id.group())
    return None

def route_initial(state: AgentState) -> str:
    if state["component_id"] is not None:
        return "tool"
    return "agent"

graph_builder=StateGraph(AgentState)
graph_builder.add_node("agent",agent_node)
graph_builder.add_node("tool",tool_node)

graph_builder.add_conditional_edges(
    START,
    route_initial,
    {
        "tool": "tool",
        "agent": "agent"
    }
)

graph_builder.add_edge("tool", "agent")
graph_builder.add_edge("agent", END)

graph = graph_builder.compile()

@app.post("/agent/query")
def query_agent(request: AgentRequest):
    initial_state = create_initial_state(request.question)
    return graph.invoke(initial_state)
# initial_state= create_initial_state("¿Qué diferencia hay entre un LLM y un AI agent?")
# result=graph.invoke(initial_state)
# print (result)