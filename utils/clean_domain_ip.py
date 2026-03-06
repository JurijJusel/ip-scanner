from urllib.parse import unquote
import socket


def clean_domain(domain: str) -> str:
    """
    Remove common URL components from domain string.
    Args:
        domain: Domain string to clean (e.g., 'https://www.google.com/')
    Returns:
        str: Cleaned domain name, or empty string if invalid
    Example:
        clean_domain("https://www.google.com/") -> 'google.com'
    """
    try:
        if domain is None:
            return ""

        if not isinstance(domain, str):
            return ""

        decoded = unquote(domain)
        if decoded != domain:
            print(f"🔍 [1] UNQUOTE: '{domain}' → '{decoded}'")
        else:
            print(f"🔍 [1] UNQUOTE: No change for '{domain}'")


        domain = decoded.strip().lower()

        if not domain:
            return ""

        # Remove protocols
        original = domain
        for protocol in ['https://', 'http://', 'ftp://', 'ftps://', 'ws://', 'wss://']:
            if domain.startswith(protocol):
                domain = domain[len(protocol):]
                break

        # Remove www.
        if domain.startswith('www.'):
            original = domain
            domain = domain[4:]


        # Remove path
        if '/' in domain:
            original = domain
            domain = domain.split('/')[0]


        # Remove trailing dots
        domain = domain.rstrip('.')


        return domain

    except Exception as e:
        print(f"❌ Unexpected error cleaning domain '{domain}': {e}")
        import traceback
        traceback.print_exc()
        return ""


def domain_to_ip(domain: str) -> str:
    """
    Resolve domain name to IP address.
    Args:
        domain: Domain name (e.g., 'google.com')
    Returns:
        str: IP address
    Example:
        ip = domain_to_ip('google.com')
        print(ip)  # '142.250.185.46'
    """
    try:
        domain = clean_domain(domain)
        print(f"Resolving domain: {domain}")

        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror as e:
        print(f"Failed to resolve domain {domain}: {e}")
        return None

    except Exception as e:
        print(f"❌ Unexpected error resolving '{domain}': {e}")
        return None


if __name__ == "__main__":
    test_domains = [
        "https://www.google.com/",
        "HTTP://WWW.GOOGLE.COM/",
        "www.skelbiu.lt",
        "google.com",
        "WWW.SKELBIU.LT",
        "https://skelbiu.lt/",
        "http://www.skelbiu.lt",
        ""
    ]

    for test in test_domains:
        result = clean_domain(test)
        print(f"'{test}' → '{result}'")
