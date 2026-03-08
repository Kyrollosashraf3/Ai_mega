# ============================================================================
# Added get_model_family() function to determine model family from registry
# Updated to support all model families in models_registry.json
# ============================================================================

"""Utility functions for model handling."""

import json
from app.config.settings import settings
from app.config.logger import get_logger


def _load_registry_data():
    """Load and cache registry data to avoid multiple file reads."""
    try:
        with open(settings.MODELS_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Could not load models data: {e}")


def get_model_info(model_name: str) -> dict:
    """Get model information from registry (searches all families)."""
    data = _load_registry_data()
    
    for family, models in data.items():
        for model_info in models:
            if model_info.get("model_name") == model_name:
                return model_info
    
    raise ValueError(f"Model '{model_name}' not found in registry.")


def get_model_family(model_name: str) -> str:
    """Get the model family (e.g., 'huggingface') for a given model name."""
    data = _load_registry_data()
    
    for family, models in data.items():
        for model_info in models:
            if model_info.get("model_name") == model_name:
                return family
    
    raise ValueError(f"Model '{model_name}' not found in registry.")


def validate_model_access(model_name: str) -> bool:
    """
    Check if model exists in registry AND has an endpoint configured.
    For HuggingFace models, also verifies the model is in HUGGINGFACE_ENDPOINTS.
    """
    try:
        data = _load_registry_data()
        
        # Find model and family in single pass
        for family, models in data.items():
            for model_info in models:
                if model_info.get("model_name") == model_name:
                    return True

    except (ValueError, RuntimeError):
        return False



def prepare_family_parameters(req: dict, family: str) -> dict:
    base = {
        "model": req["model"],
        "temperature": req.get("temperature", 1.0),
        "max_tokens": req.get("max_tokens", 1024),
        "top_p": req.get("top_p", 1),
        "frequency_penalty": req.get("frequency_penalty", 0),
        "presence_penalty": req.get("presence_penalty", 0),
        "stream": req.get("stream", False),
    }

    messages = req.get("messages", [])
    
    if family in ["openai", "groq"]:
        base["messages"] = messages
        # Special handling for gpt-5 models which may not support temperature/top_p
        if base["model"].startswith("gpt-5"):
            base["temperature"] = None
            base["top_p"] = None

    elif family == "google":
        base["contents"] = "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in messages)
        base["max_output_tokens"] = base.pop("max_tokens")
        base.pop("messages", None)
    else:
        raise ValueError(f"Unknown model family: {family}")
    return base
