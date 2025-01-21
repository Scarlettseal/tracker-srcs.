import random
import string
import requests

# Replace with your webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1304918942686380113/3DIOQcY7w1WZJFuScR9MAFNLcasn87q1_r_XGFZepgZac6DQRIwPbqgtGzE5XiyXLeS5"

def generate_random_code(length=100):
    # Choose random uppercase letters and digits for the code
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_random_codes(number=100, length=4):
    # Generate a list of random codes
    return [generate_random_code(length) for _ in range(number)]

def send_codes_to_webhook(codes):
    # Format the codes into a message
    message = "codes:\n" + "\n".join(codes)
    
    # Create the payload
    payload = {
        "content": message
    }
    
    # Send the request to the webhook
    response = requests.post(WEBHOOK_URL, json=payload)
    
    # Check for errors
    if response.status_code == 204:
        print("Codes sent successfully!")
    else:
        print(f"Failed to send codes: {response.status_code} - {response.text}")

# Generate random codes
random_codes = generate_random_codes()

# Send codes to the webhook
send_codes_to_webhook(random_codes)
