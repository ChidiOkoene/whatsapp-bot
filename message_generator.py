"""
LLM Message Generator for WhatsApp Bot
Supports LM Studio (local), OpenAI, and template-based generation
"""
import os
from typing import Optional

# Try to import OpenAI, but make it optional
try:
    import openai  # type: ignore
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None  # type: ignore

# Configuration
# LM Studio Configuration (local LLM)
# Update the base URL to match your LM Studio server address
# Check LM Studio's "Reachable at" address in the server settings
LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://192.168.1.57:1234/v1")
# Model name - leave empty to auto-detect, or specify like "mistralai/mistral-7b-instruct-v0.3"
LM_STUDIO_MODEL = os.getenv("LM_STUDIO_MODEL", "")  # Leave empty to auto-detect the loaded model
USE_LM_STUDIO = os.getenv("USE_LM_STUDIO", "true").lower() == "true"  # Default to LM Studio

# OpenAI Configuration (cloud)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEFAULT_MODEL = "gpt-3.5-turbo"  # or "gpt-4" for better quality


def generate_message_lm_studio(
    recipient_name: str = "darling",
    relationship: str = "romantic partner",
    style: str = "sweet and loving",
    max_length: int = 100
) -> str:
    """
    Generate a message using LM Studio local API.
    
    Args:
        recipient_name: Name of the recipient
        relationship: Relationship with recipient
        style: Style of the message
        max_length: Maximum length of the message
    
    Returns:
        Generated message string
    """
    if not OPENAI_AVAILABLE or openai is None:
        raise ImportError("OpenAI library not installed. Run: pip install openai")
    
    # LM Studio uses OpenAI-compatible API, but no API key needed
    # Use a dummy key since LM Studio doesn't require authentication
    client = openai.OpenAI(  # type: ignore
        base_url=LM_STUDIO_BASE_URL,
        api_key="lm-studio"  # LM Studio doesn't require a real API key
    )
    
    prompt = f"""Generate a short, {style} WhatsApp message for my {relationship} named {recipient_name}.
    
Requirements:
- Keep it under {max_length} characters
- Make it personal and heartfelt
- Include an emoji or two
- Be natural and conversational
- Don't be too formal

Generate only the message text, nothing else:"""

    try:
        # Get the model name - try to fetch from LM Studio, or use specified/default
        model = LM_STUDIO_MODEL
        if not model:
            # Try to get the first available model from LM Studio
            try:
                models_response = client.models.list()
                if models_response.data and len(models_response.data) > 0:
                    model = models_response.data[0].id
                else:
                    model = "local-model"  # Fallback
            except:
                model = "local-model"  # Fallback if we can't list models
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates personal, warm WhatsApp messages."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.8
        )
        
        message = response.choices[0].message.content.strip()
        # Remove quotes if the model wrapped it in quotes
        if message.startswith('"') and message.endswith('"'):
            message = message[1:-1]
        if message.startswith("'") and message.endswith("'"):
            message = message[1:-1]
        
        return message
    except Exception as e:
        raise Exception(f"Failed to generate message with LM Studio: {e}. Make sure LM Studio is running and the server is active.")


def generate_message_openai(
    recipient_name: str = "darling",
    relationship: str = "romantic partner",
    style: str = "sweet and loving",
    max_length: int = 100
) -> str:
    """
    Generate a message using OpenAI API.
    
    Args:
        recipient_name: Name of the recipient
        relationship: Relationship with recipient
        style: Style of the message
        max_length: Maximum length of the message
    
    Returns:
        Generated message string
    """
    if not OPENAI_AVAILABLE or openai is None:
        raise ImportError("OpenAI library not installed. Run: pip install openai")
    
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY not set. Set it as an environment variable or in the script."
        )
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY)  # type: ignore
    
    prompt = f"""Generate a short, {style} WhatsApp message for my {relationship} named {recipient_name}.
    
Requirements:
- Keep it under {max_length} characters
- Make it personal and heartfelt
- Include an emoji or two
- Be natural and conversational
- Don't be too formal

Generate only the message text, nothing else:"""

    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates personal, warm WhatsApp messages."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.8
        )
        
        message = response.choices[0].message.content.strip()
        # Remove quotes if the model wrapped it in quotes
        if message.startswith('"') and message.endswith('"'):
            message = message[1:-1]
        if message.startswith("'") and message.endswith("'"):
            message = message[1:-1]
        
        return message
    except Exception as e:
        raise Exception(f"Failed to generate message with OpenAI: {e}")


