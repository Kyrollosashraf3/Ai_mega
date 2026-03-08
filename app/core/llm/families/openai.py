from openai import OpenAI
from app.config.settings import settings
from app.config.logger import get_logger
from app.core.llm.token_counter import format_usage_response, count_tokens_for_messages, count_tokens_with_tiktoken

logger = get_logger(__name__)

def stream_response_openai(model: str, messages: list, max_tokens: int, temperature: float, top_p: float):
    client = OpenAI(api_key=settings.OPENAI_API_KEY, timeout=120.0)
    formatted_messages = [
        {
            "role": msg.role if hasattr(msg, "role") else msg["role"],
            "content": msg.content if hasattr(msg, "content") else msg["content"]
        } 
        for msg in messages
    ]
    
    # Handle temperature/top_p for o1/o3 models if necessary (OpenAI sometimes restricts these)
    kwargs = {
        "model": model,
        "messages": formatted_messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "stream": True
    }
    
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    try:
        response_stream = client.chat.completions.create(**kwargs)
        for chunk in response_stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        logger.error(f"[OpenAI] Stream failed - {type(e).__name__}: {str(e)}")
        raise

def get_response_openai(model: str, messages: list, max_tokens: int, temperature: float, top_p: float):
    client = OpenAI(api_key=settings.OPENAI_API_KEY, timeout=120.0)
    formatted_messages = [
        {
            "role": msg.role if hasattr(msg, "role") else msg["role"],
            "content": msg.content if hasattr(msg, "content") else msg["content"]
        } 
        for msg in messages
    ]
    
    kwargs = {
        "model": model,
        "messages": formatted_messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p
    }
    
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    try:
        response = client.chat.completions.create(**kwargs)
        text = response.choices[0].message.content or ""
        
        input_tokens = response.usage.prompt_tokens if response.usage else count_tokens_for_messages(formatted_messages, model)
        output_tokens = response.usage.completion_tokens if response.usage else count_tokens_with_tiktoken(text, model)
        usage = format_usage_response(input_tokens, output_tokens)

        return {
            "message": text,
            "usage": usage
        }
    except Exception as e:
        logger.error(f"[OpenAI] API call failed - {type(e).__name__}: {str(e)}")
        raise
