"""Constants for the Parasail STT integration."""

DOMAIN = "parasail_stt"

CONF_API_KEY = "api_key"
CONF_MODEL = "model"

DEFAULT_MODEL = "openai/whisper-large-v3-turbo"

PARASAIL_API_BASE = "https://api.parasail.io/v1"

# Available Whisper models on Parasail
PARASAIL_STT_MODELS = [
    "openai/whisper-large-v3-turbo",
    "openai/whisper-large-v3",
]