def generate_message_simple(
    recipient_name: str = "darling",
    relationship: str = "romantic partner",
    style: str = "sweet and loving"
) -> str:
    """
    Generate a simple message without LLM (fallback option).
    Uses template-based generation.
    """
    import random
    from datetime import datetime
    
    hour = datetime.now().hour
    
    # Time-based greetings
    if hour < 12:
        greeting = "Good morning"
    elif hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    # Message templates
    templates = [
        f"{greeting} {recipient_name}! Thinking of you and sending lots of love 💕",
        f"Hey {recipient_name}! Hope you're having an amazing day 😊",
        f"Just wanted to say I love you, {recipient_name}! ❤️",
        f"Hi {recipient_name}! You're on my mind right now 💭✨",
        f"{greeting} beautiful! Sending you warm hugs and kisses 🤗💋",
        f"Hey {recipient_name}! You make my day brighter ☀️💖",
        f"Just a quick message to say I'm thinking of you, {recipient_name} 💕",
        f"Hi {recipient_name}! Hope your day is as wonderful as you are 🌟",
    ]
    
    return random.choice(templates)


def generate_message(
    use_llm: bool = True,
    recipient_name: str = "darling",
    relationship: str = "romantic partner",
    style: str = "sweet and loving",
    max_length: int = 100
) -> str:
    """
    Main function to generate a message.
    Tries LLM (LM Studio or OpenAI) first, falls back to simple generation if LLM is not available.
    
    Args:
        use_llm: Whether to use LLM or simple template-based generation
        recipient_name: Name of the recipient
        relationship: Relationship with recipient
        style: Style of the message
        max_length: Maximum length of the message
    
    Returns:
        Generated message string
    """
    if not use_llm:
        return generate_message_simple(
            recipient_name=recipient_name,
            relationship=relationship,
            style=style
        )
    
    if not OPENAI_AVAILABLE:
        print("⚠️  OpenAI library not installed. Using simple message generation...")
        return generate_message_simple(
            recipient_name=recipient_name,
            relationship=relationship,
            style=style
        )
    
    # Try LM Studio first (if enabled), then OpenAI, then fallback
    if USE_LM_STUDIO:
        try:
            return generate_message_lm_studio(
                recipient_name=recipient_name,
                relationship=relationship,
                style=style,
                max_length=max_length
            )
        except Exception as e:
            print(f"⚠️  LM Studio generation failed: {e}")
            print("   Trying OpenAI...")
            # Fall through to try OpenAI if LM Studio fails
    
    # Try OpenAI if LM Studio is disabled or failed
    if OPENAI_API_KEY:
        try:
            return generate_message_openai(
                recipient_name=recipient_name,
                relationship=relationship,
                style=style,
                max_length=max_length
            )
        except Exception as e:
            print(f"⚠️  OpenAI generation failed: {e}")
            print("   Falling back to simple message generation...")
            return generate_message_simple(
                recipient_name=recipient_name,
                relationship=relationship,
                style=style
            )
    else:
        print("⚠️  No LLM configured (LM Studio not running or OpenAI API key not set).")
        print("   Using simple message generation...")
        return generate_message_simple(
            recipient_name=recipient_name,
            relationship=relationship,
            style=style
        )


if __name__ == "__main__":
    # Test the message generator
    print("Testing message generator...")
    print("\n1. Simple generation (no LLM):")
    print(generate_message(use_llm=False, recipient_name="darling"))
    
    if OPENAI_AVAILABLE:
        print("\n2. LLM generation:")
        if USE_LM_STUDIO:
            print(f"   Trying LM Studio at {LM_STUDIO_BASE_URL}...")
        elif OPENAI_API_KEY:
            print("   Trying OpenAI...")
        else:
            print("   No LLM configured")
        
        try:
            print(generate_message(use_llm=True, recipient_name="darling"))
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("\n2. LLM generation skipped (OpenAI library not installed)")

