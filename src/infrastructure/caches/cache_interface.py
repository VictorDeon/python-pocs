class CacheClientInterface:
    async def set_value(self, key: str, value: str, expire: int = None) -> None:
        pass

    async def get_value(self, key: str) -> str:
        pass
