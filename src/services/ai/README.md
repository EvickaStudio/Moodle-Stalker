# OpenAI Chat/ Assistant Module

## Overview

This module, `openai_chat.py`, provides an interface to OpenAI's API for integrating chat or assistant functionalities using GPT-3.5 and GPT-4 models.

## Installation

Install and update the OpenAI Python library:

```bash
pip install -U openai
```

## Usage

### Initialize

Create a `GPT` class instance:

```python
from openai_chat import GPT

gpt = GPT()
```

### Set API Key

Set your OpenAI API key:

```python
gpt.api_key = "your_openai_api_key"
```

### Chat Completion

Generate a response using a model, system message, and user message:

```python
response = gpt.chat_completion(
    model="gpt-3.5-turbo",
    systemMessage="Your system message",
    userMessage="Your user message"
)
print(response)
```

### Standalone Assistant

Use the assistant to generate a response. The assistant will have no context of prior conversation:

```python
response = gpt.assistant(prompt="Your prompt message")
print(response)
```

### Context Assistant

Use the assistant with saving and keeping context, like a chatbot for your notifications:

```python
response = gpt.context_assistant(prompt="Your prompt message")
print(response)
```

## Function Descriptions

### `api_key(self, key: str) -> None:`

Set the API key, ensuring it is not empty and validating it with a regex pattern.

### `chat_completion(self, model: str, system_message: str, user_message: str) -> str:`

Generate a response from the chat API using the specified model and prompts.

### `assistant(self, prompt: str, thread_id: str = None) -> str:`

Manages individual threads for each message/summary, optimizing costs. Context from prior notifications is not used.

### `context_assistant(self, prompt: str) -> str:`

A context-aware assistant, like a chatbot that can remember and use information from previous notification to have a better understanding of the current context.

### `def run_assistant(self, prompt, thread_id):`

Run the assistant to generate a response for the given assistant and textwith or without a thread token.

### `create_thread(self) -> str:`

Generates a new thread for the assistant and returns the thread ID.

### `save_thread(self, thread_id: str) -> None:`

Stores the thread ID in a .ini file for later retrieval.

### `update_thread(self, thread_id: str) -> None:`

Refreshes the thread ID in the config, clearing previous conversation context.

### `resume_thread(self) -> str:`

Retrieves the thread ID from the thread.ini file.

## Dependencies

- `openai` (i am using v1.6)
- `configparser`
