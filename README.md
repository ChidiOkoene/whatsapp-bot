# WhatsApp Bot 🤖

A WhatsApp automation bot using `pywhatkit` that sends scheduled messages automatically. Features AI-powered message generation using LLM (OpenAI) or simple template-based messages.

## 🧰 Installation

1. Install the required packages:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install pywhatkit
pip install pyautogui
pip install schedule
pip install openai  # Optional: for LLM message generation
```

## ⚙️ Setup

1. Open `whatsapp_bot.py` in your editor
2. Update the configuration:
   - Replace `phone_number` with the recipient's number (include country code, e.g., `+1234567890`)
   - Configure LLM settings (see below)

### 🤖 LLM Message Generation (Optional)

The bot can generate unique messages using AI:

**Option 1: Using LM Studio (Local, Free, Recommended)**
1. Download and install [LM Studio](https://lmstudio.ai/)
2. Load a model in LM Studio
3. Start the local server in LM Studio (usually runs on `http://localhost:1234`)
4. The bot will automatically use LM Studio if it's running (default behavior)
5. Optional: Customize the endpoint or model name via environment variables:
   ```bash
   # Windows PowerShell
   $env:LM_STUDIO_BASE_URL="http://localhost:1234/v1"
   $env:LM_STUDIO_MODEL="your-model-name"  # Optional: leave empty to auto-detect
   
   # Linux/Mac
   export LM_STUDIO_BASE_URL="http://localhost:1234/v1"
   export LM_STUDIO_MODEL="your-model-name"  # Optional
   ```
6. In `whatsapp_bot.py`, set `USE_LLM = True` (default)

**Option 2: Using OpenAI (Cloud, Paid)**
1. Get an API key from [OpenAI](https://platform.openai.com/api-keys)
2. Set it as an environment variable:
   ```bash
   # Windows PowerShell
   $env:OPENAI_API_KEY="your-api-key-here"
   $env:USE_LM_STUDIO="false"  # Disable LM Studio
   
   # Windows CMD
   set OPENAI_API_KEY=your-api-key-here
   set USE_LM_STUDIO=false
   
   # Linux/Mac
   export OPENAI_API_KEY=your-api-key-here
   export USE_LM_STUDIO=false
   ```
3. In `whatsapp_bot.py`, set `USE_LLM = True`

**Option 3: Simple Template-Based (No LLM Needed)**
- Set `USE_LLM = False` in `whatsapp_bot.py`
- Messages will be generated from templates (free, no API key required)

**Customize Message Generation:**
```python
RECIPIENT_NAME = "darling"  # Name of the recipient
RELATIONSHIP = "romantic partner"  # Your relationship
MESSAGE_STYLE = "sweet and loving"  # Style: "funny", "romantic", "casual", etc.
MAX_MESSAGE_LENGTH = 100  # Maximum characters
```

## 🚀 Usage

Run the script:

```bash
python whatsapp_bot.py
```

**First time setup:**
- The script will open WhatsApp Web in your default browser
- Scan the QR code with your phone (one-time setup)
- After scanning, messages will be sent automatically

## ⏰ Scheduling Options

You can modify the schedule in `whatsapp_bot.py`:

```python
# Every 30 minutes (default)
schedule.every(30).minutes.do(send_whatsapp_message)

# Every hour
schedule.every().hour.do(send_whatsapp_message)

# Every 5 minutes
schedule.every(5).minutes.do(send_whatsapp_message)

# Daily at specific time
schedule.every().day.at("09:00").do(send_whatsapp_message)
```

## 💡 Tips

✅ **Requirements:**
- Keep your system awake (not in sleep mode)
- Stay logged into WhatsApp Web
- Maintain stable internet connection

💡 **Message Generation:**

The bot automatically generates unique messages each time using:
- **LM Studio (Local)**: AI-generated messages using your local LLM (free, no API key needed) - **Default**
- **OpenAI (Cloud)**: AI-generated personalized messages (requires API key)
- **Templates**: Simple template-based messages (no API key needed)

Each message is unique and personalized based on your configuration!

**Priority Order:**
1. LM Studio (if running and enabled)
2. OpenAI (if API key is set and LM Studio is disabled/failed)
3. Template-based (fallback)

## 🔄 Multiple Contacts

To send to multiple contacts, modify the script:

```python
contacts = ["+1234567890", "+1987654321"]

def send_to_all():
    for number in contacts:
        pywhatkit.sendwhatmsg_instantly(number, "Hello!", tab_close=True)
```

## ⚠️ Important Notes

- This bot uses WhatsApp Web, so your computer must be running
- Make sure WhatsApp Web is logged in before running the bot
- The bot will open a browser window - don't close it manually
- Use responsibly and in accordance with WhatsApp's terms of service

## 🛑 Stopping the Bot

Press `Ctrl+C` in the terminal to stop the bot.

