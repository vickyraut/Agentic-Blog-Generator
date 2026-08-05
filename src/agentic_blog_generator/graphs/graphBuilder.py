from langgraph.graph import StateGraph, START, END
from src.agentic_blog_generator.llms.groqllm import GroqLLM
from src.agentic_blog_generator.states.blogState import BlogState
from src.agentic_blog_generator.nodes.blogNode import BlogNode

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm;
        self.graph = StateGraph(BlogState)

    def build_topic_graph(self):
        """
        Build a graph to generate blogss based on topic
        """

        obj_blogNode = BlogNode(self.llm)

        #Nodes
        self.graph.add_node("title_creation",obj_blogNode.title_creation)
        self.graph.add_node("content_generator", obj_blogNode.content_generation)

        #Edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generator")
        self.graph.add_edge("content_generator", END)

        return self.graph

    def setupGraph(self, usecase):
        if usecase == "topic":
            self.build_topic_graph()

        return self.graph.compile()

# Below code is for Lamgsmith & Langgraph Studio
llm = GroqLLM().get_llm()

graph_builder = GraphBuilder(llm)
graph=graph_builder.build_topic_graph().compile()