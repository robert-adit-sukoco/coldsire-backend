from dns.resolver import Resolver
import re

def parse_spf_record(spf_record):
    # Regular expression to capture the SPF version
    version_match = re.search(r'v=([^ ]+)', spf_record)
    # Split the record to get mechanisms
    mechanisms = spf_record.split()[1:]  # Exclude the version part at the start

    # Extract values or set them to None if not found
    version = version_match.group(1) if version_match else None

    return {
        "version": version,
        "mechanisms": mechanisms
    }


async def check_spf_record(domain_name: str):
    records = []

    try:
        resolver = Resolver()
        answers = resolver.resolve(domain_name, 'TXT')
        for answer in answers:
            record = answer.to_text()
            if "v=spf1" in record:
                record_str = record.strip('"')
                spf_record_object = parse_spf_record(record_str)
                records.append(spf_record_object)
        return records
    except Exception as e:
        
        print(e)
        return None