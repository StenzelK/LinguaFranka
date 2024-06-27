import logging
from fastapi import FastAPI, Form, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocketState
from starlette.responses import HTMLResponse
from utility import *

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

######################################
#-------------Views------------------#
######################################

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    logger.info("Request to read_root received")

    try:
        site_data = load_site_data()
        logger.info("Site data loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load site data: {e}")
        raise

    try:
        translation = load_translations(site_data["site_lang"])
        logger.info("Translations loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load translations: {e}")
        raise

    dicts_to_combine = {
        "nav": translation["nav"],
        "index": translation["index"]
    }

    try:
        site_data = load_site_data()
        logger.info("Site data reloaded successfully")
    except Exception as e:
        logger.error(f"Failed to reload site data: {e}")
        raise

    try:
        practice_lang = code_to_lang(site_data["practice_lang"])
        logger.info(f"Practice language identified: {practice_lang}")
    except Exception as e:
        logger.error(f"Failed to identify practice language: {e}")
        raise

    base_dir = "chat_logs"
    directory = os.path.join(base_dir, practice_lang)

    try:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Directory '{directory}' created or already exists")
    except Exception as e:
        logger.error(f"Failed to create directory '{directory}': {e}")
        raise

    file_name = 'log.json'
    file_path = os.path.join(directory, file_name)

    try:
        with open(file_path, 'r') as f:
            log = json.load(f)
            logger.info(f"Log file '{file_path}' loaded successfully")
    except (IOError, json.JSONDecodeError) as e:
        logger.warning(f"Failed to load log file '{file_path}', initializing new log: {e}")
        log = {"log": []}

    try:
        content = nest_dictionaries(dicts_to_combine)
        logger.info("Content nested successfully")
    except Exception as e:
        logger.error(f"Failed to nest dictionaries: {e}")
        raise

    logger.info("Rendering template with content and chat log")
    return templates.TemplateResponse("index.html", {
        "request": request,
        "content": content,
        "chatlog": log
    })
    

@app.get("/profile", response_class=HTMLResponse)
def read_prof(request: Request):
    logger.info("Received request for /profile")

    try:
        logger.debug("Loading site data")
        site_data = load_site_data()
        
        logger.debug(f"Site data loaded: {site_data}")
        
        logger.debug("Loading translations")
        translation = load_translations(site_data["site_lang"])
        
        logger.debug(f"Translations loaded: {translation}")
        
        logger.debug("Loading user profile")
        user_profile = load_user_profile(site_data["user_profile"])
        
        logger.debug(f"User profile loaded: {user_profile}")
        
        logger.debug("Getting profile list")
        profile_list = get_profile_list()
        
        logger.debug(f"Profile list obtained: {profile_list}")

        dicts_to_combine = {
            "nav": translation["nav"],
            "profile": translation["profile"],
            "user_profile": user_profile,
            "profile_list": profile_list
        }
        
        logger.debug(f"Combining dictionaries: {dicts_to_combine}")
        
        content = nest_dictionaries(dicts_to_combine)
        
        logger.debug(f"Content nested: {content}")

        return templates.TemplateResponse("profile.html", {"request": request, "content": content})

    except Exception as e:
        logger.error(f"Error processing request for /profile: {e}")
        raise e
    

