import html
import json
import locale
import os
import re
import httpx
import yaml
from LLM_abstract import llm_get_bot_answer, llm_get_bot_explain, llm_get_chat_initialise, llm_get_chat_response, llm_get_user_comment, llm_guess_lang
from GPT_tools import gpt_get_chat_initialise, gpt_guess_lang, gpt_get_chat_response, gpt_get_user_comment, gpt_get_bot_explain, gpt_get_bot_answer
import tiktoken
from iso639 import languages


def load_config():
    """ Load the YAML configuration file. """
    file_path = "config.yaml"
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
        return config

def get_system_language_iso_639_1():
    # Set the locale to the user's default setting (typically from the LANG environment variable)
    locale.setlocale(locale.LC_ALL, '')
    
    # Get the default locale information
    default_locale = locale.getdefaultlocale()
    
    # The first part of the locale tuple is the language and country code
    # Example output: ('en_US', 'UTF-8')
    lang_country_code = default, encoding = default_locale
    
    # Extract the language code (first two letters before underscore)
    language_code_iso_639_1 = default[:2] if default else None
    
    return language_code_iso_639_1

def get_global_translation(target_lang):
    """
    Load the 'en.json' file, translate its content except for blacklisted keys, 
    and save the result to a new JSON file named as '<target_lang>.json'.

    Args:
    target_lang (str): The language code to translate the content into.
    blacklist (list): List of keys to skip during translation.
    """
    base_dir = 'translations'
    input_file_path = f'{base_dir}/en.json'
    output_file_path = f'{base_dir}/{target_lang}.json'
    blacklist = ('title')

    # Create a translator object

    # Load the JSON data
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Function to recursively translate content
    def translate_content(content):
        if isinstance(content, dict):
            return {k: (translate_content(v) if k not in blacklist else v) for k, v in content.items()}
        elif isinstance(content, str):
            return translate_string(content, target_lang).text
        return content

    # Translate the content
    translated_data = translate_content(data)

    # Save the translated data to a new JSON file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(translated_data, file, ensure_ascii=False, indent=4)
        
def load_languages():
    """
    Loads language data from a JSON file located in the static directory.
    
    Returns:
    list: A list of dictionaries, where each dictionary contains a 'code' and a 'name' of a language.
    """
    try:
        with open('static/ISO-639-1-language.json', 'r') as file:
            languages = json.load(file)
            return languages
    except FileNotFoundError:
        print("The language file could not be found.")
        return []
    except json.JSONDecodeError:
        print("The language file is not in proper JSON format.")
        return []

        
def translate_string(string, lang, api_key):
    """
    Translates a string into the specified language using Google Translate API via httpx.

    Args:
    string (str): The string to translate.
    lang (str): The ISO-639-1 code of the target language.
    api_key (str): The API key for accessing Google Translate API.

    Returns:
    str: The translated text.

    Raises:
    ValueError: If the provided language code is unsupported.
    """
    
    if any(d["code"] == lang for d in load_languages()):
        raise ValueError(f"Unsupported language code: {lang}")

    url = "https://translation.googleapis.com/language/translate/v2"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": api_key
    }
    data = {
        "q": string,
        "target": lang
    }

    response = httpx.post(url, headers=headers, params=params, json=data)

    if response.status_code == 200:
        translation = response.json()
        translated_text = translation["data"]["translations"][0]["translatedText"]
        return translated_text
    else:
        raise Exception(f"Translation API request failed with status code {response.status_code}: {response.text}")

        
