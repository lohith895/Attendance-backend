import os

try:
    from twilio.rest import Client  # type: ignore
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False

def send_whatsapp_alert(teacher_phone: str, parent_phone: str, student_name: str, subject_name: str, subject_code: str):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    
    # Format message body
    body = f"Dear Parent, {student_name} was marked ABSENT for {subject_name} ({subject_code}) today. - Sender: Professor (WhatsApp: {teacher_phone})"
    
    # Clean phone numbers (must start with + for Twilio WhatsApp compatibility)
    t_phone = teacher_phone if teacher_phone.startswith("+") else f"+{teacher_phone.strip()}"
    p_phone = parent_phone if parent_phone.startswith("+") else f"+{parent_phone.strip()}"
    
    if account_sid and auth_token and not account_sid.startswith("your_") and TWILIO_AVAILABLE:
        try:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                from_=f"whatsapp:{t_phone}",
                body=body,
                to=f"whatsapp:{p_phone}"
            )
            print(f"[TWILIO ALERT] WhatsApp message sent from {t_phone} to {p_phone}. SID: {message.sid}")
            return {"success": True, "sid": message.sid, "mode": "live"}
        except Exception as e:
            print(f"[TWILIO ERROR] Failed to send WhatsApp message: {str(e)}")
            # Fallback to simulation
            
    # Simulation mode
    log_line = f"=== WhatsApp Alert (Simulated) ===\nFrom (Teacher): {t_phone}\nTo (Parent): {p_phone}\nMessage: {body}\n==================================\n"
    print(log_line)
    
    try:
        with open("sms_logs.txt", "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception:
        pass
        
    return {"success": True, "mode": "simulated", "message": body}
