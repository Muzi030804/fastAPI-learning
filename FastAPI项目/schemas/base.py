from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class NewsItemBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: int = Field(..., alias="categoryId")
    views: int
    publish_time: Optional[datetime] = Field(None, alias="publishTime")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class NewsListItem(NewsItemBase):
    """新闻列表缓存用: 补齐未命中时 ORM 会输出的字段, 避免命中前后结构不一致"""

    content: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )