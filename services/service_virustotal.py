import requests
from typing import Optional, List, Dict
from models.virustotal_model import VirusTotalIP
from utils.http_helpers import handle_api_response
from rich import print


def check_virustotal_key(api_key: str, virustotal_api_url: str) -> bool:
    """
    Validate VirusTotal API key by making a test request.
    Args:
        api_key: VirusTotal API key
        virustotal_api_url: Base URL for VirusTotal API
    Returns:
        bool: True if API key is valid, False otherwise
    """
    try:
        if not api_key:
            print("VirusTotal API key not found in environment variables")
            return False

        # Build full URL with test IP
        test_ip = "8.8.8.8"
        url = f"{virustotal_api_url}{test_ip}"

        headers = {
            'x-apikey': api_key,
            'Accept': 'application/json',
        }

        response = requests.get(url=url, headers=headers, timeout=10)
        success, error_msg = handle_api_response(response, "VirusTotal")

        if not success:
            print(error_msg)
            return False

        return True

    except requests.exceptions.Timeout:
        print("VirusTotal API request timed out")
        return False

    except requests.exceptions.RequestException as e:
        print(f"Failed to validate VirusTotal API: {e}")
        return False

    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def check_ip_virustotal(ip: str, api_key: str, base_api_url: str) -> Optional[VirusTotalIP]:
    """
    Check IP reputation via VirusTotal API v3.
    Args:
        ip: IP address to check
        api_key: VirusTotal API key
        base_url: Base URL (e.g., 'https://www.virustotal.com/api/v3/ip_addresses/')
    Returns:
        VirusTotalIP: Pydantic model with analysis results, or None if failed
    """

    url = f"{base_api_url}{ip}"

    headers = {
        "x-apikey": api_key,
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        attributes = data.get('data', {}).get('attributes', {})

        if not attributes:
            print(f"[WARNING] No data returned for IP: {ip}")
            return None

        vt_data = {
            'ip': ip,
            'reputation': attributes.get('reputation', 0),
            'last_analysis_stats': attributes.get('last_analysis_stats', {}),
            'last_analysis_results': attributes.get('last_analysis_results', {}),
            'network': attributes.get('network'),
            'country': attributes.get('country'),
            'continent': attributes.get('continent'),
            'asn': attributes.get('asn'),
            'as_owner': attributes.get('as_owner'),
            'regional_internet_registry': attributes.get('regional_internet_registry'),
            'whois': attributes.get('whois'),
            'whois_date': attributes.get('whois_date'),
            'last_analysis_date': attributes.get('last_analysis_date'),
            'last_modification_date': attributes.get('last_modification_date'),
            'total_votes': attributes.get('total_votes', {'harmless': 0, 'malicious': 0}),
            'tags': attributes.get('tags', [])
        }

        return VirusTotalIP(**vt_data)

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"[ERROR] IP not found in VirusTotal: {ip}")
        else:
            print(f"[ERROR] HTTP error for IP {ip}: {e}")
        return None

    except requests.exceptions.Timeout:
        print(f"[ERROR] Timeout checking IP {ip}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed for IP {ip}: {e}")
        return None

    except Exception as e:
        print(f"[ERROR] Unexpected error checking IP {ip}: {e}")
        return None


def get_virustotal_info_from_ips_list(ip_list: List[str], api_key: str, base_api_url: str) -> List[Dict]:
    """
    Check multiple IP addresses using VirusTotal API.
    Args:
        ip_list: List of IP addresses to check
        api_key: API key for VirusTotal
        base_url: Base URL for VirusTotal API
    Returns:
        list: List of VirusTotal results as dictionaries
    """

    collected_data = []

    for ip_address in ip_list:
        vt_result = check_ip_virustotal(ip_address, api_key, base_api_url)

        if vt_result is None:
            print(f"Skipping {ip_address} - no data retrieved")
            continue

        collected_data.append(vt_result.model_dump(exclude_none=True))

    return collected_data
