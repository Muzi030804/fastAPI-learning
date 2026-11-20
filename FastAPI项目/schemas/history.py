from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase



class HistoryAddRequest(BaseModel):
    news_id: int = Field(...,alias="newsId")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,

    )

# 规划两个类: 一个是新闻模型类 + 浏览历史的模型类


class HistoryNewsResponse(NewsItemBase):
    history_id: int = Field(..., alias="historyId")
    view_time: datetime = Field(..., alias="viewTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

# 浏览历史列表接口响应模型类
class HistoryListResponse(BaseModel):
    list: list[HistoryNewsResponse]
    total: int
    has_more: bool = Field(..., alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )