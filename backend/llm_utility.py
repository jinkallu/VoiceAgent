import requests

class LLMUtility:
    def call_4o(self, data):
        api_url = "https://ai-jineshks5663ai187603290877.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview"
        api_key = "8Zms47s4V1kBOKonmuISNgOngZPjApmpI5rElTdgXEg9jCcKIrq0JQQJ99BCACfhMk5XJ3w3AAAAACOGcEbH"

        # Prepare headers and data
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key
        }
        # Make the POST request
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", None)

            return content
        
    def troubelshooting_step1(self, query):
        system_message = """
            You are a technical documentation assistant.

            You will receive raw, unstructured text extracted from a PDF manual or troubleshooting guide. Your job is to read and analyze this text to identify useful and practical troubleshooting problems.

            ❌ Do NOT include:
            - Legal disclaimers
            - Battery warnings
            - Safety notices that do not involve problem-solving
            - Generic installation instructions unless they are part of a problem

            ✅ DO include:
            - Real-world issues users might face (e.g., device not turning on, paper jam, Wi-Fi not connecting)
            - Specific error messages that require action
            - Any described symptoms that can be mapped to a problem

            🧠 Reason about *implied* problems too — not just ones directly mentioned.

            🎯 Format the response as clean JSON:
            [
            {
                "problem": "<Describe the user-facing issue or symptom>"
            },
            ...
            ]

            Be specific, concise, and avoid repetition, find as many problems as possible.
        """.strip()

        data = {
            "messages": [
                {
                    "role": "system", 
                    "content": system_message
                },
                {
                    "role": "user", 
                    "content": query
                }
            ],
            "temperature": 0.2,
            "seed": 1
        }
        return self.call_4o (data)
    
    def troubelshooting_step2(self, query, problems):
        system_message = f"""
            You are a technical documentation assistant.

            You will receive raw, unstructured text extracted from a PDF manual or troubleshooting guide. Your job is to read and analyze this text to identify useful and practical troubleshooting problems.

            In a previous step, an LLM identifies following problems : {problems}, check them against the document and add missing problems, update or delete duplicates as necessary.

            🧠 Reason about *implied* problems too — not just ones directly mentioned.

            🎯 Format the response as clean JSON:
            [
            {{
                "problem": 'Describe the user-facing issue or symptom'
            }},
            ...
            ]

            Be specific, concise, and avoid repetition, find as many problems as possible.
        """.strip()

        data = {
            "messages": [
                {
                    "role": "system", 
                    "content": system_message
                },
                {
                    "role": "user", 
                    "content": query
                }
            ],
            "temperature": 0.2,
            "seed": 1
        }
        return self.call_4o (data)
    
    def troubelshooting_step3(self, query, problems):
        system_message = f"""
            You are a technical documentation assistant.

            You will receive raw, unstructured text extracted from a PDF manual or troubleshooting guide. Your job is to read and analyze this text to identify useful and practical troubleshooting problems.

            In a previous step, an LLM identifies following problems : {problems}, check them against the document and add solutions steps to the corresponding problems.

            🧠 Reason about *implied* problems too — not just ones directly mentioned.

            🎯 Format the response as clean JSON:
            [
            {{
                "problem": 'Describe the user-facing issue or symptom',
                "solution steps": [<Explain the step-by-step solution or instructions if available>]
            }},
            ...
            ]

            Be specific, concise, and avoid repetition, find as many problems as possible.
        """.strip()

        data = {
            "messages": [
                {
                    "role": "system", 
                    "content": system_message
                },
                {
                    "role": "user", 
                    "content": query
                }
            ],
            "temperature": 0.2,
            "seed": 1
        }
        return self.call_4o (data)
    
    def howto_step1(self, query):
        system_message = """
            You are a technical documentation assistant.

            You will receive raw, unstructured text extracted from a PDF manual or troubleshooting guide. Your job is to read and analyze this text to identify useful and practical how-to problems.

            ❌ Do NOT include:
            - Legal disclaimers
            - Battery warnings
            - Safety notices that do not involve how-to solving
            - Generic installation instructions unless they are part of a how-to problem

            ✅ DO include:
            - Real-world how-to issues users might face (e.g., how to turn on device, how to solve paper jam, how to connect to Wi-Fi network)
            - Specific error messages that require action
            - Any described symptoms that can be mapped to a how-to problem

            🧠 Reason about *implied* how-to problems too — not just ones directly mentioned.

            🎯 Format the response as clean JSON:
            [
            {
                "problem": "<Describe the user-facing how-to issue>",
            },
            ...
            ]

            Be specific, concise, and avoid repetition, find as many how-to problems as possible.
        """.strip()

        data = {
            "messages": [
                {
                    "role": "system", 
                    "content": system_message
                },
                {
                    "role": "user", 
                    "content": query
                }
            ],
            "temperature": 0.2,
            "seed": 1
        }
        return self.call_4o (data)