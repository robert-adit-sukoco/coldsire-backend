from dns.resolver import Resolver
import re

def parse_dmarc_record(dkim_record):
    # Regular expressions to match each part
    version_match = re.search(r'v=([^;]+)', dkim_record)
    policy_match = re.search(r'p=([^;]+)', dkim_record)
    
    # Extracting values if matches are found, or setting them to None if not
    version = version_match.group(1) if version_match else None
    policy = policy_match.group(1) if policy_match else None
    
    return {
        "version": version,
        "policy": policy
    }

async def get_dmarc_record(domain_name: str):
    dmarc_domain = f"_dmarc.{domain_name}"
    records = []
    try:
        resolver = Resolver()
        answers = resolver.resolve(dmarc_domain, 'TXT')
        for answer in answers:
            record = answer.to_text()
            if "v=DMARC1" in record:
                record_str = record.strip('"')
                dmarc_record_object = parse_dmarc_record(record_str)
                records.append(dmarc_record_object)
        return records
    except:
        return None