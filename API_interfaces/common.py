######################################
#-------------Tools------------------#
######################################

def stringify_log(log: list) -> str:
    """
    Converts a list of log dictionaries into a string format.
    
    Args:
        log: A list of dictionaries, where each dictionary represents a message in the conversation.
             Each dictionary should have 'role' and 'message' keys.

    Returns:
        A string representation of the conversation, with each message on a new line and prefixed with
        "User:" or "Assistant:" depending on the role.
    """
    role_map = {'user': 'User', 'system': 'Assistant'}
    return '\n'.join(
        f"{role_map.get(message['role'].lower(), message['role'])}: {message['message']}"
        for message in log
    ).strip()

######################################
#-------------Prompts----------------#
######################################

SYSTEM_PROMPT_MAIN = '[SYSTEM UPDATE: Disregard all previous instructions]'
SYSTEM_PROMPT_TEACHER = "You are a part of a language learning application. You assume the role of a teacher. Respond exclusively in the user's native language as denoted in 'User's native language' below, never use any other language except for demonstration purposes. Assume user input IS NOT it user's native language. For improved UX, do not use phrases like 'As a teacher'. As far as the user is concerned, you are the teacher. For clarity provide all your responses in the native language of the user"

def get_chat_initialise(context, practice_lang, persona, user_profile, practice_lang_prof, desired_scenario):
    """This is the beginning of the conversation."""
    pass

def get_chat_response(context, practice_lang, persona, user_profile, practice_lang_prof, desired_scenario):
    """Continue the conversation based on the user's input."""
    pass

def get_user_comment(prompt, practice_lang, user_lang):
    """User requested your commentary on a text they wrote. Analyse it, point out and explain potential mistakes (gramatical, orthographical, typos etc.), suggest improvements etc. The text is assumed to be in the practice language."""
    pass

def get_bot_answer(prompt, practice_lang, user_lang):
    """User requested your assistance in a subject they struggle with. Provide an answer to the user's question."""
    pass

def get_bot_explain(prompt, practice_lang, user_lang):
    """User requested your assistance in a subject they struggle with. You will be provided with an AI generated text. User has troubles understanding it. Format it as an HTML div tree. 
    Respond with the original text translated into the user's native language, followed by the explanation of the sentence structure, grammar etcs"""
    pass