from dns.resolver import Resolver
import re

def parse_dkim_record(dkim_record):
    # Regular expressions to match each part
    version_match = re.search(r'v=([^;]+)', dkim_record)
    algorithm_match = re.search(r'k=([^;]+)', dkim_record)
    key_match = re.search(r'p=([^;]+)', dkim_record)
    
    # Extracting values if matches are found, or setting them to None if not
    version = version_match.group(1) if version_match else None
    algorithm = algorithm_match.group(1) if algorithm_match else None
    public_key = key_match.group(1) if key_match else None
    
    return {
        "version": version,
        "algorithm": algorithm,
        "public_key": public_key
    }


async def get_dkim_verified(domain_name: str, selector: str):
    dkim_domain = f"{selector}._domainkey.{domain_name}"
    records = []
    try:
        resolver = Resolver()
        answers = resolver.resolve(dkim_domain, 'TXT')
        for answer in answers:
            record = answer.to_text().strip('"')
            dkim_record_object = parse_dkim_record(record)
            records.append(dkim_record_object)
        return records
    except:
        return None