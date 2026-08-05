import requests
import time
from typing import Dict, Any, Callable, Optional
from src.agentic_blog_generator.llms.groqllm import GroqLLM
from src.agentic_blog_generator.graphs.graphBuilder import GraphBuilder
from config.constants import API_URL

class BlogGeneratorService:
    """
    Service class handling blog generation via direct LangGraph invocation
    or FastAPI backend endpoints.
    """

    @staticmethod
    def generate_blog_direct(
        topic: str,
        language: str,
        blog_length: str,
        step_callback: Optional[Callable[[str, str], None]] = None
    ) -> Dict[str, Any]:
        """
        Execute the LangGraph workflow directly in-process with step progress callbacks.
        """
        start_time = time.time()

        if step_callback:
            step_callback("title", "running")

        # Step 1: Initialize Groq LLM & Graph
        groq_llm = GroqLLM()
        llm = groq_llm.get_llm()
        graph_builder = GraphBuilder(llm)
        compiled_graph = graph_builder.setupGraph()

        initial_state = {
            "topic": topic,
            "current_language": language,
            "blog_length": blog_length
        }

        # Execute title creation & content generation with step tracking
        if step_callback:
            step_callback("title", "active")

        # Stream graph steps if possible, or invoke directly
        final_state = {}
        for event in compiled_graph.stream(initial_state):
            for node_name, node_output in event.items():
                if node_name == "title_creation" and step_callback:
                    step_callback("title", "done")
                    step_callback("content", "active")
                elif node_name == "content_generator" and step_callback:
                    step_callback("content", "done")
                    step_callback("translation", "active")
                elif node_name == "translation" and step_callback:
                    step_callback("translation", "done")
                
                # Update accumulated state
                if isinstance(node_output, dict):
                    final_state.update(node_output)

        elapsed_time = time.time() - start_time
        
        if step_callback:
            step_callback("completed", "done")

        return {
            "title": final_state.get("blog", {}).get("title", ""),
            "content": final_state.get("blog", {}).get("content", ""),
            "elapsed_time": elapsed_time
        }

    @staticmethod
    def generate_blog_api(topic: str, language: str, blog_length: str) -> Dict[str, Any]:
        """
        Call FastAPI backend POST /blogs endpoint.
        """
        start_time = time.time()
        payload = {
            "topic": topic,
            "language": language,
            "blog_length": blog_length
        }

        response = requests.post(API_URL, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()
        data = result.get("data", {})
        blog = data.get("blog", {})

        elapsed_time = time.time() - start_time

        return {
            "title": blog.get("title", ""),
            "content": blog.get("content", ""),
            "elapsed_time": elapsed_time
        }