def load_translations(site_lang):
    base_dir = 'translations'
    # Construct the path for the requested language file
    language_file_path = os.path.join(base_dir, f'{site_lang}.json')
    
    # Check if the specific language file exists
    if not os.path.exists(language_file_path):
        # If not, use the default English language file
        try:
            get_global_translation(site_lang)
        except Exception:  # Catching all exceptions
            language_file_path = os.path.join(base_dir, 'en.json')
    
    # Load the JSON data from the file
    with open(language_file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def nest_dictionaries(dict_of_dicts):
    result = {}
    for key, value in dict_of_dicts.items():
        result[key] = value
    return result

def load_site_data():
    config = load_config()
    settings = config.get("settings")
    site_lang = get_system_language_iso_639_1() if not settings["overwrite_sys_lang"] else settings["user_lang"]
    user_profile = settings["user_profile"]
    practice_lang = settings["practice_lang"]
    practice_lang_prof = settings["practice_lang_prof"]
    desired_scenario = settings["desired_scenario"]
    auto_translate = settings["auto_translate"]
    
    
    return {"config": config, "settings": settings, "site_lang": site_lang, "user_profile": user_profile, "practice_lang": practice_lang, "practice_lang_prof": practice_lang_prof, "desired_scenario": desired_scenario, "auto_translate": auto_translate}

def load_user_profile(profile):
    base_dir = 'user_profiles'
    profile_path = os.path.join(base_dir, f"{profile}.json")
    default_path = os.path.join(base_dir, "default.json")

    # Check if the specified profile JSON file exists
    if os.path.exists(profile_path):
        with open(profile_path, 'r', encoding="utf-8") as file:
            return json.load(file)
    else:
        # If the specified file does not exist, load the default profile
        with open(default_path, 'r', encoding="utf-8") as file:
            return json.load(file)
        
def get_profile_list():
    base_dir = 'user_profiles'
    
    profiles = []

    # Loop through all files in the directory
    for filename in os.listdir(base_dir):
        if filename.endswith(".json"):  # Check if the file is a JSON file
            profiles.append(filename[:-5].capitalize())

    return profiles

def update_user_profile(new_profile):
    config_path = "config.yaml"
    profile_path = f"user_profiles/{new_profile}.json"
    
    # Load the new profile from the JSON file
    with open(profile_path, 'r') as profile_file:
        new_profile_data = json.load(profile_file)
    
    # Read the existing config file
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    # Update the user_profile and user_lang in the config
    config['settings']['user_profile'] = new_profile
    config['settings']['user_lang'] = lang_to_code(new_profile_data.get('native_language'))
    
    # Write the updated data back to the config file
    with open(config_path, 'w') as config_file:
        yaml.safe_dump(config, config_file)
        
def update_practice_language(language, practice_lang_prof, desired_scenario):
    file_path = "config.yaml"
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
        
    scenarios_file = "scenarios.json"
    with open(scenarios_file, 'r') as file:
        scenarios = json.load(file)
    
    scenario = find_json_value(scenarios, desired_scenario)
    
    code = lang_to_code(language)
    # Update the practice_lang
    config['settings']['practice_lang'] = code
    config['settings']['practice_lang_prof'] = practice_lang_prof
    config['settings']['desired_scenario'] = scenario
    
    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        yaml.safe_dump(config, file)
        
def find_json_value(d, key):
    if key in d:
        return d[key]
    for k, v in d.items():
        if isinstance(v, dict):
            result = find_json_value(v, key)
            if result is not None:
                return result
    return None
        
def update_config(**kwargs):
    file_path = "config.yaml"
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # Update the user_profile with kwargs
    for key, value in kwargs.items():
        if key in config['settings']:
            config['settings'][key] = value
    
    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        yaml.safe_dump(config, file)

def update_apis(**kwargs):
    file_path = "API_keys.py"
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    api_keys = {
        'gpt3_api_key': 'OPENAI_API',
        'gemini_api_key': 'GEMINI_API',
        'llama_api_key': 'LLAMA_API',
        'claude_api_key': 'CLAUDE_API'
    }

    # Create a dictionary for the current API keys
    api_replacements = {api_keys[key]: value for key, value in kwargs.items() if key in api_keys}

    # Update the lines with the new API keys
    with open(file_path, 'w') as file:
        for line in lines:
            for api_var, new_value in api_replacements.items():
                if line.startswith(api_var):
                    line = f"{api_var} = \"{new_value}\"\n"
            file.write(line)
        

def lang_to_code(name):
    name = name.lower()
    try:
        lang = languages.get(name=name)
        return lang.part1
    except KeyError:
        return llm_guess_lang(name)

def code_to_lang(code):
    """
    Converts an ISO-639-1 code to its corresponding language name. If no language is found, assumes non-standard conlang.
    
    Args:
    code (str): The ISO-639-1 code of the language.
    
    Returns:
    str: The full name of the language or code if the code is not found.
    """
    try:
        lang = languages.get(part1=code.lower())
        return lang.name
    except KeyError:
        return code

def get_chatlog_filename(directory, bot_name=None):
    """
    Generate the next available chat log filename in the specified directory.

    Parameters:
    - directory (str): The directory where chat logs are stored.
    - bot_name (str, optional): Name of the bot (not used in this function).

    Returns:
    - str: The next available chat log filename in the format "chatN.json".
    """
    # List all files in the directory
    files = os.listdir(directory)
    # Filter files to count only those that match our naming scheme
    count = sum(1 for file in files if file.startswith('chat') and file.endswith('.json'))
    # Return the next file name
    return f"chat{count + 1}.json"


def append_chatlog(text, file_path, role):
    """
    Append a new chat message to the chat log file.

    Parameters:
    - text (str): The message text to append.
    - file_path (str): The path to the chat log file.
    - is_bot (bool): Flag indicating if the message is from the bot.

    Returns:
    - None
    """
    # Try to read the existing data from the file
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"log": []}  # Initialize with an empty log if file doesn't exist or is empty

    # Append the new dictionary to the log list
    app_dict = {"role": role, "message": text}
    data["log"].append(app_dict)

    # Write the updated data back to the file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def get_context_to_n(file_path, n=20):
    """
    Get the context of the chat from the last `n` messages in the chat log file.

    Parameters:
    - file_path (str): The path to the chat log file.
    - n (int): The number of last messages to retrieve.

    Returns:
    - str: A single string containing the last `n` messages separated by " | ".
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"Error reading the file: {error}")
        return ""
    
    # Extract the log list
    log_entries = data.get("log", [])
    
    total_entries = len(log_entries)
    
    # Calculate the starting index for n-th last entry
    start_index = max(0, total_entries - n)
    
    # Extract messages from n-th last entry to the end
    messages = [entry["message"] for entry in log_entries[start_index:]]
    
    # Compile the messages into a single string with clear separations
    compiled_messages = " | ".join(messages)
    
    return compiled_messages

def get_context_to_token_limit(file_path, token_limit=2900):
    """
    Truncate the log entries to fit within a certain token limit.

    Parameters:
    - file_path (str): The path to the chat log file.
    - token_limit (int): The maximum number of tokens allowed.

    Returns:
    - dict: A dictionary containing the truncated log entries in the specified format.
    """
    
    # Load configuration settings
    config = load_config()
    settings = config.get("settings")
    overwrite_token_limit = settings.get("overwrite_token_limit")
    user_token_limit = settings.get("user_token_limit")
    
    # Overwrite token limit if settings dictate
    if overwrite_token_limit:
        token_limit = user_token_limit
    
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"Error reading the file: {error}")
        return {"messages": []}
    
    # Extract the log list
    log_entries = data.get("log", [])
    
    total_tokens = 0
    truncated_log = []

    for entry in reversed(log_entries):

        message_tokens = len(encoding.encode(entry["message"]))
        
        if total_tokens + message_tokens <= token_limit:
            truncated_log.append(entry)
            total_tokens += message_tokens
        else:
            break
    
    # Format the truncated log entries as required
    formatted_log = [
        {"role": entry["role"], "content": entry["message"]}
        for entry in truncated_log[::-1]
    ]

    return formatted_log


def initialize_chat_log():
    """
    Check for the existence of log.json. If it doesn't exist, create it and
    call gpt_get_chat_initialise with the necessary parameters, then append
    the response as the system role.
    """
    
    site_data = load_site_data()
    practice_lang = code_to_lang(site_data["practice_lang"])
    user_profile = load_user_profile(site_data["user_profile"])
    practice_lang_prof = site_data["practice_lang_prof"]
    desired_scenario = site_data["desired_scenario"]
    base_dir = "chat_logs"
    directory = os.path.join(base_dir, practice_lang)
    
    os.makedirs(directory, exist_ok=True)
    file_name = 'log.json'
    file_path = os.path.join(directory, file_name)
    
    if not os.path.exists(file_path):
        initial_response = llm_get_chat_initialise([], practice_lang, "N/A", user_profile, practice_lang_prof, desired_scenario)
        print(f'Initial bot response: {initial_response}')
        
        initial_log = {
            "log": [
                {"role": "system", "message": initial_response}
            ]
        }
        
        with open(file_path, 'w') as f:
            json.dump(initial_log, f, indent=4)

def process_data(data):
    """
    Process the given data based on its type.

    Parameters:
    - data (dict): The data/message to be processed.

    Returns:
    - dict: A dictionary containing the processed result.
    """
    if data['type'] == 'message':
        return handle_message(data['content'])
    elif data['type'] == 'question':
        return handle_question(data['content'])
    elif data['type'] == 'explain':
        return handle_explain(data['content'])
    else:
        raise ValueError("Unknown data type")

def handle_message(content):
    """
    Process a chat message, append it to the chat log, generate a bot response,
    and append the bot response to the chat log. Finally, return the chat log.

    Parameters:
    - content (str): The message content to be processed.

    Returns:
    - dict: A dictionary containing the message and the updated chat log.
    """
    
    print(f'Content: {content}')
    site_data = load_site_data()

    practice_lang = code_to_lang(site_data["practice_lang"])
    user_profile = load_user_profile(site_data["user_profile"])
    practice_lang_prof = site_data["practice_lang_prof"]
    desired_scenario = site_data["desired_scenario"]
    base_dir = "chat_logs"
    directory = os.path.join(base_dir, practice_lang)
    
    os.makedirs(directory, exist_ok=True)
    file_name = 'log.json'
    file_path = os.path.join(directory, file_name)
    
    # Create and write default data to the file
    append_chatlog(content, file_path, role='user')
    context = get_context_to_token_limit(file_path)

    bot_response = llm_get_chat_response(context, practice_lang, "N/A", user_profile, practice_lang_prof, desired_scenario)
    print(f'Bot response: {bot_response}')
    append_chatlog(bot_response, file_path, role='system')
    
    with open(file_path, 'r') as f:
        log = json.load(f)["log"]

    return {"type": "message", "message": "Processed data", "chatlog": log}

def handle_question(content):
    """
    Handle a question by simply acknowledging it without processing.

    Parameters:
    - content (str): The question content.

    Returns:
    - dict: A dictionary acknowledging the question.
    """
    print(f'Content {content}')
    site_data = load_site_data()

    practice_lang = code_to_lang(site_data["practice_lang"])
    user_lang = code_to_lang(site_data["site_lang"])
    
    answer = llm_get_bot_answer(content, practice_lang, user_lang)
    print(f'Answer: {answer}')

    return {"type": "question", "message": "Question received", "answer": answer}

def handle_explain(content):
    """
    Handle a question by simply acknowledging it without processing.

    Parameters:
    - content (str): The question content.

    Returns:
    - dict: A dictionary acknowledging the question.
    """
    print(f'Content {content}')
    site_data = load_site_data()

    practice_lang = code_to_lang(site_data["practice_lang"])
    user_lang = code_to_lang(site_data["site_lang"])
    print(f'User: {user_lang}')
    
    if content['role'] == 'system':
        
        explanation = llm_get_bot_explain(content['message'], practice_lang, user_lang)
    else:
        explanation = llm_get_user_comment(content['message'], practice_lang, user_lang)
    
    
    print(f'Explanation: {explanation}')

    return {"type": "explanation", "message": "Question received", "explanation": explanation}

