import openai
import yaml

def load_config(file_path='config.yml'):
    """ Load configuration from a YAML file. """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def query_openai(prompt, config=None):
    """ Send a prompt to the OpenAI API and return the response. """
    if config is None:
        config = load_config()
    
    try:
        # Set up the API key from the configuration
        openai.api_key = config['openai']['api_key']

        # Send the prompt to the OpenAI model specified in the config
        response = openai.Completion.create(
            model=config['openai']['model'],
            prompt=prompt,
            max_tokens=150  # You can adjust parameters like max_tokens as needed
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

def gpt_guess_lang(name):
    
    #TODO
    
    return name

def gpt_get_chat_response(prompt):
    
    #TODO
    
    return prompt[-20:]

def gpt_get_user_comment(prompt):
    
    #TODO
    
    return prompt

def gpt_get_bot_explanation(prompt):
    
    #TODO
    
    return prompt