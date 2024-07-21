from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.exceptions import CityNotFound
from app.openmeteo import OpenMeteo
from app.schemas import SCity

router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.globals["zip"] = zip


@router.get("/", response_class=HTMLResponse)
def get_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@router.get("/meteo", response_class=HTMLResponse)
async def get_meteo(request: Request, city: SCity = Depends()):
    try:
        meteo = await OpenMeteo(city.name).get_meteo()
        return templates.TemplateResponse(request=request, name="search.html", context={"city": city, "meteo": meteo})
    except CityNotFound:
        return templates.TemplateResponse(request=request, name="error.html")
