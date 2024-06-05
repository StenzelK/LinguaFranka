import json
import locale
import os
from googletrans import Translator, LANGUAGES
import yaml

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
    site_lang = get_system_language_iso_639_1() if not settings["overwrite_sys_lang"] else settings["language"]
    user_profile = settings["user_profile"]
    
    
    return {"config": config, "settings": settings, "site_lang": site_lang, "user_profile": user_profile}

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

