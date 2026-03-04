import ipaddress
import re
from typing import Optional


def is_valid_ip(value: str) -> bool:
    """
    Check if value is a valid IP address (IPv4 or IPv6).
    Args:
        value: String to validate
    Returns:
        bool: True if valid IP address, False otherwise
    Example:
        >>> is_valid_ip("8.8.8.8")
        True
        >>> is_valid_ip("google.com")
        False
        >>> is_valid_ip("2001:4860:4860::8888")
        True
    """
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def is_valid_ipv4(value: str) -> bool:
    """
    Check if value is a valid IPv4 address.
    Args:
        value: String to validate
    Returns:
        bool: True if valid IPv4, False otherwise
    Example:
        >>> is_valid_ipv4("8.8.8.8")
        True
        >>> is_valid_ipv4("2001:4860:4860::8888")
        False
    """
    try:
        ipaddress.IPv4Address(value)
        return True
    except (ValueError, ipaddress.AddressValueError):
        return False


def is_valid_ipv6(value: str) -> bool:
    """
    Check if value is a valid IPv6 address.
    Args:
        value: String to validate
    Returns:
        bool: True if valid IPv6, False otherwise
    Example:
        >>> is_valid_ipv6("2001:4860:4860::8888")
        True
        >>> is_valid_ipv6("8.8.8.8")
        False
    """
    try:
        ipaddress.IPv6Address(value)
        return True
    except (ValueError, ipaddress.AddressValueError):
        return False


def is_valid_domain(domain: str) -> bool:
    """
    Check if domain string is a valid domain name format.
    Args:
        domain: Domain string to validate
    Returns:
        bool: True if valid domain format, False otherwise
    Example:
        >>> is_valid_domain("google.com")
        True
        >>> is_valid_domain("sub.example.co.uk")
        True
        >>> is_valid_domain("invalid domain!")
        False
    """

    pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))


def is_private_ip(ip: str) -> bool:
    """
    Check if IP address is private (RFC 1918).
    Args:
        ip: IP address string
    Returns:
        bool: True if private IP, False otherwise
    Example:
        >>> is_private_ip("192.168.1.1")
        True
        >>> is_private_ip("8.8.8.8")
        False
        >>> is_private_ip("10.0.0.1")
        True
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        return False


def is_loopback_ip(ip: str) -> bool:
    """
    Check if IP address is loopback (127.0.0.0/8 or ::1).
    Args:
        ip: IP address string
    Returns:
        bool: True if loopback IP, False otherwise
    Example:
        >>> is_loopback_ip("127.0.0.1")
        True
        >>> is_loopback_ip("8.8.8.8")
        False
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_loopback
    except ValueError:
        return False


def get_ip_version(ip: str) -> Optional[int]:
    """
    Get IP version (4 or 6).
    Args:
        ip: IP address string
    Returns:
        int: 4 for IPv4, 6 for IPv6, None if invalid
    Example:
        >>> get_ip_version("8.8.8.8")
        4
        >>> get_ip_version("2001:4860:4860::8888")
        6
        >>> get_ip_version("invalid")
        None
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.version
    except ValueError:
        return None
