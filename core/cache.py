from core.scraper import get_keys_by_country


class VPNKeyCache:
    def __init__(self):
        self.cached_keys = {}

    async def fetch_keys(self):

        self.cached_keys = await get_keys_by_country(limit=16)

    def get_keys_for_country(self, country):

        return self.cached_keys.get(country, [])



vpn_key_cache = VPNKeyCache()