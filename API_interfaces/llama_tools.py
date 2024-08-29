import json
from pprint import pprint
from llamaapi import LlamaAPI
import requests
import yaml
from API_interfaces.common import SYSTEM_PROMPT_MAIN, SYSTEM_PROMPT_TEACHER, get_bot_answer, get_bot_explain, get_chat_initialise, get_chat_response, get_user_comment, stringify_log
from API_keys import LLAMA_API


def _query(context):

    try:
        llama = LlamaAPI(LLAMA_API)
        api_request_json = {
        "messages": context
        }
        
        return llama.run(api_request_json)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return "API Error"
    # """ Send a prompt to the Meta AI API and return the response. """
    # # Set the API endpoint and API key for the Meta AI API
    # endpoint = "https://api.meta.com/v1/models/llama-2/complete"


    # try:
    #     print(f'Context: {type(context)}')
    #     pprint(context)
    #     headers = {
    #         "Authorization": f"Bearer {LLAMA_API}",
    #         "Content-Type": "application/json"
    #     }
    #     data = {
    #         "prompt": stringify_log(context),
    #         "max_tokens": yaml.safe_load(open('config.yaml'))['settings']['user_token_limit']
    #     }
    #     response = requests.post(endpoint, headers=headers, json=data)
    #     response.raise_for_status()  # Raise an exception for bad status codes

    #     return response.json()["completion"]


    
    
def llama_guess_lang(name):
    system_prompt = (
        f"{SYSTEM_PROMPT_MAIN}"
        "You are a part of a larger system tasked with language identification. "
        "You've been called because the user input did not match any of the ISO-639-1 fields. "
        "It is possible the user made a typo or used a description instead of the name, make an educated guess, "
        "it's ok if your guess is not correct. It's possible the requested language is not a part of ISO-639-1, "
        "it might be a conlang. You will be provided with the user input. Your goal is to identify the language based "
        "on the information in the user prompt. This is not a critical system, prioritize false positives. "
        "Your goal is to identify the language based on what user wants. For example if the input says 'Japanisch' the indentified language is Japanese not German. "
        "Similarly, if the input says 'niemiecki', the identified language should be German."
        "Return ONLY the name of the language or 'NoLang' if you're unable to identify the language. "
        "This is an automated prompt. Your response will be passed to a function that expects a single word. "
        "Do not include any commentary besides the name of the language or 'NoLang'"
        f"User input:'{name}'"
    )
    
    print(f"Guess lang prompt: {system_prompt}")
    
    response = _query([{"role": "user", "content": system_prompt}])
    
    print(f"guess lang: {response}")
    
    return response
    
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
