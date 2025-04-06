import requests
from msal import ConfidentialClientApplication

import os
from dotenv import load_dotenv
load_dotenv()

class SendEmail:
    def __init__(self):
        # === CONFIG ===
        self.CLIENT_ID = os.environ.get("EMAIL_CLIENT_ID")
        self.TENANT_ID = os.environ.get("AZURE_TENANT_ID")
        self.CLIENT_SECRET = os.environ.get("EMAIL_SECRET_VALUE")
        self.AUTHORITY = f'https://login.microsoftonline.com/{self.TENANT_ID}'
        self.SCOPE = ["https://graph.microsoft.com/.default"]

        self.EMAIL_FROM = 'jinesh.ks@tralpine.com'
        # === AUTH ===
        self.app = ConfidentialClientApplication(self.CLIENT_ID, authority=self.AUTHORITY, client_credential=self.CLIENT_SECRET)

    def sendTextMessage(self, email_to, email_from="noreply@tralpine.com", subject="Test Email from Python via Microsoft Graph", content="Hello from Python using Microsoft Graph API!"):
        result = None
        try:
            result = self.app.acquire_token_for_client(scopes=self.SCOPE)

            # === SEND EMAIL ===
            if 'access_token' in result:
                access_token = result['access_token']

                email_msg = {
                    "message": {
                        "subject": subject,
                        "body": {
                            "contentType": "Text",
                            "content": content
                        },
                        "toRecipients": [
                            {
                                "emailAddress": {
                                    "address": email_to
                                }
                            }
                        ]
                    }
                }

                response = requests.post(
                    url=f"https://graph.microsoft.com/v1.0/users/{email_from}/sendMail",  # Use the sender's email directly
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    },
                    json=email_msg
                )


                if response.status_code == 202:
                    print("✅ Email sent successfully!")
                    return True
                else:
                    print(f"❌ Failed to send email: {response.status_code} - {response.text}")
                    return False
            else:
                print("❌ Authentication failed.")
                return False
        except Exception as e:
            print (e)
            return False


if __name__ == "__main__":
    sendEmail = SendEmail()
    sendEmail.sendTextMessage("jinesh.bond@gmail.com", email_from="jinesh.ks@tralpine.com", subject="Test email", content="Test content")