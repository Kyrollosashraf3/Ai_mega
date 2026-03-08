import google.generativeai as genai
from app.config.settings import settings
from app.core.llm.token_counter import format_usage_response
from app.config.logger import get_logger

logger = get_logger(__name__)

def stream_response_google(model: str, contents: str, max_output_tokens: int, temperature: float, top_p: float = 1.0, top_k: int = None):
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    model_obj = genai.GenerativeModel(model)
    
    if max_output_tokens < 1024:
        max_output_tokens = 1024

    generation_config = {
        "max_output_tokens": max_output_tokens,
        "temperature": temperature,
        "top_p": top_p
    }
    if top_k is not None:
        generation_config["top_k"] = top_k

    try:
        response_stream = model_obj.generate_content(contents, generation_config=generation_config, stream=True)
        for chunk in response_stream:
            try:
                if getattr(chunk, "candidates", None):
                    for candidate in chunk.candidates:
                        if getattr(candidate, "content", None) and getattr(candidate.content, "parts", None):
                            for part in candidate.content.parts:
                                if hasattr(part, "text") and part.text:
                                    yield part.text
                elif hasattr(chunk, "finish_reason"):
                    continue
            except (ValueError, StopIteration):
                continue
    except (ValueError, StopIteration, Exception):
        return




def get_response_google(model: str, contents: str, max_output_tokens: int, temperature: float, top_p: float = 1.0, top_k: int = None):
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    
    if max_output_tokens < 1024:
        max_output_tokens = 1024
    
    model_obj = genai.GenerativeModel(model)
    generation_config = {"max_output_tokens": max_output_tokens, "temperature": temperature, "top_p": top_p}
    if top_k is not None:
        generation_config["top_k"] = top_k

    try:
        response = model_obj.generate_content(contents, generation_config=generation_config)

        text_output = ""
        if hasattr(response, "candidates") and response.candidates:
            for c in response.candidates:
                if hasattr(c, "content") and c.content.parts:
                    for part in c.content.parts:
                        if hasattr(part, "text") and part.text:
                            text_output += part.text

        if not text_output:
            text_output = "[No content generated]"

        usage = None
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            usage_meta = response.usage_metadata
            usage = format_usage_response(getattr(usage_meta, "prompt_token_count", 0), getattr(usage_meta, "candidates_token_count", 0))
        
        return {"text": text_output, "model": model, "usage": usage}
    except Exception as e:
        logger.error(f"[Google] API call failed - {type(e).__name__}: {str(e)}")
        raise
