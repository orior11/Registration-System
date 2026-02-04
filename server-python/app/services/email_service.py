from typing import Optional
from app.config import settings


async def send_reset_code(email: str, code: str) -> bool:
    """
    Send password reset code via email
    
    Args:
        email: Recipient email address
        code: 6-digit reset code
        
    Returns:
        True if sent successfully, False otherwise
    """
    subject = "Password Reset Code"
    body = f"""
    <html>
    <body>
        <h2>Password Reset Request</h2>
        <p>Your password reset code is:</p>
        <h1 style="color: #3B4CB8; letter-spacing: 5px;">{code}</h1>
        <p>This code will expire in 15 minutes.</p>
        <p>If you didn't request this, please ignore this email.</p>
    </body>
    </html>
    """
    
    if settings.EMAIL_SERVICE == "console":
        # For development - just print to console
        print(f"\n{'='*50}")
        print(f"[EMAIL] TO: {email}")
        print(f"[EMAIL] SUBJECT: {subject}")
        print(f"[EMAIL] RESET CODE: {code}")
        print(f"[EMAIL] EXPIRES IN: 15 minutes")
        print(f"{'='*50}\n")
        return True
    
    elif settings.EMAIL_SERVICE == "azure":
        # Azure Communication Services implementation
        try:
            from azure.communication.email import EmailClient
            
            if not settings.AZURE_COMMUNICATION_CONNECTION_STRING:
                print("[WARNING] Azure Communication connection string not configured")
                return False
            
            client = EmailClient.from_connection_string(
                settings.AZURE_COMMUNICATION_CONNECTION_STRING
            )
            
            message = {
                "senderAddress": settings.FROM_EMAIL,
                "recipients": {
                    "to": [{"address": email}]
                },
                "content": {
                    "subject": subject,
                    "html": body
                }
            }
            
            poller = client.begin_send(message)
            result = poller.result()
            
            print(f"[OK] Email sent to {email} via Azure")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to send email via Azure: {e}")
            return False
    
    elif settings.EMAIL_SERVICE == "sendgrid":
        # SendGrid implementation
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail
            
            if not settings.SENDGRID_API_KEY:
                print("[WARNING] SendGrid API key not configured")
                return False
            
            message = Mail(
                from_email=settings.FROM_EMAIL,
                to_emails=email,
                subject=subject,
                html_content=body
            )
            
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            
            print(f"[OK] Email sent to {email} via SendGrid")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to send email via SendGrid: {e}")
            return False
    
    else:
        print(f"[ERROR] Unknown email service: {settings.EMAIL_SERVICE}")
        return False


async def send_welcome_email(email: str, name: str) -> bool:
    """
    Send welcome email to new user
    
    Args:
        email: User's email address
        name: User's name
        
    Returns:
        True if sent successfully
    """
    subject = "Welcome to Our Platform!"
    body = f"""
    <html>
    <body>
        <h2>Welcome {name}!</h2>
        <p>Thank you for registering with us.</p>
        <p>We're excited to have you on board.</p>
    </body>
    </html>
    """
    
    if settings.EMAIL_SERVICE == "console":
        print(f"\n{'='*50}")
        print(f"[EMAIL] WELCOME EMAIL TO: {email}")
        print(f"[EMAIL] NAME: {name}")
        print(f"{'='*50}\n")
        return True
    
    # Add actual email sending logic here similar to send_reset_code
    return True