@app.get("/lang", response_class=HTMLResponse)
def read_lang(request: Request):
    logger.info("Received request for /lang")

    try:
        logger.debug("Loading site data")
        site_data = load_site_data()
        
        logger.debug(f"Site data loaded: {site_data}")
        
        site_lang = site_data["site_lang"]
        logger.debug(f"Site language: {site_lang}")
        
        logger.debug("Loading translations")
        translation = load_translations(site_lang)
        
        logger.debug(f"Translations loaded: {translation}")

        logger.debug("Converting practice language code to language name")
        practice_lang = code_to_lang(site_data["practice_lang"])
        
        logger.debug(f"Practice language: {practice_lang}")

        if site_lang != "en":
            logger.debug(f"Translating practice language to site language: {site_lang}")
            practice_lang = translate_string(practice_lang, site_lang)
            logger.debug(f"Translated practice language: {practice_lang}")

        dicts_to_combine = {
            "nav": translation["nav"],
            "lang": translation["lang"],
            "practice_lang": practice_lang,
        }
        
        logger.debug(f"Combining dictionaries: {dicts_to_combine}")
        
        content = nest_dictionaries(dicts_to_combine)
        
        logger.debug(f"Content nested: {content}")

        return templates.TemplateResponse("lang.html", {"request": request, "content": content})

    except Exception as e:
        logger.error(f"Error processing request for /lang: {e}")
        raise e
    
    
######################################
#-------------Logic------------------#
######################################

@app.post("/change_user_profile")
async def change_user_profile(profile: str = Form(...)):
    logger.info("Received request to change user profile")

    try:
        logger.debug(f"Updating user profile with data: {profile}")
        update_user_profile(profile)
        logger.info("User profile updated successfully")

        return RedirectResponse(url="/profile", status_code=303)

    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        raise e

@app.post("/add_user_profile")
async def add_user_profile(name: str = Form(...), age: int = Form(...), 
                           native_language: str = Form(...), interests: str = Form(...)):
    logger.info("Received request to add a new user profile")

    try:
        logger.debug(f"Processing inputs: name={name}, age={age}, native_language={native_language}, interests={interests}")
        
        # Split the interests input into a list
        interests_list = [interest.strip() for interest in interests.split(',')]
        logger.debug(f"Processed interests: {interests_list}")

        # Create the new profile dictionary
        new_prof = {
            "name": name,
            "age": age,
            "native_language": native_language,
            "interests": interests_list
        }
        logger.debug(f"New profile created: {new_prof}")

        # Prepare the file path
        file_name = name.replace(' ', '_')
        directory = "user_profiles"
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, f"{file_name}.json")
        logger.debug(f"File path prepared: {file_path}")

        # Write the new profile to a JSON file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(new_prof, f, ensure_ascii=False, indent=4)
        logger.info(f"User profile saved successfully: {file_path}")

        return RedirectResponse(url="/profile", status_code=303)

    except Exception as e:
        logger.error(f"Error adding new user profile: {e}")
        raise e

@app.post("/chooselang")
async def choose_language(language: str = Form(...), practice_lang_prof: str = Form(...)):
    """
    Endpoint to handle language choice from a form.

    Args:
    language (str): The language choice submitted from the form.

    Returns:
    dict: A confirmation message with the chosen language.
    """
    logger.info("Received request to choose language")

    try:
        logger.debug(f"Language chosen: {language}")
        
        update_practice_language(language)
        logger.info("Practice language updated successfully")

        return RedirectResponse(url="/lang", status_code=303)

    except Exception as e:
        logger.error(f"Error updating practice language: {e}")
        raise e

######################################
#-------------Chat util--------------#
######################################


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            try:
                data = await websocket.receive_text()
                data_json = json.loads(data)  # Parse the incoming string to a dictionary
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON: {e}")
                await websocket.send_json({"type": "error", "message": "Invalid JSON format"})
                continue
            except WebSocketDisconnect:
                logger.info("WebSocket was disconnected.")
                break  # Exit the loop if the WebSocket is disconnected
            
            print(f'Data: {type(data_json)} {data_json}')
            response_data = process_data(data_json)  # Ensure this function does not throw unhandled exceptions
            print(f'Response: {type(response_data)} {response_data}')
            await websocket.send_json(response_data)
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        if websocket.application_state == WebSocketState.CONNECTED:
            try:
                logger.info("Closing WebSocket connection.")
                await websocket.close()
            except RuntimeError as e:
                logger.error(f"Error while closing WebSocket: {e}")
        else:
            logger.info("WebSocket already closed.")