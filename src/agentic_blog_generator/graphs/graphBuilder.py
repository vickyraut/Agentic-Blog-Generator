from langgraph.graph import StateGraph, START, END
from src.agentic_blog_generator.llms.groqllm import GroqLLM
from src.agentic_blog_generator.states.blogState import BlogState

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm;
        self.graph = StateGraph(BlogState)

    def build_topic_graph(self):
        """
        Build a graph to generate blogss based on topic
        """

        #Nodes
        self.graph.add_node("title_creation",)
        self.graph.add_node("content_generator",)

        #Edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generator")
        self.graph.add_edge("content_generator", END)

        return self.graph

    

