import json
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.config import settings
from app.models.schemas import ChatRequest
from app.config.logger import get_logger
from app.core.llm.stream_handler import stream_model_family
from app.core.llm.utils import get_model_family, validate_model_access
from app.core.llm.call_handler import call_model_family
from app.core.llm.token_counter import estimate_tokens_for_model, count_tokens_for_messages, format_usage_response

logger = get_logger(__name__)
 

router = APIRouter(tags=["chat"])

@router.get("/models")
async def get_models():
    try:
        with open(settings.MODELS_JSON_PATH, "r", encoding="utf-8") as f:
            models = json.load(f)
            logger.info(f"[Models] Returned {sum(len(v) for v in models.values())} models")
            return models
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Model registry file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid model registry format")
    except Exception as e:
        logger.error(f"[Models] Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error reading models: {str(e)}")


async def event_generator(request: ChatRequest):
    """Internal generator for Server-Sent Events with usage tracking."""
    collected_chunks = []
    try:
        # stream_model_family should return an iterator/generator
        for chunk in stream_model_family(request):
            collected_chunks.append(chunk)
            yield f"data: {chunk}\n\n"
        
        full_response = "".join(collected_chunks)
        family = get_model_family(request.model)
        
        # Token counting logic
        if family == "openai":
            input_tokens = count_tokens_for_messages(
                [{"role": msg.role, "content": msg.content} for msg in request.messages], 
                request.model
            )
        else:
            input_text = "\n".join([f"{msg.role}: {msg.content}" for msg in request.messages])
            input_tokens = estimate_tokens_for_model(input_text, family)
            
        output_tokens = estimate_tokens_for_model(full_response, family)
        usage = format_usage_response(input_tokens, output_tokens)
        
        yield f"data: [USAGE] {json.dumps(usage)}\n\n"
        yield "data: [DONE]\n\n"
        logger.info(f"[Chat] Stream completed: {usage['total_tokens']} tokens")
        
    except Exception as e:
        logger.error(f"[Chat] Stream error: {type(e).__name__}: {str(e)}")
        yield f"data: [ERROR] {str(e)}\n\n"


@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        if not validate_model_access(request.model):
            raise HTTPException(status_code=403, detail="Access denied for this model")
            
        if request.stream:
            return StreamingResponse(event_generator(request), media_type="text/event-stream")
        else:
            response = prepare_family_parameters(request)
            return response
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Chat] Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")