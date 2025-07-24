# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need



# app/utils.py

import random
import string
import re

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def is_valid_url(url):
    url_regex = re.compile(
        r'^(http:\/\/|https:\/\/)'  
        r'([\w\-]+\.)+[\w]{2,}'     
        r'([\/\w\-\.\?\=\&\%\#]*)*$',  
        re.IGNORECASE
    )
    return re.match(url_regex, url) is not None
