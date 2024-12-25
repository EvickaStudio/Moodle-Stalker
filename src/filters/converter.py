import re

from src.turndown import TurndownService

td = TurndownService({"headingStyle": "atx", "codeBlockStyle": "fenced"})


def convert(html_content: str) -> str:
    """
    Converts HTML content to Markdown using TurndownService.

    Args:
        html_content (str): The HTML content to be converted.

    Returns:
        str: The converted and cleaned content.
    """
    md_output = td.turndown(html_content)
    return clean_converted_text(md_output)


def clean_converted_text(text: str) -> str:
    """
    Cleans the converted text by applying regex replacements.

    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text.
    """
    reg = r"\[!\[.*\]\(.*\)\]\(.*\)"
    text = re.sub(reg, "", text)
    text = text.replace("* * *", "")
    return text
