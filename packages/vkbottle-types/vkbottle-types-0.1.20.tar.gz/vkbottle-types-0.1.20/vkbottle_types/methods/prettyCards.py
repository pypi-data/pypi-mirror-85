from typing import Optional, List

from vkbottle_types.responses import prettyCards
from .base_category import BaseCategory


class PrettyCardsCategory(BaseCategory):
    async def create(
        self,
        owner_id: int,
        photo: str,
        title: str,
        link: str,
        price: Optional[str] = None,
        price_old: Optional[str] = None,
        button: Optional[str] = None,
        **kwargs
    ) -> prettyCards.CreateResponseModel:
        """prettyCards.create method
        :param owner_id:
        :param photo:
        :param title:
        :param link:
        :param price:
        :param price_old:
        :param button:
        """

        params = self.get_set_params(locals())
        return prettyCards.CreateResponse(
            **await self.api.request("prettyCards.create", params)
        ).response

    async def delete(
        self, owner_id: int, card_id: int, **kwargs
    ) -> prettyCards.DeleteResponseModel:
        """prettyCards.delete method
        :param owner_id:
        :param card_id:
        """

        params = self.get_set_params(locals())
        return prettyCards.DeleteResponse(
            **await self.api.request("prettyCards.delete", params)
        ).response

    async def edit(
        self,
        owner_id: int,
        card_id: int,
        photo: Optional[str] = None,
        title: Optional[str] = None,
        link: Optional[str] = None,
        price: Optional[str] = None,
        price_old: Optional[str] = None,
        button: Optional[str] = None,
        **kwargs
    ) -> prettyCards.EditResponseModel:
        """prettyCards.edit method
        :param owner_id:
        :param card_id:
        :param photo:
        :param title:
        :param link:
        :param price:
        :param price_old:
        :param button:
        """

        params = self.get_set_params(locals())
        return prettyCards.EditResponse(
            **await self.api.request("prettyCards.edit", params)
        ).response

    async def get(
        self,
        owner_id: int,
        offset: Optional[int] = None,
        count: Optional[int] = None,
        **kwargs
    ) -> prettyCards.GetResponseModel:
        """prettyCards.get method
        :param owner_id:
        :param offset:
        :param count:
        """

        params = self.get_set_params(locals())
        return prettyCards.GetResponse(
            **await self.api.request("prettyCards.get", params)
        ).response

    async def get_by_id(
        self, owner_id: int, card_ids: List[int], **kwargs
    ) -> prettyCards.GetByIdResponseModel:
        """prettyCards.getById method
        :param owner_id:
        :param card_ids:
        """

        params = self.get_set_params(locals())
        return prettyCards.GetByIdResponse(
            **await self.api.request("prettyCards.getById", params)
        ).response

    async def get_upload_url(self, **kwargs) -> prettyCards.GetUploadURLResponseModel:
        """prettyCards.getUploadURL method"""

        params = self.get_set_params(locals())
        return prettyCards.GetUploadURLResponse(
            **await self.api.request("prettyCards.getUploadURL", params)
        ).response
