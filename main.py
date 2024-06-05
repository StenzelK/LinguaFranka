from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from utility import *

app = FastAPI()
templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    
    site_data=load_site_data()
    print(site_data)
    
    translation = load_translations(site_data["site_lang"])

    dicts_to_combine = {
    "nav": translation["nav"],
    "index": translation["index"]
        }
    
    content = nest_dictionaries(dicts_to_combine)
    
    return templates.TemplateResponse("index.html", {"request": request, "content": content})