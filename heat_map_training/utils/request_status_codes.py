"""
Contains request status codes
"""

from requests import codes

STATUS_CODE_OK = codes.get('ok', 200)
STATUS_CODE_NOT_FOUND = codes.get('not_found', 404)
