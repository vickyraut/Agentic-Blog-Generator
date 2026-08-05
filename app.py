import uvicorn
from fastapi import FastAPI, Request
from src.agentic_blog_generator.llms.groqllm import GroqLLM
from src.agentic_blog_generator.graphs.graphBuilder import GraphBuilder

import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

## APIs
@app.post("/blogs")
async def create_blogs(request:Request):
    data = await request.json()
    topic = data.get("topic", "")

    # Get LLM Object

    groqllm = GroqLLM()
    llm = groqllm.get_llm()

    # Get the graph
    graph_buider = GraphBuilder(llm)
    if topic:
        graph = graph_buider.setupGraph(usecase="topic")
        state  = graph.invoke({"topic":topic})

    return {"data": state}


if __name__=="__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
