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
async def create_blogs(request: Request):
    data = await request.json()
    topic = data.get("topic", "").strip()
    language = data.get("language", "English").strip()
    blog_length = data.get("blog_length", "Medium").strip()

    if not topic:
        return {"error": "Topic is required"}

    # Get LLM Object
    groqllm = GroqLLM()
    llm = groqllm.get_llm()

    # Get the graph
    graph_builder = GraphBuilder(llm)
    graph = graph_builder.setupGraph()

    state = graph.invoke({
        "topic": topic,
        "current_language": language,
        "blog_length": blog_length
    })

    return {"data": state}



if __name__=="__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
