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

        self.obj_blogNode = BlogNode(self.llm)

        #Nodes
        self.graph.add_node("title_creation",self.obj_blogNode.title_creation)
        self.graph.add_node("content_generator", self.obj_blogNode.content_generation)

        #Edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generator")
        self.graph.add_edge("content_generator", END)

        return self.graph

    def build_language_graph(self):
        """
        Build a graph for blog generation with inputs topic and language
        """

        self.obj_blogNode = BlogNode(self.llm)
        
        #Nodes
        self.graph.add_node("title_creation",self.obj_blogNode.title_creation)
        self.graph.add_node("content_generator", self.obj_blogNode.content_generation)
        # self.graph.add_node("hindi_translation",lambda state: self.obj_blogNode.translation({**state, "current_language": "hindi"}))
        self.graph.add_node("hindi_translation",self.obj_blogNode.translation)
        self.graph.add_node("french_translation",self.obj_blogNode.translation)
        # self.graph.add_node("french_translation",lambda state: self.obj_blogNode.translation({**state, "current_language":"french"}))
        self.graph.add_node("route",self.obj_blogNode.route)

        #Edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generator")
        self.graph.add_edge("content_generator", "route")

        #Conditional Edge
        self.graph.add_conditional_edges(
            "route",
            self.obj_blogNode.route_decision,
            {
                "hindi":"hindi_translation",
                "french":"french_translation"
            }
        )

        self.graph.add_edge("hindi_translation",END)
        self.graph.add_edge("french_translation",END)
        return self.graph


    def setupGraph(self, usecase):
        if usecase == "topic":
            self.build_topic_graph()
        if usecase=="language":
            print("Language block")
            self.build_language_graph()

        return self.graph.compile()

# Below code is for Lamgsmith & Langgraph Studio
llm = GroqLLM().get_llm()

graph_builder = GraphBuilder(llm)
graph=graph_builder.build_language_graph().compile()