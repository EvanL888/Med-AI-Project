"""Safely load Azure OpenAI secrets from a fixed path."""
import importlib.util
import sys
import os
 
SECRET_PATH = r"C:\Users\Evan\Documents\VS Code\API Keys\secrets.py"
FALLBACK_SECRET_PATH = r"C:\Users\ahmtt\Documents\VS\API KEY\secret.py"
 
class Secret:
    """Secrets for Azure OpenAI (loaded at runtime)."""
    AZURE_OPENAI_DEPLOYMENT: str = ""
    AZURE_OPENAI_API_KEY: str = ""
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_SPEECH_STT_DEPLOYMENT: str = ""
    AZURE_SPEECH_STT_KEY: str = ""
    AZURE_SPEECH_STT_ENDPOINT: str = ""
    AZURE_SPEECH_STT_REGION: str = ""
    AZURE_OPENAI_SPEECH_TTS_DEPLOYMENT: str = ""
    AZURE_SPEECH_TTS_KEY: str = ""
    AZURE_SPEECH_TTS_ENDPOINT: str = ""
    AZURE_SPEECH_TTS_REGION: str = ""
 
 
def load_secrets() -> Secret:
    """Dynamically import secret.py from fixed path or fallback path. Fail gracefully if missing."""
    # Try primary path first, then fallback path
    secret_path = SECRET_PATH
    if not os.path.exists(SECRET_PATH):
        if os.path.exists(FALLBACK_SECRET_PATH):
            secret_path = FALLBACK_SECRET_PATH
        else:
            raise RuntimeError(f"secret.py not found at {SECRET_PATH} or {FALLBACK_SECRET_PATH}. Please create it with your Azure OpenAI credentials.")
    
    try:
        spec = importlib.util.spec_from_file_location("secret", secret_path)
        secret = importlib.util.module_from_spec(spec)
        sys.modules["secret"] = secret
        spec.loader.exec_module(secret)
        s = Secret()
        s.AZURE_OPENAI_DEPLOYMENT = getattr(secret, "AZURE_OPENAI_DEPLOYMENT", "")
        s.AZURE_OPENAI_API_KEY = getattr(secret, "AZURE_OPENAI_API_KEY", "")
        s.AZURE_OPENAI_ENDPOINT = getattr(secret, "AZURE_OPENAI_ENDPOINT", "")
        s.AZURE_OPENAI_SPEECH_STT_DEPLOYMENT = getattr(secret, "AZURE_OPENAI_SPEECH_STT_DEPLOYMENT", "")
        s.AZURE_SPEECH_STT_KEY = getattr(secret, "AZURE_SPEECH_STT_KEY", "")
        s.AZURE_SPEECH_STT_ENDPOINT = getattr(secret, "AZURE_SPEECH_STT_ENDPOINT", "")
        s.AZURE_SPEECH_STT_REGION = getattr(secret, "AZURE_SPEECH_STT_REGION", "")
        s.AZURE_OPENAI_SPEECH_TTS_DEPLOYMENT = getattr(secret, "AZURE_OPENAI_SPEECH_TTS_DEPLOYMENT", "")
        s.AZURE_SPEECH_TTS_KEY = getattr(secret, "AZURE_SPEECH_TTS_KEY", "")
        s.AZURE_SPEECH_TTS_ENDPOINT = getattr(secret, "AZURE_SPEECH_TTS_ENDPOINT", "")
        s.AZURE_SPEECH_TTS_REGION = getattr(secret, "AZURE_SPEECH_TTS_REGION", "")
        if not all([
            s.AZURE_OPENAI_DEPLOYMENT,
            s.AZURE_OPENAI_API_KEY,
            s.AZURE_OPENAI_ENDPOINT,
            s.AZURE_OPENAI_SPEECH_STT_DEPLOYMENT,
            s.AZURE_OPENAI_SPEECH_TTS_DEPLOYMENT,
        ]):
            raise RuntimeError(f"secret.py is missing required fields. Please check your credentials at {secret_path}.")
        return s
    except Exception as e:
        raise RuntimeError(f"Failed to load secrets from secret.py at {secret_path}. Please check the file and try again. [REDACTED]") from None
 
