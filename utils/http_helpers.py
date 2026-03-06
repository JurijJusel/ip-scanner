from typing import Optional
import requests


def handle_api_response(
        response: requests.Response,
        api_name: str = "API") -> tuple[bool, Optional[str]]:
    """
    Handle common API response status codes.
    Args:
        response: Requests Response object
        api_name: Name of the API for error messages
    Returns:
        tuple: (is_success: bool, error_message: Optional[str])
    Example:
        >>> response = requests.get(...)
        >>> success, error = handle_api_response(response, "VirusTotal")
        >>> if not success:
        ...     print(error)
    """
    status = response.status_code

    if status == 200:
        return True, None

    # Common error codes
    error_messages = {
        400: f"{api_name} API Bad request - invalid parameters",
        401: f"{api_name} API key is invalid or expired",
        403: f"{api_name} API key does not have permission",
        404: f"{api_name} API endpoint not found - check URL",
        429: f"{api_name} API rate limit exceeded",
        500: f"{api_name} API internal server error",
        502: f"{api_name} API bad gateway",
        503: f"{api_name} API service unavailable",
        504: f"{api_name} API timeout - server not responding",
    }

    error_msg = error_messages.get(
        status,
        f"{api_name} API returned status code: {status}"
    )

    return False, error_msg
