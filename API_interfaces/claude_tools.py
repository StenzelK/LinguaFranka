import anthropic
import requests
import json


from API_interfaces.common import SYSTEM_PROMPT_MAIN, SYSTEM_PROMPT_TEACHER, get_bot_answer, get_bot_explain, get_chat_initialise, get_chat_response, get_user_comment
from API_keys import CLAUDE_API

def replace_system_with_assistant(context):
    for item in context:
        if item['role'] == 'system':
            item['role'] = 'assistant'
    return context

def _query(context):

    #print('Claude call')
    context = replace_system_with_assistant(context)
    try:
        client = anthropic.Anthropic(
        api_key=CLAUDE_API,)

        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            messages=context
        )   
        
        
        
        return message.content[0].text
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return "API Error"

def claude_guess_lang(name):
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

claude_get_chat_initialise = construct_chat_prompt(get_chat_initialise)
# def claude_get_chat_initialise(context, practice_lang, persona, user_profile, practice_lang_prof, desired_scenario):
#     """This is the beginning of the conversation."""
#     pass

claude_get_chat_response = construct_chat_prompt(get_chat_response)
# def claude_get_chat_response(context, practice_lang, persona, user_profile, practice_lang_prof, desired_scenario):
#     """Continue the conversation based on the user's input."""
#     pass

claude_get_user_comment = construct_teacher_prompt(get_user_comment)
# def claude_get_user_comment(prompt, practice_lang, user_lang):
#     """User requested your commentary on a text they wrote. Analyse it, point out and explain potential mistakes (gramatical, orthographical, typos etc.), suggest improvements etc. The text is assumed to be in the practice language."""
#     pass

claude_get_bot_answer = construct_teacher_prompt(get_bot_answer)
# def claude_get_bot_answer(prompt, practice_lang, user_lang):
#     """User requested your assistance in a subject they struggle with. Provide an answer to the user's question."""
#     pass

claude_get_bot_explain = construct_teacher_prompt(get_bot_explain)
# def claude_get_bot_explain(prompt, practice_lang, user_lang):
#     """User requested your assistance in a subject they struggle with. You will be provided with an AI generated text. User has troubles understanding it. Format it as an HTML div tree. 
#     Respond with the original text translated into the user's native language, followed by the explanation of the sentence structure, grammar etcs"""
#     pass
