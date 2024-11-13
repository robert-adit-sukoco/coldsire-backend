from fastapi import FastAPI, Request, status, HTTPException

from constants.success_response import create_success_response
from services.check_spf_dkim_dmarc_service import check_spf_dkim_dmarc_service
from services.check_spf_dkim_dmarc_from_dataset_service import check_spf_dkim_dmarc_from_dataset_service
from helpers.validators import validate_domain_name

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return create_success_response("Hello World!")


@app.get("/check/{domain_name}", status_code=status.HTTP_200_OK)
async def check_domain_name(domain_name: str):

    if (not validate_domain_name(domain_name)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain not found")
    
    result = await check_spf_dkim_dmarc_service(domain_name)
    return create_success_response(result)

@app.get("/check-dataset")
async def check_domain_name_dataset(page: int | None):
    get_page = 1
    if page is not None:
        get_page = page
    result = await check_spf_dkim_dmarc_from_dataset_service(get_page)
    return create_success_response(result)

