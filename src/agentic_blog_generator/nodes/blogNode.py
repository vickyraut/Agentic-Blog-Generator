from src.agentic_blog_generator.states.blogState import Blog, BlogState
from langchain_core.messages import HumanMessage

class BlogNode:
    """
    A class for representing blog graph nodes
    """

    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogState):
        """
        Create an SEO-friendly title for the blog.
        """
        if "topic" in state and state["topic"]:
            prompt = """You are an expert SEO blog content writer.
Generate a compelling, creative, and SEO-friendly blog title for the topic: "{topic}".
Do NOT enclose the title in quotes. Return ONLY the title text.
"""
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            clean_title = response.content.strip().strip('"').strip("'")
            return {"blog": {"title": clean_title, "content": ""}}

    def content_generation(self, state: BlogState):
        """
        Generate detailed blog content formatted in Markdown.
        """
        if "topic" in state and state["topic"]:
            length_setting = state.get("blog_length", "Medium").capitalize()
            length_instructions = {
                "Short": "Keep the blog concise, well-structured, and around 300 to 500 words.",
                "Medium": "Provide comprehensive coverage, well-structured sections, and around 800 to 1200 words.",
                "Long": "Provide an in-depth, highly detailed breakdown with multiple subheadings, examples, and 1500+ words."
            }
            length_guide = length_instructions.get(length_setting, length_instructions["Medium"])

            system_prompt = """You are an expert blog writer and content creator. Use Markdown formatting.
Generate high-quality blog content for the topic: "{topic}".
Title: "{title}"

Guidelines:
- {length_guide}
- Use clear Markdown headings (H2, H3), bullet points, and subheadings.
- Include informative tables, code blocks, or blockquotes where appropriate.
- Maintain an engaging, professional tone.
"""
            current_title = state.get("blog", {}).get("title", state["topic"])
            system_message = system_prompt.format(
                topic=state["topic"],
                title=current_title,
                length_guide=length_guide
            )
            response = self.llm.invoke(system_message)
            return {"blog": {"title": current_title, "content": response.content}}

    def translation(self, state: BlogState):
        """
        Dynamically translate the blog title and content into the specified target language.
        If the target language is English or unspecified, skip translation.
        """
        target_language = state.get("current_language", "English").strip()
        
        # Skip translation if target language is English
        if not target_language or target_language.lower() in ["english", "en"]:
            return {"blog": state.get("blog", {})}

        blog_title = state["blog"]["title"]
        blog_content = state["blog"]["content"]

        title_translation_prompt = """Translate the following blog title into {current_language}.
Return ONLY the translated title without extra quotes or commentary.

ORIGINAL TITLE:
{blog_title}
"""

        content_translation_prompt = """Translate the following blog content into {current_language}.
- Maintain all Markdown formatting (headings, lists, tables, code blocks, bold text).
- Keep code snippets in code blocks unchanged unless comments need translation.
- Preserve the tone and structure of the original content.

ORIGINAL CONTENT:
{blog_content}
"""

        title_messages = [
            HumanMessage(
                content=title_translation_prompt.format(
                    current_language=target_language,
                    blog_title=blog_title,
                )
            )
        ]
        content_messages = [
            HumanMessage(
                content=content_translation_prompt.format(
                    current_language=target_language,
                    blog_content=blog_content,
                )
            )
        ]

        translated_title = self.llm.invoke(title_messages)
        translated_content = self.llm.invoke(content_messages)

        translated_blog = Blog(
            title=translated_title.content.strip().strip('"'),
            content=translated_content.content,
        )
        return {"blog": translated_blog.model_dump()}
