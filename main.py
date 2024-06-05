from fastapi import FastAPI, Form, Request
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
    
    content = nest_dictionaries(dicts_to_combine)
    
    return templates.TemplateResponse("index.html",\
        {"request": request, "content": content})
    
@app.get("/profile", response_class=HTMLResponse)
def read_root(request: Request):
    
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