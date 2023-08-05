import pkg_resources
from requests.structures import CaseInsensitiveDict
from requests.utils import default_user_agent as requests_user_agent


def default_headers_with_brotli():
    """
    Returns default header with this library's custom User-Agent
    and Accept-Encoding which prefers Brotli

    :rtype: requests.structures.CaseInsensitiveDict
    """

    name = "requests-extra"
    version = pkg_resources.get_distribution(name).version

    return CaseInsensitiveDict(
        {
            "User-Agent": f"{name}/{version} ({requests_user_agent()})",
            "Accept-Encoding": "br, gzip, deflate",
            "Accept": "*/*",
            "Connection": "keep-alive",
        }
    )
