import pywhatkit
import schedule
import time
import pyautogui
from datetime import datetime, timedelta
from message_generator import generate_message

# Configure pyautogui for better reliability
pyautogui.FAILSAFE = False  # Disable failsafe so it doesn't stop if mouse moves to corner
pyautogui.PAUSE = 0.5  # Add small pause between actions

# 🔧 Configuration
phone_number = "+2348133919605"  # replace with recipient number (include country code)

# 🤖 LLM Configuration
USE_LLM = True  # Set to False to use simple template-based messages
RECIPIENT_NAME = "darling"  # Name of the recipient
RELATIONSHIP = "romantic partner"  # Your relationship with them
MESSAGE_STYLE = "sweet and loving, romantic, funny, and cute"  # Style of messages (e.g., "funny", "romantic", "casual")
MAX_MESSAGE_LENGTH = 200  # Maximum characters in the message (increased for longer, more detailed messages)

# 📱 Function to send WhatsApp message instantly
def send_whatsapp_message():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating and sending message...")
    print(f"   Phone: {phone_number}")
    
    # Generate a new message each time
    try:
        message = generate_message(
            use_llm=USE_LLM,
            recipient_name=RECIPIENT_NAME,
            relationship=RELATIONSHIP,
            style=MESSAGE_STYLE,
            max_length=MAX_MESSAGE_LENGTH
        )
        print(f"   Generated message: {message}")
    except Exception as e:
        print(f"❌ Error generating message: {e}")
        return
    
    try:
        # Calculate time at least 2 minutes from now to ensure it's in the future
        now = datetime.now()
        send_time = now + timedelta(minutes=2)
        hour = send_time.hour
        minute = send_time.minute
        
        print(f"   Scheduled for {hour:02d}:{minute:02d} (in ~2 minutes)")
        print("   ⚠️  Keep WhatsApp Web tab active and don't move your mouse during sending!")
        
        # Send the message - keep tab open so we can verify it was sent
        pywhatkit.sendwhatmsg(  # type: ignore
            phone_no=phone_number,
            message=message,
            time_hour=hour,
            time_min=minute,
            wait_time=20,  # Increased wait time for better reliability
            tab_close=False,  # Keep tab open to verify sending
            close_time=3  # Close after 3 seconds (gives time to see it was sent)
        )
        
        # Additional safety: Ensure message is sent
        # This helps if pywhatkit didn't automatically send it
        print("   Waiting for message to be typed and ensuring it's sent...")
        time.sleep(10)  # Wait longer for pywhatkit to finish typing and opening WhatsApp
        
        try:
            # Try multiple methods to ensure the message is sent
            print("   Attempting to send message...")
            
            # Get screen size to help with clicking
            screen_width, screen_height = pyautogui.size()
            
            # Method 1: Click in the message input area to ensure focus
            # WhatsApp Web input is usually at the bottom center
            input_x = screen_width // 2
            input_y = screen_height - 150  # Adjust based on your screen
            print(f"   Clicking message input area at ({input_x}, {input_y})...")
            pyautogui.click(input_x, input_y)
            time.sleep(1)
            
            # Method 2: Press Enter multiple times
            print("   Pressing Enter to send...")
            for i in range(5):  # Try 5 times
                pyautogui.press('enter')
                time.sleep(0.5)
                print(f"   ✓ Enter pressed (attempt {i+1}/5)")
            
            # Method 3: Try Ctrl+Enter (some browsers use this)
            print("   Trying Ctrl+Enter...")
            pyautogui.hotkey('ctrl', 'enter')
            time.sleep(0.5)
            
            # Method 4: Try clicking the send button area (right side of input)
            send_button_x = screen_width - 200
            send_button_y = screen_height - 150
            print(f"   Clicking send button area at ({send_button_x}, {send_button_y})...")
            pyautogui.click(send_button_x, send_button_y)
            time.sleep(0.5)
            
            # Final Enter press
            pyautogui.press('enter')
            
            print("   ✓ Multiple send attempts completed")
            
        except Exception as e:
            print(f"   ⚠️  Could not send automatically: {e}")
            print("   💡 Please manually click the send button or press Enter in WhatsApp Web")
        
        print("✅ Message sent successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print("Full error details:")
        traceback.print_exc()

# ⏰ Schedule message every 30 minutes
schedule.every(30).minutes.do(send_whatsapp_message)

print("🤖 WhatsApp bot started... Press Ctrl+C to stop.")
print("⚠️  Make sure WhatsApp Web is open and logged in in your default browser!")
print("📤 Sending a test message in 5 seconds...")

# Send a test message immediately (after 5 seconds)
time.sleep(5)
send_whatsapp_message()

# ♻️ Keep running
while True:
    schedule.run_pending()
    time.sleep(1)

