

from fastapi import APIRouter, HTTPException, status
from app.models.category_model import CategoryIn
from app.models.keyword_model import KeywordIn
from app.models.rule_model import RuleIn
from app.db.mongo import get_categories_col, get_keywords_col, get_rules_col

router = APIRouter(prefix="/admin", tags=["admin"])

# ==================== CATEGORIES ====================
@router.post("/categories", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryIn):
    """Create a new category"""
    categories_col = get_categories_col()
    
    existing = categories_col.find_one({"name": category.name})
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Category '{category.name}' already exists"
        )
    
    result = categories_col.insert_one(category.model_dump())
    return {
        "status": "success",
        "message": "Category created",
        "id": str(result.inserted_id)
    }

@router.get("/categories", response_model=dict)
async def list_categories():
    """Get all categories"""
    categories_col = get_categories_col()
    categories = list(categories_col.find({}))
    
    for cat in categories:
        cat["_id"] = str(cat["_id"])
    
    return {
        "status": "success",
        "count": len(categories),
        "categories": categories
    }

# ==================== KEYWORDS ====================
@router.post("/keywords", response_model=dict)
async def create_keyword(keyword: KeywordIn):
    """Add a keyword for category detection"""
    keywords_col = get_keywords_col()
    categories_col = get_categories_col()
    
    # Validate category exists
    category = categories_col.find_one({"_id": keyword.category_id})
    if not category:
        raise HTTPException(
            status_code=404,
            detail=f"Category '{keyword.category_id}' not found"
        )
    
    result = keywords_col.insert_one(keyword.model_dump())
    return {
        "status": "success",
        "message": "Keyword added",
        "id": str(result.inserted_id)
    }

@router.get("/keywords", response_model=dict)
async def list_keywords():
    """Get all keywords"""
    keywords_col = get_keywords_col()
    keywords = list(keywords_col.find({}))
    
    for kw in keywords:
        kw["_id"] = str(kw["_id"])
    
    return {
        "status": "success",
        "count": len(keywords),
        "keywords": keywords
    }

# ==================== RULES ====================
@router.post("/rules", response_model=dict)
async def create_rule(rule: RuleIn):
    """Create a recommendation rule"""
    rules_col = get_rules_col()
    categories_col = get_categories_col()
    
    # Validate trigger category exists
    trigger_cat = categories_col.find_one({"_id": rule.trigger_category_id})
    if not trigger_cat:
        raise HTTPException(
            status_code=404,
            detail=f"Trigger category '{rule.trigger_category_id}' not found"
        )
    
    # Validate recommended categories
    for rec_id in rule.recommended_category_ids:
        rec_cat = categories_col.find_one({"_id": rec_id})
        if not rec_cat:
            raise HTTPException(
                status_code=404,
                detail=f"Recommended category '{rec_id}' not found"
            )
    
    # Check if rule exists
    existing = rules_col.find_one({"trigger_category_id": rule.trigger_category_id})
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Rule for '{rule.trigger_category_id}' already exists"
        )
    
    result = rules_col.insert_one(rule.model_dump())
    return {
        "status": "success",
        "message": "Rule created",
        "id": str(result.inserted_id)
    }

@router.get("/rules", response_model=dict)
async def list_rules():
    """Get all rules with details"""
    rules_col = get_rules_col()
    categories_col = get_categories_col()
    
    rules = list(rules_col.find({}))
    
    for rule in rules:
        rule["_id"] = str(rule["_id"])
        
        # Add trigger category name
        trigger_cat = categories_col.find_one({"_id": rule.get("trigger_category_id")})
        if trigger_cat:
            rule["trigger_category_name"] = trigger_cat.get("name")
        
        # Add recommended category names
        recommended_names = []
        for cat_id in rule.get("recommended_category_ids", []):
            rec_cat = categories_col.find_one({"_id": cat_id})
            if rec_cat:
                recommended_names.append(rec_cat.get("name"))
        rule["recommended_category_names"] = recommended_names
    
    return {
        "status": "success",
        "count": len(rules),
        "rules": rules
    }

@router.delete("/reset", response_model=dict)
async def reset_database():
    """Reset database (for testing)"""
    get_categories_col().delete_many({})
    get_keywords_col().delete_many({})
    get_rules_col().delete_many({})
    
    return {
        "status": "success",
        "message": "Database reset"
    }

@router.get("/health", response_model=dict)
async def admin_health():
    """Admin health check"""
    try:
        # Test database
        categories_count = get_categories_col().count_documents({})
        keywords_count = get_keywords_col().count_documents({})
        rules_count = get_rules_col().count_documents({})
        
        return {
            "status": "healthy",
            "database": {
                "categories": categories_count,
                "keywords": keywords_count,
                "rules": rules_count
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")