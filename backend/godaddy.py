import requests
import os
from dotenv import load_dotenv

load_dotenv()

class GoDaddy:
    def __init__(self):
        godaddy_api_key = os.environ.get("GODADDY_KEY")
        godaddy_api_secret = os.environ.get("GODADDY_SECRET")
        self.godaddy_base_url = os.environ.get("GODADDY_BASE_URL")
        print(godaddy_api_key, godaddy_api_secret, self.godaddy_base_url )
        self.header = {
                            "Authorization": f"sso-key {godaddy_api_key}:{godaddy_api_secret}",
                            "Content-Type": "application/json"
                        }
        self.domain = "tralpine.com"

    def get_record(self, subdomain):
        resp = requests.get(
                        f"{self.godaddy_base_url}/v1/domains/{self.domain}/records/CNAME",
                        headers=self.header,
                    )
        print(resp)

if __name__ == "__main__":
    goDaddy = GoDaddy()
    goDaddy.get_record("appx")
