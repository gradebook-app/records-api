import httpx
from common.genesis import SchoolDistrict, get_genesis_config
from urllib.parse import parse_qs

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


async def validateGenesisAuthToken(token: str) -> bool:
    genesis_config = get_genesis_config(SchoolDistrict.SB)
    root_url = genesis_config.root
    main_route = genesis_config.main
    home_route = f"{root_url}{main_route}?tab1=studentdata&tab2=studentsummary"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            home_route, cookies={"JSESSIONID": token}, headers=headers
        )
        location: str = response.headers.get("Location")
        if not location:
            return False

        # TODO: Check if the studentId matches with the studentId associated with the userId
        studentId = parse_qs(location).get("studentid")
        if studentId:
            return True

    return False
