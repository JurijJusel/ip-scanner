import os
from fastapi import APIRouter, HTTPException
from models.abuseip_model import AbuseModel
from services.service_abuseip import get_info_from_ip, transform_to_abuse_model
from utils.clean_domain_ip import domain_to_ip
from config import ABUSE_API_URL
from utils.validators import is_valid_ip

router = APIRouter()


@router.get("/abuseipdb/{ip_or_domain}", response_model=AbuseModel)
async def get_abuseipdb(ip_or_domain: str):
    api_key = os.getenv("ABUSEIPDB_API")

    if is_valid_ip(ip_or_domain):
        ip = ip_or_domain
    else:
        ip = domain_to_ip(ip_or_domain)
        if ip is None:
            raise HTTPException(status_code=400, detail=f"Could not resolve domain: {ip_or_domain}")

    data = get_info_from_ip(ip, api_key, ABUSE_API_URL)

    if data is None:
        raise HTTPException(status_code=404, detail=f"No data found for IP: {ip}")

    result = transform_to_abuse_model(data)

    if result is None:
        raise HTTPException(status_code=500, detail=f"Failed to parse data for IP: {ip}")

    return result
