from typing import Optional, List

from vkbottle_types.responses import base, storage
from .base_category import BaseCategory


class StorageCategory(BaseCategory):
    async def get(
        self,
        key: Optional[str] = None,
        keys: Optional[List[str]] = None,
        user_id: Optional[int] = None,
        **kwargs
    ) -> storage.GetV5110ResponseModel:
        """Returns a value of variable with the name set by key parameter.
        :param key:
        :param keys:
        :param user_id:
        """

        params = self.get_set_params(locals())
        return storage.GetV5110Response(
            **await self.api.request("storage.get", params)
        ).response

    async def get_keys(
        self,
        user_id: Optional[int] = None,
        offset: Optional[int] = None,
        count: Optional[int] = None,
        **kwargs
    ) -> storage.GetKeysResponseModel:
        """Returns the names of all variables.
        :param user_id: user id, whose variables names are returned if they were requested with a server method.
        :param offset:
        :param count: amount of variable names the info needs to be collected from.
        """

        params = self.get_set_params(locals())
        return storage.GetKeysResponse(
            **await self.api.request("storage.getKeys", params)
        ).response

    async def set(
        self,
        key: str,
        value: Optional[str] = None,
        user_id: Optional[int] = None,
        **kwargs
    ) -> base.OkResponseModel:
        """Saves a value of variable with the name set by 'key' parameter.
        :param key:
        :param value:
        :param user_id:
        """

        params = self.get_set_params(locals())
        return base.OkResponse(**await self.api.request("storage.set", params)).response
