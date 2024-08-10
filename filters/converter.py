import subprocess
import os

def convert(html_content: str) -> str:
    script_path = os.path.join("assets", "convert.js")
    result = subprocess.run(
        ["node", script_path],
        input=html_content,
        text=True,
        capture_output=True,
        encoding="utf-8"
    )

    return result.stdout