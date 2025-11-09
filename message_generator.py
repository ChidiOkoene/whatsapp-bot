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
    
    prompt = f"""Generate a romantic, funny, loving, and cute WhatsApp message for my {relationship} named {recipient_name}.

The message should be:
- Romantic and heartfelt, expressing deep love and affection
- Funny and playful, with cute humor that makes them smile
- Loving and warm, showing how much they mean to you
- Cute and endearing, with sweet details or inside jokes if possible
- Multiple sentences (2-4 sentences), not just one generic line
- Personal and specific, not generic or cliché
- Natural and conversational, like you're really talking to them
- Include 2-4 emojis that match the tone
- Keep it under {max_length} characters total

Make it feel genuine, like you're really thinking about them right now. Mix romance with humor and cuteness.

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
                {"role": "system", "content": "You are a creative and romantic message writer who creates heartfelt, funny, and cute WhatsApp messages. You excel at mixing romance with humor and creating messages that feel genuine and personal."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,  # Increased for longer messages
            temperature=0.9  # Higher temperature for more creativity and variety
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
    
    prompt = f"""Generate a romantic, funny, loving, and cute WhatsApp message for my {relationship} named {recipient_name}.

The message should be:
- Romantic and heartfelt, expressing deep love and affection
- Funny and playful, with cute humor that makes them smile
- Loving and warm, showing how much they mean to you
- Cute and endearing, with sweet details or inside jokes if possible
- Multiple sentences (2-4 sentences), not just one generic line
- Personal and specific, not generic or cliché
- Natural and conversational, like you're really talking to them
- Include 2-4 emojis that match the tone
- Keep it under {max_length} characters total

Make it feel genuine, like you're really thinking about them right now. Mix romance with humor and cuteness.

Generate only the message text, nothing else:"""

    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "You are a creative and romantic message writer who creates heartfelt, funny, and cute WhatsApp messages. You excel at mixing romance with humor and creating messages that feel genuine and personal."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,  # Increased for longer messages
            temperature=0.9  # Higher temperature for more creativity and variety
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
    
    # Message templates - More romantic, funny, and cute
    templates = [
        f"{greeting} {recipient_name}! 💕 I was just thinking about you and couldn't help but smile. You have this amazing way of making everything better, even when you're not here. Sending you all my love and a million hugs! 🤗❤️",
        f"Hey {recipient_name}! 😊 I know this is random, but I was just sitting here and realized how incredibly lucky I am to have you. You're not just my {relationship}, you're my favorite person, my best friend, and honestly, the cutest human on the planet! 💖✨",
        f"Hi beautiful! 🌟 Just wanted to tell you that I love you more than words can say. You make my heart do this little happy dance every time I think of you (which is basically all the time 😅). Can't wait to see you! 💕",
        f"{greeting} {recipient_name}! 💭 You know what's funny? I was trying to focus on something, but my brain kept going 'but what about {recipient_name}?' 😂 I guess my heart just really misses you right now. Sending you all the love! ❤️🤗",
        f"Hey {recipient_name}! ☀️ I hope you're having the most amazing day because you absolutely deserve it! You're the kind of person who makes everything brighter just by existing. Also, you're super cute and I love you! 💖😊",
        f"Hi {recipient_name}! 💕 Random thought: I was just thinking about how you laugh at my terrible jokes and how you make even the most ordinary moments feel special. You're honestly the best thing that's ever happened to me. Love you so much! ❤️✨",
        f"{greeting} my love! 🤗 I know I tell you this a lot, but you're genuinely the most amazing person I know. You're beautiful, funny, kind, and you put up with me - which honestly deserves an award! 😂💖",
        f"Hey {recipient_name}! 🌟 Just a quick message to say you're on my mind (as always) and I'm sending you all the good vibes, hugs, and love! You make everything better just by being you. Can't wait to talk to you! 💕😊",
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

