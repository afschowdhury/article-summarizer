import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_summary_prompt(keyword: str, content: str) -> str:
    """Creates a prompt for summarizing research papers."""
    prompt = f"""
    You are tasked with summarizing a research paper in a simple and understandable manner for a general audience. The paper has been selected based on a specific keyword search.

    The keyword used to find this research paper is:
    <keyword>
    {keyword}
    </keyword>

    Here is the content of the research paper:
    <content>
    {content}
    </content>

    Please follow these steps to summarize the research paper:

    1. Read through the entire content carefully.
    2. Identify the main topic, research question, or hypothesis of the paper.
    3. Determine the key findings or conclusions of the research.
    4. Note any significant methodologies or approaches used in the study.
    5. Consider the implications or potential applications of the research.

    When writing your summary:
    - Use simple, clear language that a non-expert can understand.
    - Avoid technical jargon where possible. If you must use technical terms, briefly explain them.
    - Focus on the most important and interesting aspects of the research.
    - Keep the summary concise, aiming for about 3-5 paragraphs.
    - Relate the content back to the keyword that was used to find the paper, if relevant.

    Just response with the summary."""

    return [{"role": "user", "content": prompt}]


def get_summary(keyword, processed_content):

    data = []
    for content in processed_content:
        data_dict = {}

        data_dict["title"] = content.get("title")
        if content.get("author") is not None:
            data_dict["author"] = f'{content.get("author")[0].get("name")} et al.'
        else:
            data_dict["author"] = "Unable to detect author"
        data_dict["url"] = content.get("link")

        content = content.get("content")
        if not content:
            continue

        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.5,
            max_tokens=500,
            messages=create_summary_prompt(keyword, content),
        )
        data_dict["summary"] = response.choices[0].message.content
        data.append(data_dict)
    return data
