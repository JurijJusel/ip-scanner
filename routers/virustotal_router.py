from fastapi import APIRouter, HTTPException
from models.virustotal_model import VirusTotalIP
from services.service_virustotal import check_ip_virustotal
from services.socket_domain_ip import domain_to_ip
import os
import re


router = APIRouter()

def is_ip(value: str) -> bool:
    pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    return bool(re.match(pattern, value))

@router.get("/virustotal/{ip_or_domain}", response_model=VirusTotalIP)
async def get_virustotal(ip_or_domain: str):
    api_key = os.getenv("VIRUSTOTAL_API")

    if is_ip(ip_or_domain):
        ip = ip_or_domain
    else:
        ip = domain_to_ip(ip_or_domain)
        if ip is None:
            raise HTTPException(status_code=400, detail=f"Could not resolve domain: {ip_or_domain}")

    result = check_ip_virustotal(ip, api_key)

    if result is None:
        raise HTTPException(status_code=404, detail=f"No data found for IP: {ip}")

    return result
