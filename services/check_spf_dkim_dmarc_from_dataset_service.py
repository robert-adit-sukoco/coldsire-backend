from helpers.get_spf_record import check_spf_record
from helpers.get_dmarc_record import get_dmarc_record
from helpers.get_dkim_verified import get_dkim_verified
from helpers.logger import logger
from helpers.validators import validate_domain_name
from .check_spf_dkim_dmarc_service import check_spf_dkim_dmarc_service
import math



async def check_spf_dkim_dmarc_from_dataset_service(page):
    # Read domain_names.txt
    file_object = open('./domain_names.txt', 'r')
    file_data = file_object.read()
    all_domains = file_data.splitlines()
    file_object.close()

    size = 10

    total_pages = math.ceil(len(all_domains) / size)

    if (page > total_pages):
        return []

    lower_offset = (page - 1) * size
    upper_offset = min(len(all_domains), (page * size))

    get_domains = all_domains[lower_offset:upper_offset]

    results = []

    for i in range(len(get_domains)):
        domain_name = get_domains[i]
        if (not validate_domain_name(domain_name)):
            result_obj = {
                "domain_name": domain_name,
                "spf_results": None,
                "dkim_results": None,
                "dmarc_results": None,
            }
            results.append(result_obj)
        result = await check_spf_dkim_dmarc_service(domain_name)
        result_obj = {
            "domain_name": domain_name,
            "spf_results": result["spf_results"],
            "dkim_results": result["dkim_results"],
            "dmarc_results": result["dmarc_results"],
        }
        results.append(result_obj)

    return {
        "pagination": {
            "total_pages": total_pages,
            "total_data": len(all_domains)
        },
        "results" : results
    }
