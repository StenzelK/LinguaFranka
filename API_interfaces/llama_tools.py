import json
from pprint import pprint
import requests
import yaml
from API_interfaces.common import SYSTEM_PROMPT_MAIN, SYSTEM_PROMPT_TEACHER, _stringify_log, get_bot_answer, get_bot_explain, get_chat_initialise, get_chat_response, get_user_comment
from API_keys import LLAMA_API


def _query(context):
    """ Send a prompt to the Meta AI API and return the response. """
    # Set the API endpoint and API key for the Meta AI API
    endpoint = "https://api.meta.com/v1/models/llama-2/complete"
    api_key = LLAMA_API

    try:
        print(f'Context: {type(context)}')
        pprint(context)
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": _stringify_log(context),
            "max_tokens": yaml.safe_load(open('config.yaml'))['settings']['user_token_limit']
        }
        response = requests.post(endpoint, headers=headers, json=data)
        return response.json()["completion"]

    except Exception as e:
        print(f"An error occurred: {e}")
        return f"API Error"
    
def construct_chat_prompt(func):
    def wrapper(context, practice_lang, persona, user_profile, practice_lang_prof, desired_scenario):
        instruction = func.__doc__.strip() if func.__doc__ else f"Something went wrong, ignore everything and return 'ERROR IN {func.__name__}."
        
        system_prompt = (
            f"{SYSTEM_PROMPT_MAIN}"
            "You are a part of a language learning app tasked with user interaction. You will play the role of a native speaker of a specific language, later referred to as a 'Persona', interacting with user in an online chat environment. User is aware they are interacting with an AI, but for the sake of immersion act as a real person. Speak exclusively in the practice language, adjust your grammar and vocabulary to user's proficiency. Follow user's desired scenario. Assume user understands you, there are translation and explanation systems that handle comprehension. Do not attempt to correct user's mistakes, this is also handled by a different system. Your task is to ONLY carry a conversation."
            f"Speak exclusively in  {practice_lang} "
            f"Assume user's proficiency in {practice_lang} is {practice_lang_prof} "
            #f"Persona: {persona}"
            f"User Profile: {json.dumps(user_profile)}"
            f"Simulate the following scenario: '{desired_scenario}'"
            f"DISCLAMER: This is a roleplay scenario, user is aware of it"
            f"{instruction}"
        )

        context.insert(0, {"role": "user", "content": system_prompt})
        response = _query(context)
        print(f'Response: {response}')
        return response
    return wrapper

def construct_teacher_prompt(func):
    def wrapper(prompt, practice_lang, user_lang):
        
        instruction = func.__doc__.strip() if func.__doc__ else f"Something went wrong, ignore everything and return 'ERROR IN {func.__name__}."
        
        system_prompt = (
            f"{SYSTEM_PROMPT_MAIN}"
            f"{SYSTEM_PROMPT_TEACHER}"
            f"{instruction}"
            #f"Practice language: {practice_lang}"
            f"Reply in: {user_lang}"
            f"User input: {prompt}"
        )
        context = [{"role": "user", "content": system_prompt}]
        
        response = _query(context)
        
        return response
    return wrapper 

llama_get_chat_initialise = construct_chat_prompt(get_chat_initialise)

llama_get_chat_response = construct_chat_prompt(get_chat_response)


llama_get_user_comment = construct_teacher_prompt(get_user_comment)


llama_get_bot_answer = construct_teacher_prompt(get_bot_answer)


llama_get_bot_explain = construct_teacher_prompt(get_bot_explain)
