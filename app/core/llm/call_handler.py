from app.core.llm.utils import get_model_family, prepare_family_parameters
from app.config.logger import get_logger
from app.core.llm.perplexity import PerplexityError, SearchMode, get_perplexity_client
from app.core.llm.families.google import get_response_google
from app.core.llm.families.openai import get_response_openai
from app.core.llm.families.groq  import get_response_groq
 
logger = get_logger(__name__)

def call_model_family(req):
    """Standardized handler for non-streaming LLM requests."""
    logger.info(f"[Call] Processing model: {req.model}")

    # Ensure user message exists
            
    user_query = None
    for msg in reversed(req.messages):
        msg_role = msg.role if hasattr(msg, "role") else msg.get("role")
        msg_content = msg.content if hasattr(msg, "content") else msg.get("content")
        if msg_role == "user":
            user_query = msg_content
            break
    if not user_query:
        logger.error("[Chat] No user message found")
        raise ValueError("No user message found in request")
        



    # WEB SEARCH

    if req.web_search_mode and req.web_search_mode in ["fast", "deep"]:
        try:
            search_mode = SearchMode.FAST if req.web_search_mode == "fast" else SearchMode.DEEP
            perplexity = get_perplexity_client()
            search_result = perplexity.search(query=user_query, mode=search_mode, temperature=req.web_search_temperature if req.web_search_temperature is not None else 0.2, top_p=req.web_search_top_p if req.web_search_top_p is not None else 0.9, max_tokens=req.web_search_max_tokens if req.web_search_max_tokens is not None else 1024)
            context_info["web_search"] = {"mode": req.web_search_mode, "result": search_result}
            web_text = f"Web Search Results ({req.web_search_mode} mode):\n\n{search_result.get('content', '')}\n"
            citations = search_result.get("citations", [])
            if citations:
                web_text += "\n\nSource URLs:\n"
                for cite in citations:
                    web_text += f"- {cite}\n"
                web_text += "\nIMPORTANT: When referencing information from web search, cite using the full URL in square brackets immediately after the information, e.g., [https://example.com]"
                combined_contexts.append(("Web Search", web_text))
                active_modes.append("web_search")
        except (PerplexityError, Exception) as e:
            logger.error(f"[Chat] Web search error: {type(e).__name__}: {str(e)}")
            


    # Stream - Non stream Chat
    family = get_model_family(req.model)
    params = prepare_family_parameters(req.dict(), family)

    if family == "google":
        return get_response_google(
            model=params["model"],
            contents=params["contents"],
            max_output_tokens=params["max_output_tokens"],
            temperature=params["temperature"],
            top_p=params["top_p"]
        )
    elif family == "openai":
        return get_response_openai(
            model=params["model"],
            messages=params["messages"],
            max_tokens=params["max_tokens"],
            temperature=params["temperature"],
            top_p=params["top_p"]
        )
    elif family == "groq":
        return get_response_groq(
            model=params["model"],
            messages=params["messages"],
            temperature=params["temperature"],
            max_tokens=params["max_tokens"],
            top_p=params["top_p"]
        )
    else:
        logger.error(f"[Call] Unsupported model family for non-streaming: {family}")
        raise ValueError(f"Unsupported family for non-streaming: {family}")
