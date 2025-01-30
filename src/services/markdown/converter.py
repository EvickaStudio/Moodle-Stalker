import re

from .turndown import MarkdownConverter

TURNDOWN = MarkdownConverter({"headingStyle": "atx", "codeBlockStyle": "fenced"})


def convert(html_content: str) -> str:
    """
    Converts HTML content to Markdown using TurndownService.

    Args:
        html_content (str): The HTML content to be converted.

    Returns:
        str: The converted and cleaned content.
    """
    md_output = TURNDOWN.to_markdown(html_content)
    return clean_converted_text(md_output)


def clean_converted_text(text: str) -> str:
    """
    Cleans the converted text by applying regex replacements.

    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text.
    """
    # Regex to detect Markdown images
    # as Discord does not support them, we remove them
    reg = r"\[!\[.*\]\(.*\)\]\(.*\)"
    text = re.sub(reg, "", text)
    # Regex to detect horizontal rules
    reg = r"* * *"
    text = re.sub(reg, "", text)
    return text