#!/usr/bin/env python3
"""
Test script to verify Resend API is working
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print(f"✓ Loaded .env from {dotenv_path}")
else:
    print(f"✗ .env file not found at {dotenv_path}")
    sys.exit(1)

# Check Resend configuration
RESEND_API_KEY = os.getenv('RESEND_API_KEY')
RESEND_FROM_EMAIL = os.getenv('RESEND_FROM_EMAIL')

print(f"\n[CONFIG]")
print(f"  RESEND_API_KEY: {'****' + RESEND_API_KEY[-10:] if RESEND_API_KEY else 'NOT SET'}")
print(f"  RESEND_FROM_EMAIL: {RESEND_FROM_EMAIL}")

if not RESEND_API_KEY:
    print("\n✗ RESEND_API_KEY not configured in .env")
    sys.exit(1)

# Test Resend API
print(f"\n[TESTING RESEND API]")
try:
    import resend
    resend.api_key = RESEND_API_KEY
    
    # Send test email
    test_recipient = "hostelconnect05@gmail.com"  # Must be the registered Resend account email
    
    print(f"  Sending test email to: {test_recipient}")
    
    email = resend.Emails.send({
        "from": "delivery@resend.dev",
        "to": test_recipient,
        "subject": "🧪 HostelConnect Email Test",
        "html": """
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #3b82f6;">✅ Email Service Working!</h2>
            <p>This is a test email from HostelConnect using Resend API.</p>
            <p>If you received this email, the email service is working correctly.</p>
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">
            <p style="font-size: 12px; color: #9ca3af;">Test sent on: """ + str(__import__('datetime').datetime.now()) + """</p>
        </body>
        </html>
        """
    })
    
    message_id = email.get('id')
    
    if message_id:
        print(f"  ✓ Email sent successfully!")
        print(f"  Message ID: {message_id}")
        print(f"\n[SUCCESS] Resend API is working correctly!")
        print(f"Check your email inbox for the test message.")
    else:
        error = email.get('message', 'Unknown error')
        print(f"  ✗ Failed to send email: {error}")
        print(f"\n[FAILED] Resend API returned an error")
        sys.exit(1)
        
except ImportError:
    print("  ✗ resend module not installed")
    print("  Install it with: pip install resend")
    sys.exit(1)
except Exception as e:
    print(f"  ✗ Exception occurred: {type(e).__name__}: {str(e)}")
    print(f"\n[FAILED] Error testing Resend API")
    sys.exit(1)
