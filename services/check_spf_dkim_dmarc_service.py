from helpers.get_spf_record import check_spf_record
from helpers.get_dmarc_record import get_dmarc_record
from helpers.get_dkim_verified import get_dkim_verified
from helpers.logger import logger
import asyncio

async def check_spf_dkim_dmarc_service(domain_name: str):
    logger.info(f"Checking records for {domain_name}")
    spf = check_spf_record(domain_name)
    dkim = get_dkim_verified(domain_name, "selector1")
    dmarc = get_dmarc_record(domain_name)

    spf_result, dkim_result, dmarc_result = await asyncio.gather(spf, dkim, dmarc)

    return {
        "spf_results": spf_result,
        "dkim_results": dkim_result,
        "dmarc_results": dmarc_result
    }