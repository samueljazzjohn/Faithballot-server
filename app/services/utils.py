import re
import json

from app.helpers.logger import logger

def sanitize_and_parse_json(gpt_response_intent_content):
    # Remove control characters from the content
    sanitized_content = re.sub(r'[\x00-\x1F\x7F]', '', gpt_response_intent_content)

    # Regular expression to extract JSON-like objects
    json_match = re.search(r'{(?:[^{}]|(?:\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\}))*}', sanitized_content)


    if json_match:
        extracted_json = json_match.group(0)

        try:
            parsed_json = json.loads(extracted_json)

            # Return the message property if it exists, otherwise check output.message
            return parsed_json
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON: {e}")  # Raise ValueError with the JSON decode error
    else:
        raise ValueError("No JSON object found in the sanitized content.")