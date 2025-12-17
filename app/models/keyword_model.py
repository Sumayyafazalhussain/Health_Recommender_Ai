
from pydantic import BaseModel, Field

class KeywordIn(BaseModel):
    keyword: str = Field(..., description="Keyword to match")
    category_id: str = Field(..., description="Category ID")
    match_type: str = Field("partial", description="Match type: 'exact', 'partial', or 'type'")

class KeywordOut(KeywordIn):
    id: str = Field(..., alias="_id")
    
    class Config:
        populate_by_name = True