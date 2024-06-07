import json
import locale
import os
from googletrans import Translator, LANGUAGES
import yaml
from GPT_tools import *

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
    translator = Translator()

    # Check if the target language is supported
    if target_lang not in LANGUAGES:
        raise ValueError(f"Unsupported language code: {target_lang}")

    # Load the JSON data
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Function to recursively translate content
    def translate_content(content):
        if isinstance(content, dict):
            return {k: (translate_content(v) if k not in blacklist else v) for k, v in content.items()}
        elif isinstance(content, str):
            return translator.translate(content, dest=target_lang).text
        return content

    # Translate the content
    translated_data = translate_content(data)

    # Save the translated data to a new JSON file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(translated_data, file, ensure_ascii=False, indent=4)
        
def translate_string(string, lang):
    """
    Translates a string into the specified language using googletrans library.

    Args:
    string (str): The string to translate.
    lang (str): The ISO-639-1 code of the target language.

    Returns:
    str: The translated text.

    Raises:
    ValueError: If the provided language code is unsupported.
    """
    
    translator = Translator()
    if lang not in LANGUAGES:
        raise ValueError(f"Unsupported language code: {lang}")
    
    return translator.translate(string, dest=lang).text
        
def load_translations(site_lang):
    base_dir = 'translations'
    # Construct the path for the requested language file
    language_file_path = os.path.join(base_dir, f'{site_lang}.json')
    
    # Check if the specific language file exists
    if not os.path.exists(language_file_path):
        # If not, use the default English language file
        try:
            get_global_translation(site_lang)
        except ValueError:
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
    
    
    return {"config": config, "settings": settings, "site_lang": site_lang, "user_profile": user_profile, "practice_lang": practice_lang}

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
    file_path = "config.yaml"
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # Update the user_profile
    config['settings']['user_profile'] = new_profile
    
    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        yaml.safe_dump(config, file)
        
def update_practice_language(language):
    file_path = "config.yaml"
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    
    code = lang_to_code(language)
    # Update the practice_lang
    config['settings']['practice_lang'] = code
    
    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        yaml.safe_dump(config, file)
        
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

def lang_to_code(name, failover=False, depth=0):
    """
    Converts a partial or full language name to its corresponding ISO-639-1 code.
    
    Attempts to normalize input into English.
    
    If no code is found, attempts AI interpretation of input to determine the language.
    Limits recursion to a single failover attempt.
    
    If AI failover is not successful, returns "NoLang".
    
    Args:
    name (str): The partial or full name of the language.
    failover (bool): Whether the function is in failover mode.
    depth (int): Current recursion depth, default is 0.
    
    Returns:
    str: The first matching ISO-639-1 code or "NoLang" if no match is found.
    """
    name = name.lower()
    name = translate_string(name, "en")
    languages = load_languages()
    for language in languages:
        if name in language['name'].lower():
            return language['code']

    # Check if failover is already used or if the depth limit is reached
    if not failover and depth < 1:
        guess_name = gpt_guess_lang(name)  # Assuming this function returns a guessed language name
        return lang_to_code(guess_name, failover=True, depth=depth+1)
    
    return "NoLang"

def code_to_lang(code):
    """
    Converts an ISO-639-1 code to its corresponding language name. If no language is found, assumes non-standard conlang.
    
    Args:
    code (str): The ISO-639-1 code of the language.
    
    Returns:
    str: The full name of the language or code if the code is not found.
    """
    languages = load_languages()
    for language in languages:
        if code.lower() == language['code']:
            return language['name']
    return code

def get_chatlog_filename(directory, bot_name=None):
    # List all files in the directory
    files = os.listdir(directory)
    # Filter files to count only those that match our naming scheme
    count = sum(1 for file in files if file.startswith('chat') and file.endswith('.json'))
    # Return the next file name
    return f"chat{count + 1}.json"

def append_chatlog(text, file_path, is_bot=False):
    # Try to read the existing data from the file
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"log": []}  # Initialize with an empty log if file doesn't exist or is empty

    # Append the new dictionary to the log list
    app_dict = {"is_bot": is_bot, "message": text}
    data["log"].append(app_dict)

    # Write the updated data back to the file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
        
        
def get_context(file_path, n = 20):
    
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
    start_index = max(0, total_entries - n) if n > total_entries else 0
    
    # Extract messages from n-th last entry to the end
    messages = [entry["message"] for entry in log_entries[start_index:]]
    
    # Compile the messages into a single string with clear separations
    compiled_messages = " | ".join(messages)
    
    return compiled_messages

def process_data(data):
    
    site_data=load_site_data()

    practice_lang = code_to_lang(site_data["practice_lang"])
    base_dir="chat_logs"
    directory = os.path.join(base_dir, practice_lang)
    
    os.makedirs(directory, exist_ok=True)
    file_name = 'log.json'
    file_path = os.path.join(directory, file_name)
    # Create and write default data to the file
    append_chatlog(data, file_path)
    context = get_context(file_path)
    bot_response = gpt_get_chat_response(context)
    append_chatlog(bot_response, file_path, is_bot=True)
    
    with open(file_path, 'r') as f:
        
        log = json.load(f)["log"]
    
    print(log)
    return {"message": "Processed data", "chatlog": log}