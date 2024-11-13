import re
import socket

def validate_domain_name(domain_name: str) -> bool:
    # Regular expression for basic domain format validation
    domain_regex = re.compile(
        r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.(?:[A-Za-z]{2,6}|[A-Za-z0-9-]{2,})$'
    )
    
    # Check if domain name matches the basic syntax
    if not domain_regex.match(domain_name):
        return False
    
    # Check if the domain can be resolved using DNS
    try:
        socket.gethostbyname(domain_name)
        return True  # Domain is valid and exists
    except socket.gaierror:
        return False  # Domain does not exist or cannot be resolved
