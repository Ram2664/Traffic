from __future__ import annotations

from backend.utils.settings import get_settings


def gemini_is_configured() -> bool:
    return bool(get_settings().gemini_api_key)


def get_gemini_stub_response(prompt: str) -> dict:
    return {
        'configured': gemini_is_configured(),
        'message': 'Gemini integration scaffold only. Configure GEMINI_API_KEY in .env for future phases.',
        'prompt_preview': prompt[:120],
    }
