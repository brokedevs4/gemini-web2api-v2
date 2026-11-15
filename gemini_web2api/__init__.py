"""gemini-web2api v2: Gemini Web to OpenAI & Gemini API bridge."""
__version__ = "2.0.0"

from .models import MODELS, resolve_model
from .config import CONFIG

__all__ = ["MODELS", "resolve_model", "CONFIG", "__version__"]
