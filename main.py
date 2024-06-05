from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from utility import *

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



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