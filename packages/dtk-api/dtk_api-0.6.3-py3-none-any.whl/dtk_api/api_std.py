import asyncio
import logging
from datetime import datetime
from typing import Set, Tuple

from tbk_api import ItemInfo

from .api_async import DtkAsyncApi
from .gen import *

__all__ = ["DtkStdApi"]


class DtkStdApi(object):
    """
    大淘客标准化 接口
    """

    def __init__(self, **kwargs):
        self._api = DtkAsyncApi(**kwargs)

    async def get_goods_detail(self, tao_id: str) -> Optional[ItemInfo]:
        args = GoodsGetGoodsDetailsArgs(id="", goodsId=tao_id)
        data = await self._api.goods_get_goods_details(args)
        if data is None:
            return None
        return self.convert_to_item_info(data)

    async def get_multi_goods_detail(self, tao_ids: List[str]) -> List[ItemInfo]:
        future_list = map(self.get_goods_detail, tao_ids)
        ret_list, pending = await asyncio.wait(
            future_list
        )  # type: Set[asyncio.Task], Any
        data_list = list(map(lambda x: x.result(), iter(ret_list)))
        return list(filter(lambda x: x is not None, data_list))

    async def goods_explosive_goods_list(
        self, args: GoodsExplosiveGoodsListArgs
    ) -> Optional[List[ItemInfo]]:
        ret = await self._api.goods_explosive_goods_list(args)
        if ret is None:
            return None
        tao_ids = []
        for data in ret:
            tao_ids.append(data.goodsId)
        return await self.get_multi_goods_detail(tao_ids)

    async def goods_exclusive_goods_list(
        self, args: GoodsExclusiveGoodsListArgs
    ) -> Optional[List[ItemInfo]]:
        ret = await self._api.goods_exclusive_goods_list(args)
        if ret is None:
            return None
        tao_ids = []
        for data in ret:
            tao_ids.append(data.goodsId)
        return await self.get_multi_goods_detail(tao_ids)

    async def goods_nine_op_goods_list(
        self, args: GoodsNineOpGoodsListArgs
    ) -> Optional[List[ItemInfo]]:
        ret = await self._api.goods_nine_op_goods_list(args)
        ret = ret.list
        if ret is None:
            return None
        tao_ids = []
        for data in ret:
            tao_ids.append(data.goodsId)
        return await self.get_multi_goods_detail(tao_ids)

    async def category_ddq_goods_list(
        self, args: CategoryDdqGoodsListArgs
    ) -> Optional[Tuple[List[ItemInfo], List[CategoryDdqGoodsListRespRoundslist]]]:
        result = await self._api.category_ddq_goods_list(args)
        ret = result.goodsList
        if ret is None:
            return None
        tao_ids = []
        for data in ret:
            tao_ids.append(data.goodsId)
        return await self.get_multi_goods_detail(tao_ids), result.roundsList

    async def goods_get_ranking_list(
        self, args: GoodsGetRankingListArgs
    ) -> Optional[List[ItemInfo]]:
        ret = await self._api.goods_get_ranking_list(args)
        if ret is None:
            return None
        tao_ids = []
        for data in ret:
            tao_ids.append(data.goodsId)
        return await self.get_multi_goods_detail(tao_ids)

    async def goods_list_super_goods(
        self, args: GoodsListSuperGoodsArgs
    ) -> Optional[List[ItemInfo]]:
        ret = await self._api.goods_list_super_goods(args)
        if ret is None:
            return None
        tao_ids = []
        for data in ret:
            tao_ids.append(data.goodsId)
        return await self.get_multi_goods_detail(tao_ids)

    async def goods_list_similer_goods_by_open(
        self, args: GoodsListSimilerGoodsByOpenArgs
    ) -> Optional[List[ItemInfo]]:
        ret = await self._api.goods_list_similer_goods_by_open(args)
        if ret is None:
            return None
        tao_ids = []
        for data in ret:
            tao_ids.append(data.goodsId)
        return await self.get_multi_goods_detail(tao_ids)

    async def goods_get_goods_list(
        self, args: GoodsGetGoodsListArgs
    ) -> Optional[List[ItemInfo]]:
        ret = await self._api.goods_get_goods_list(args)
        if ret is None:
            return None
        tao_ids = []
        for data in ret:
            tao_ids.append(data.goodsId)
        return await self.get_multi_goods_detail(tao_ids)

    async def goods_get_dtk_search_goods(
        self, args: GoodsGetDtkSearchGoodsArgs
    ) -> Optional[List[ItemInfo]]:
        ret = await self._api.goods_get_dtk_search_goods(args)
        ret = ret.list
        if ret is None:
            return None
        tao_ids = []
        for data in ret:
            tao_ids.append(data.goodsId)
        return await self.get_multi_goods_detail(tao_ids)

    async def tb_service_get_tb_service(
        self, args: TbServiceGetTbServiceArgs
    ) -> Optional[List[ItemInfo]]:
        ret = await self._api.tb_service_get_tb_service(args)
        if ret is None:
            return None
        tao_ids = []
        for data in ret:
            tao_ids.append(str(data.item_id))
        return await self.get_multi_goods_detail(tao_ids)

    @staticmethod
    def convert_to_item_info(data: GoodsGetGoodsDetailsResp) -> ItemInfo:
        logger = logging.getLogger("root")
        try:
            pics = json.loads(data.detailPics)
            tao_details = list(map(lambda x: x["img"], pics))
        except json.JSONDecodeError as e:  # 吃掉这个异常
            logger.error(f"decode pic failed: {e}")
            tao_details = []

        def convert_to_time(s: str) -> Optional[datetime]:
            try:
                return datetime.fromisoformat(s)
            except ValueError as err:
                logger.error(f"convert to time failed: {err}")
                return None

        return ItemInfo(
            tao_id=data.goodsId,
            tao_img=data.mainPic,
            tao_link=data.itemLink,
            tao_details=tao_details,
            title_long=data.title,
            title_short=data.dtitle,
            price_origin=data.originalPrice,
            price_actual=data.actualPrice,
            price_coupon=data.couponPrice,
            seller_id=data.sellerId,
            seller_name=data.shopName,
            seller_logo=data.shopLogo,
            seller_level=data.shopLevel,
            score_dsr=data.dsrScore,
            score_ship=data.shipScore,
            score_service=data.serviceScore,
            percent_dsr=data.dsrPercent,
            percent_ship=data.shipPercent,
            percent_service=data.servicePercent,
            commission_rate=(data.commissionRate / 100.0),
            commission_money=(data.actualPrice / 100.0 * data.commissionRate),
            sale_month=data.monthSales,
            sale_day=data.dailySales,
            sale_two_hours=data.twoHoursSales,
            coupon_start_time=convert_to_time(data.couponStartTime),
            coupon_end_time=convert_to_time(data.couponEndTime),
            coupon_total_num=data.couponTotalNum,
            coupon_recv_num=data.couponReceiveNum,
            coupon_link=data.couponLink,
            yun_fei_xian=data.yunfeixian > 0,
        )
