from src.agentic_blog_generator.states.blogState import Blog, BlogState
from langchain_core.messages import HumanMessage

class BlogNode:
    """
    A class fot representing blog Node
    """

    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state:BlogState):
        """
        create the title for the blog
        """

        if "topic" in state and state["topic"]:
            prompt="""
                   You are an expert blog content writer. Use Markdown formatting. Generate
                   a blog title for the {topic}. This title should be creative and SEO friendly
        
                   """

            sytem_message = prompt.format(topic=state["topic"])
            print(sytem_message)
            response=self.llm.invoke(sytem_message)
            print(response)
            return {"blog":{"title":response.content}}

    def content_generation(self, state:BlogState):
        if "topic" in state and state["topic"]:
            system_prompt =  """You are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic = state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog":{"title": state['blog']['title'], "content": response.content}}

    def translation(self, state:BlogState):
        """
        Translate the content to the specified language.
        """
        title_translation_prompt = """
        Translate the following blog title into {current_language}.
        Return only the translated title.

        ORIGINAL TITLE:
        {blog_title}
        """

        content_translation_prompt = """
        Translate the following blog content into {current_language}.
        - Maintain the original tone, style, and formatting.
        - Adapt cultural references and idioms to be appropriate for {current_language}.

        ORIGINAL CONTENT:
        {blog_content}
        
        """

        print(state["current_language"])
        blog_title = state["blog"]["title"]
        blog_content = state["blog"]["content"]
        title_messages=[
            HumanMessage(
                title_translation_prompt.format(
                    current_language=state["current_language"],
                    blog_title=blog_title,
                )
            )
        ]
        content_messages=[
            HumanMessage(
                content_translation_prompt.format(
                    current_language=state["current_language"],
                    blog_content=blog_content,
                )
            )
        ]
        translated_title = self.llm.invoke(title_messages)
        translated_content = self.llm.invoke(content_messages)
        translated_blog = Blog(
            title=translated_title.content,
            content=translated_content.content,
        )
        return {"blog": translated_blog.model_dump()}

    def route(self, state: BlogState):
        return {"current_language": state['current_language'] }
        
        
    def route_decision(self, state: BlogState):
        """
        Route the content to the respective translation function.
        """
        if state["current_language"] == "hindi":
            return "hindi"
        elif state["current_language"] == "french": 
            return "french"
        else:
            return state['current_language']
