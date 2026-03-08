import tiktoken
from typing import Dict, Optional, List

def count_tokens_with_tiktoken(text: str, model: str) -> int:
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def count_tokens_for_messages(messages: List[Dict], model: str) -> int:
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    tokens_per_message = 3
    tokens_per_name = 1
    num_tokens = 0
    
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            if isinstance(value, str):
                num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens

def estimate_tokens_for_model(text: str, model_family: str) -> int:
    if model_family in ["openai", "google","groq"]:
        return count_tokens_with_tiktoken(text, "gpt-4")
    return len(text) // 4

def format_usage_response(input_tokens: Optional[int] = None, output_tokens: Optional[int] = None, total_tokens: Optional[int] = None) -> Dict[str, int]:
    input_tokens = input_tokens or 0
    output_tokens = output_tokens or 0
    if total_tokens is None:
        total_tokens = input_tokens + output_tokens
    return {"input_tokens": input_tokens, "output_tokens": output_tokens, "total_tokens": total_tokens}

