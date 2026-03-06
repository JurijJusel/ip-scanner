import os
from fastapi import APIRouter, HTTPException
from models.virustotal_model import VirusTotalIP
from services.service_virustotal import check_ip_virustotal
from utils.clean_domain_ip import domain_to_ip
from config import VIRUSTOTAL_API_URL
from utils.validators import is_valid_ip

router = APIRouter()


@router.get("/virustotal/{ip_or_domain:path}", response_model=VirusTotalIP)
async def get_virustotal(ip_or_domain: str):
    """
    Check IP or domain reputation via VirusTotal API.
    Args:
        ip_or_domain: IP address or domain name (can include protocol like https://)
    Returns:
        VirusTotalIP: Analysis results from VirusTotal
    Raises:
        HTTPException 400: If domain cannot be resolved
        HTTPException 404: If no data found for IP
        HTTPException 500: If API key not configured
    """
    api_key = os.getenv("VIRUSTOTAL_API")
    if not api_key:
        print("VirusTotal API key not found in environment variables")
        raise HTTPException(
            status_code=500,
            detail="VirusTotal API key not configured"
        )

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
