import re
import sys
import json
from g4f import ChatCompletion
import g4f.models
import time

g4f.debug.logging = False  # Enable logging
g4f.check_version = False  # Disable automatic version checking


def generate_gpt_response(in_provider, input_message):
    providers = {'you': g4f.Provider.You, 'bing': g4f.Provider.Bing}

    # Convert the provider name to lowercase for case-insensitive comparison
    lower_cased_provider = in_provider.lower()

    # Check if the provided provider is in the dictionary
    if lower_cased_provider not in providers:
        raise ValueError(f"Invalid provider: {in_provider}")

    # Set the provider based on the dictionary
    selected_provider = providers[lower_cased_provider]

    # Use the selected provider in ChatCompletion.create
    res = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": input_message}],
        stream=True,
        provider=selected_provider
    )

    result_str = []
    for mess in res:
        if isinstance(mess, str):  # Check if it's a string response
            result_str.append(mess)
        elif isinstance(mess, dict) and 'mimetype' in mess and 'content' in mess:
            if mess['mimetype'] == 'text/plain':
                result_str.append(mess['content'])
        # Handle other mimetypes if needed

    # convert list to string
    result_str = ''.join(result_str)

    # remove unwanted patterns
    result_str = re.sub(r'\[[0-9]+]: https://[^\s]+ ""\n', '', result_str)

    # remove code block
    result_str = re.sub(r"```[^\S\r\n]*[a-z]*\n.*?\n```", '', result_str, 0, re.DOTALL)

    result_str = result_str.split('\n\n', 1)[0]
    result_str = result_str.split('\n- ')
    return result_str



