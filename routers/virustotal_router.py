import os
from fastapi import APIRouter, HTTPException
from models.virustotal_model import VirusTotalIP
from services.service_virustotal import check_ip_virustotal
from utils.clean_domain_ip import domain_to_ip
from config import VIRUSTOTAL_API_URL
from utils.validators import is_valid_ip

router = APIRouter()


@router.get("/virustotal/{ip_or_domain}", response_model=VirusTotalIP)
async def get_virustotal(ip_or_domain: str):  # ← Tik ip_or_domain!
    api_key = os.getenv("VIRUSTOTAL_API")

    if is_valid_ip(ip_or_domain):
        ip = ip_or_domain
    else:
        ip = domain_to_ip(ip_or_domain)
        if ip is None:
            raise HTTPException(status_code=400, detail=f"Could not resolve domain: {ip_or_domain}")

    result = check_ip_virustotal(ip, api_key, VIRUSTOTAL_API_URL)

    if result is None:
        raise HTTPException(status_code=404, detail=f"No data found for IP: {ip}")

    return result
