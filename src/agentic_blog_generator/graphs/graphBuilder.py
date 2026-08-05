from langgraph.graph import StateGraph, START, END
from src.agentic_blog_generator.llms.groqllm import GroqLLM
from src.agentic_blog_generator.states.blogState import BlogState
from src.agentic_blog_generator.nodes.blogNode import BlogNode

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)

    def build_graph(self):
        """
        Build a linear agentic graph for blog generation:
        START -> Title Creation -> Content Generation -> Dynamic Translation -> END
        """
        self.obj_blogNode = BlogNode(self.llm)

        # Nodes
        self.graph.add_node("title_creation", self.obj_blogNode.title_creation)
        self.graph.add_node("content_generator", self.obj_blogNode.content_generation)
        self.graph.add_node("translation", self.obj_blogNode.translation)

        # Edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generator")
        self.graph.add_edge("content_generator", "translation")
        self.graph.add_edge("translation", END)

        return self.graph

    def build_topic_graph(self):
        return self.build_graph()

    def build_language_graph(self):
        return self.build_graph()

    def setupGraph(self, usecase="language"):
        self.build_graph()
        return self.graph.compile()

# Below code is for LangSmith & LangGraph Studio
try:
    llm = GroqLLM().get_llm()
    graph_builder = GraphBuilder(llm)
    graph = graph_builder.build_graph().compile()
except Exception:
    graph = None