from app.core.llm.utils import get_model_family, prepare_family_parameters
from app.config.logger import get_logger

from app.core.llm.families.google import stream_response_google
from app.core.llm.families.openai import stream_response_openai
from app.core.llm.families.groq  import stream_response_groq

logger = get_logger(__name__)

def stream_model_family(req):
    """Standardized handler for streaming LLM requests."""
    logger.info(f"[Stream] Processing model: {req.model}")
    
    # Ensure user message exists
    user_query = None
    for msg in reversed(req.messages):
        role = msg.role if hasattr(msg, "role") else msg.get("role")
        if role == "user":
            user_query = msg.content if hasattr(msg, "content") else msg.get("content")
            break
            
    if not user_query:
        logger.error("[Stream] No user message found in request")
        raise ValueError("No user message found in request")

    family = get_model_family(req.model)
    params = prepare_family_parameters(req.dict(), family)

    if family == "google":
        return stream_response_google(
            model=params["model"],
            contents=params["contents"], 
            max_output_tokens=params["max_output_tokens"], 
            temperature=params["temperature"], 
            top_p=params["top_p"]
        )
    
    elif family == "openai":
        return stream_response_openai(
            model=params["model"],
            messages=params["messages"], 
            max_tokens=params["max_tokens"], 
            temperature=params["temperature"], 
            top_p=params["top_p"]
        )
        
    elif family == "groq":
       return stream_response_groq(
           model=params["model"],
           messages=params["messages"], 
           max_tokens=params["max_tokens"],
           temperature=params["temperature"],
           top_p=params["top_p"]
        )

    else:
        logger.error(f"[Stream] Unsupported model family: {family}")
        raise ValueError(f"Unsupported family: {family}")