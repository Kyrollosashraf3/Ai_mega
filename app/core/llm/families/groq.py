from groq import Groq
from app.config.settings import settings


def stream_response_groq(model: str, messages: list, temperature: float = 1.0, max_tokens: int = 1024, top_p: float = 1.0):
    if not settings.GROQ_API_KEY:
        raise ValueError("Missing GROQ_API_KEY")

    client = Groq(api_key=settings.GROQ_API_KEY)

    response_stream = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=True,  # enable streaming
        )


    for chunk in response_stream:
        #print(chunk.choices[0].delta.content)
    
        choices = getattr(chunk, "choices", [])
        for choice in choices:
            delta = getattr(choice, "delta", None)
            content = getattr(delta, "content", None)
            if content:
                yield content  


def get_response_groq(model: str, messages: list, temperature: float = 1.0, max_tokens: int = 1024, top_p: float = None, stream: bool = False):
    """
    Unified Groq wrapper: supports both streaming and non-streaming.
    """

    client = Groq(api_key=settings.GROQ_API_KEY)

    # --- Non-streaming mode ---
   
    resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )

    text = ""
    choices = getattr(resp, "choices", [])
    for choice in choices:
            # Try delta first
            delta = getattr(choice, "delta", None)
            if delta and getattr(delta, "content", None):
                text += delta.content
            else:
                # Fallback to message.content
                message = getattr(choice, "message", None)
                if message:
                    text += getattr(message, "content", "")
               

    return {
            "text": text,
            "model": model,
        }

   
