import os
import requests

from fastapi import FastAPI, APIRouter, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from typing import Optional
from pathlib import Path
from app.modules.schemas import StateSearchResults
from app.modules.utility import generate_dropdown_html
from app.modules.stats import compute_percent_recovered

import pandas as pd

BASE_PATH = Path(__file__).resolve().parent


def open_data(fn, data_dir=str(BASE_PATH)+'\\app\\data'):
    path_file = f'{data_dir}\{fn}'
    if os.path.isfile(path_file):
        with open(path_file, 'r') as file:
            data = pd.read_json(file)
        return data
    else:
        response_api = requests.get(f'https://api.covid19india.org/{fn}')
        if response_api.status_code == 200:
            with open(path_file, 'w') as file:
                file.write(response_api.text)
            return response_api.text
        else:
            raise Exception(f'No such file found. Status code: {response_api.status_code}')


app = FastAPI(
    title="Covid in India Data Exploration", openapi_url="/openapi.json"
)
print('path: ',Path(__file__).parent.absolute())
app.mount(
    "/app/static",
    StaticFiles(directory=str(str(Path(__file__).parent.absolute()))+"\\app\\static"),
    name="static",
)

templates = Jinja2Templates(directory=str(Path(__file__).parent.absolute())+"\\app\\templates")

api_router = APIRouter()

data = dict(open_data('state_district_wise.json'))


@api_router.get('/favicon.ico')
async def return_favicon():
    return FileResponse(str(Path(__file__).parent.absolute())+"\\app\\static\\favicon.ico")

@api_router.get('/app/data/{filename}')
async def return_file(filename: str):
    return FileResponse(str(Path(__file__).parent.absolute())+f"\\app\\data\\{filename}")

@api_router.get("/", status_code=200)
async def root(request: Request) -> dict:

    return templates.TemplateResponse(
        "index.html",
        {"request": request, },
    )


@api_router.get("/{state}", status_code=200, response_model=StateSearchResults)
async def get_data_by_state(
        request: Request,
        state: str,
        district: Optional[str] = Query(None,
                                        description="District Name"),
):

    district_list =  list(data[state]["districtData"].keys())

    if not district:
        results = data[state]["districtData"]

        return templates.TemplateResponse(
            "index.html",
            {"request": request, "results": results,
             "state_name": state,
             "district_choices": generate_dropdown_html(district_list,
                                                        f'Districts in {state}',
                                                        state)},
        )
    else:
        results = {str(district): data[state]["districtData"][district]}

        return templates.TemplateResponse(
            "index.html",
            {"request": request,
             "state_name": state,
             "district_name": district,
             "recovered_pct": compute_percent_recovered(results),
             "state_choices": generate_dropdown_html(list(data.keys()),
                                                     'States in India',
                                                     None),
             "district_choices": generate_dropdown_html(district_list,
                                                        f'Districts in {state}',
                                                        state)
             } | results[district],
        )



app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001, log_level="debug")

    '''
    response_API = requests.get('https://api.covid19india.org/state_district_wise.json')
    #print(response_API.status_code)
    data = response_API.text
    parse_json = json.loads(data)
    active_case = parse_json['Andaman and Nicobar Islands']['districtData']['South Andaman']['active']
    print("Active cases in South Andaman:", active_case)
    print(parse_json['Andaman and Nicobar Islands'])
    '''
