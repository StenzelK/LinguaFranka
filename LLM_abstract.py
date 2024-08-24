import yaml
from API_interfaces.GPT_tools import (
    gpt_get_chat_initialise,
    gpt_guess_lang,
    gpt_get_chat_response,
    gpt_get_user_comment,
    gpt_get_bot_explain,
    gpt_get_bot_answer
)
from API_interfaces.gemini_tools import (
    gemini_get_chat_initialise,
    gemini_guess_lang,
    gemini_get_chat_response,
    gemini_get_user_comment,
    gemini_get_bot_explain,
    gemini_get_bot_answer
)
# from API_interfaces.llama_tools import (
#     llama_get_chat_initialise,
#     llama_guess_lang,
#     llama_get_chat_response,
#     llama_get_user_comment,
#     llama_get_bot_explain,
#     llama_get_bot_answer
# )
# from API_interfaces.claude_tools import (
#     claude_get_chat_initialise,
#     claude_guess_lang,
#     claude_get_chat_response,
#     claude_get_user_comment,
#     claude_get_bot_explain,
#     claude_get_bot_answer
# )

def load_llm_select():
    return yaml.safe_load(open('config.yaml'))['settings']['llm_select']

def llm_function_dispatcher(function_map, *args):
    llm_select = load_llm_select()
    return function_map.get(llm_select, lambda *args: "Method not implemented")(*args)

def llm_guess_lang(name):
    switch = {
        "gpt-3": gpt_guess_lang,
        "gemini": gemini_guess_lang,
        # "llama": llama_guess_lang,
        # "claude": claude_guess_lang,
    }
    return llm_function_dispatcher(switch, name)

def llm_get_chat_initialise(context, practice_lang, persona, user_profile, practice_lang_prof, desired_scenario):
    switch = {
        "gpt-3": gpt_get_chat_initialise,
        "gemini": gemini_get_chat_initialise,
        # "llama": llama_get_chat_initialise,
        # "claude": claude_get_chat_initialise,
    }
    return llm_function_dispatcher(switch, context, practice_lang, persona, user_profile, practice_lang_prof, desired_scenario)

def llm_get_chat_response(context, practice_lang, persona, user_profile, practice_lang_prof, desired_scenario):
    switch = {
        "gpt-3": gpt_get_chat_response,
        "gemini": gemini_get_chat_response,
        # "llama": llama_get_chat_response,
        # "claude": claude_get_chat_response,
    }
    return llm_function_dispatcher(switch, context, practice_lang, persona, user_profile, practice_lang_prof, desired_scenario)

def llm_get_user_comment(prompt, practice_lang, user_lang):
    switch = {
        "gpt-3": gpt_get_user_comment,
        "gemini": gemini_get_user_comment,
        # "llama": llama_get_user_comment,
        # "claude": claude_get_user_comment,
    }
    return llm_function_dispatcher(switch, prompt, practice_lang, user_lang)

def llm_get_bot_explain(prompt, practice_lang, user_lang):
    switch = {
        "gpt-3": gpt_get_bot_explain,
        "gemini": gemini_get_bot_explain,
        # "llama": llama_get_bot_explain,
        # "claude": claude_get_bot_explain,
    }
    return llm_function_dispatcher(switch, prompt, practice_lang, user_lang)

def llm_get_bot_answer(prompt, practice_lang, user_lang):
    switch = {
        "gpt-3": gpt_get_bot_answer,
        "gemini": gemini_get_bot_answer,
        # "llama": llama_get_bot_answer,
        # "claude": claude_get_bot_answer,
    }
    return llm_function_dispatcher(switch, prompt, practice_lang, user_lang)