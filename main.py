from fastapi import FastAPI, Form, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from utility import *

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


######################################
#-------------Views------------------#
######################################
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    
    site_data=load_site_data()
    
    translation = load_translations(site_data["site_lang"])

    dicts_to_combine = {
    "nav": translation["nav"],
    "index": translation["index"]
        }
    
    site_data=load_site_data()

    practice_lang = code_to_lang(site_data["practice_lang"])
    base_dir="chat_logs"
    directory = os.path.join(base_dir, practice_lang)
    
    os.makedirs(directory, exist_ok=True)
    file_name = 'log.json'
    file_path = os.path.join(directory, file_name)
    
    try:
        with open(file_path, 'r') as f:
            log = json.load(f)
    except (IOError, json.JSONDecodeError):
        log = {"log": []}
    
    content = nest_dictionaries(dicts_to_combine)

    return templates.TemplateResponse("index.html",\
        {"request": request, "content": content, "chatlog": log})
    
@app.get("/profile", response_class=HTMLResponse)
def read_prof(request: Request):
    
    site_data=load_site_data()
    
    translation = load_translations(site_data["site_lang"])
    
    user_profile = load_user_profile(site_data["user_profile"])
    profile_list = get_profile_list()

    dicts_to_combine = {
    "nav": translation["nav"],
    "profile": translation["profile"],
    "user_profile": user_profile,
    "profile_list": profile_list
        }
    
    content = nest_dictionaries(dicts_to_combine)
    
    return templates.TemplateResponse("profile.html",\
        {"request": request, "content": content})
    
@app.get("/lang", response_class=HTMLResponse)
def read_lang(request: Request):
    
    site_data=load_site_data()
    site_lang = site_data["site_lang"]
    translation = load_translations(site_lang)
    
    practice_lang = code_to_lang(site_data["practice_lang"])
    
    if site_lang != "en":
        practice_lang = translate_string(practice_lang, site_lang)

    dicts_to_combine = {
    "nav": translation["nav"],
    "lang": translation["lang"],
    "practice_lang": practice_lang,
        }
    
    content = nest_dictionaries(dicts_to_combine)
    
    return templates.TemplateResponse("lang.html",\
        {"request": request, "content": content})
    
    
######################################
#-------------Logic------------------#
######################################

@app.post("/change_user_profile")
async def change_user_profile(profile: str = Form(...)):
   
    update_user_profile(profile)
    
    return RedirectResponse(url="/profile", status_code=303)

@app.post("/add_user_profile")
async def add_user_profile(name: str = Form(...), age: int = Form(...), 
                           native_language: str = Form(...), interests: str = Form(...)):
    # Split the interests input into a list
    interests_list = [interest.strip() for interest in interests.split(',')]
    # Here you would normally process and store the data
    new_prof = {
        "name": name,
        "age": age,
        "native_language": native_language,
        "interests": interests_list
    }
    
    file_name=name.replace(' ', '_')
    directory = "user_profiles"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, f"{file_name}.json")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(new_prof, f, ensure_ascii=False, indent=4)
    
    
    return RedirectResponse(url="/profile", status_code=303)

@app.post("/chooselang")
async def choose_language(language: str = Form(...)):
    """
    Endpoint to handle language choice from a form.

    Args:
    language (str): The language choice submitted from the form.

    Returns:
    dict: A confirmation message with the chosen language.
    """
    update_practice_language(language)
    
    return RedirectResponse(url="/lang", status_code=303)

######################################
#-------------Chat util--------------#
######################################

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response_data = process_data(data)  # Ensure this function does not throw unhandled exceptions
            await websocket.send_json(response_data)
    except WebSocketDisconnect:
        print("WebSocket was disconnected.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()
        
