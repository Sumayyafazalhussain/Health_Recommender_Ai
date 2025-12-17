
from pydantic import BaseModel, Field
from typing import List

class RuleIn(BaseModel):
    trigger_category_id: str = Field(..., description="Category that triggers this rule")
    recommended_category_ids: List[str] = Field(..., description="Categories to recommend")
    ai_prompt_template: str = Field(
        default="User is near a {trigger_category}. Suggest healthy alternatives like {alternatives}.",
        description="Template for AI message generation"
    )

class RuleOut(RuleIn):
    id: str = Field(..., alias="_id")
    
    class Config:
        populate_by_name = True