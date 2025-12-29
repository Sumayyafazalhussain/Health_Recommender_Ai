

# from sqlalchemy.orm import Session
# from typing import List, Dict, Any, Optional
# import uuid
# from datetime import datetime

# from app.db.neon_connection import SessionLocal, Category, Keyword, Rule, Menu

# class NeonService:
    
#     # ========== CATEGORIES ==========
#     def get_categories(self) -> List[Dict[str, Any]]:
#         """Get all categories from Neon"""
#         db = SessionLocal()
#         try:
#             categories = db.query(Category).all()
#             result = []
#             for cat in categories:
#                 result.append({
#                     "_id": cat.id,
#                     "id": cat.id,
#                     "name": cat.name,
#                     "description": cat.description,
#                     "is_unhealthy": cat.is_unhealthy,
#                     "created_at": cat.created_at.isoformat() if cat.created_at else None
#                 })
#             return result
#         except Exception as e:
#             print(f"❌ Error getting categories: {e}")
#             return []
#         finally:
#             db.close()
    
#     def get_category_by_id(self, category_id: str) -> Optional[Dict[str, Any]]:
#         """Get category by ID"""
#         db = SessionLocal()
#         try:
#             category = db.query(Category).filter(Category.id == category_id).first()
#             if category:
#                 return {
#                     "id": category.id,
#                     "name": category.name,
#                     "description": category.description,
#                     "is_unhealthy": category.is_unhealthy
#                 }
#             return None
#         finally:
#             db.close()
    
#     def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
#         """Create a new category"""
#         db = SessionLocal()
#         try:
#             # Check if category already exists
#             existing = db.query(Category).filter(Category.name == category_data["name"]).first()
#             if existing:
#                 return {
#                     "status": "error",
#                     "message": f"Category '{category_data['name']}' already exists"
#                 }
            
#             # Generate ID
#             category_id = str(uuid.uuid4())
            
#             category = Category(
#                 id=category_id,
#                 name=category_data["name"],
#                 description=category_data.get("description"),
#                 is_unhealthy=category_data.get("is_unhealthy", True)
#             )
            
#             db.add(category)
#             db.commit()
            
#             return {
#                 "status": "success",
#                 "message": "Category created",
#                 "id": category_id
#             }
            
#         except Exception as e:
#             db.rollback()
#             return {
#                 "status": "error",
#                 "message": f"Database error: {str(e)}"
#             }
#         finally:
#             db.close()
    
#     # ========== KEYWORDS ==========
#     def get_keywords(self) -> List[Dict[str, Any]]:
#         """Get all keywords from Neon"""
#         db = SessionLocal()
#         try:
#             keywords = db.query(Keyword).all()
#             result = []
#             for kw in keywords:
#                 result.append({
#                     "_id": kw.id,
#                     "id": kw.id,
#                     "keyword": kw.keyword,
#                     "category_id": kw.category_id,
#                     "match_type": kw.match_type
#                 })
#             return result
#         except Exception as e:
#             print(f"❌ Error getting keywords: {e}")
#             return []
#         finally:
#             db.close()
    
#     def create_keyword(self, keyword_data: Dict[str, Any]) -> Dict[str, Any]:
#         """Add a keyword for category detection"""
#         db = SessionLocal()
#         try:
#             # Check if category exists
#             category = self.get_category_by_id(keyword_data['category_id'])
#             if not category:
#                 return {
#                     "status": "error",
#                     "message": f"Category '{keyword_data['category_id']}' not found"
#                 }
            
#             # Generate ID
#             keyword_id = str(uuid.uuid4())
            
#             keyword = Keyword(
#                 id=keyword_id,
#                 keyword=keyword_data["keyword"],
#                 category_id=keyword_data["category_id"],
#                 match_type=keyword_data.get("match_type", "partial")
#             )
            
#             db.add(keyword)
#             db.commit()
            
#             return {
#                 "status": "success",
#                 "message": "Keyword added",
#                 "id": keyword_id
#             }
            
#         except Exception as e:
#             db.rollback()
#             return {
#                 "status": "error",
#                 "message": f"Database error: {str(e)}"
#             }
#         finally:
#             db.close()
    
#     # ========== RULES ==========
#     def get_rules(self) -> List[Dict[str, Any]]:
#         """Get all rules from Neon"""
#         db = SessionLocal()
#         try:
#             rules = db.query(Rule).all()
#             result = []
#             for rule in rules:
#                 rule_data = {
#                     "_id": rule.id,
#                     "id": rule.id,
#                     "trigger_category_id": rule.trigger_category_id,
#                     "ai_prompt_template": rule.ai_prompt_template
#                 }
                
#                 # Get recommended categories
#                 recommended_ids = []
#                 recommended_names = []
#                 for cat in rule.recommended_categories:
#                     recommended_ids.append(cat.id)
#                     recommended_names.append(cat.name)
                
#                 rule_data["recommended_category_ids"] = recommended_ids
#                 rule_data["recommended_category_names"] = recommended_names
                
#                 result.append(rule_data)
#             return result
#         except Exception as e:
#             print(f"❌ Error getting rules: {e}")
#             return []
#         finally:
#             db.close()
    
#     def create_rule(self, rule_data: Dict[str, Any]) -> Dict[str, Any]:
#         """Create a recommendation rule"""
#         db = SessionLocal()
#         try:
#             # Validate trigger category exists
#             trigger_cat = self.get_category_by_id(rule_data['trigger_category_id'])
#             if not trigger_cat:
#                 return {
#                     "status": "error",
#                     "message": f"Trigger category '{rule_data['trigger_category_id']}' not found"
#                 }
            
#             # Check if rule exists
#             existing = db.query(Rule).filter(
#                 Rule.trigger_category_id == rule_data['trigger_category_id']
#             ).first()
            
#             if existing:
#                 return {
#                     "status": "error",
#                     "message": f"Rule for '{rule_data['trigger_category_id']}' already exists"
#                 }
            
#             # Create rule
#             rule_id = str(uuid.uuid4())
#             rule = Rule(
#                 id=rule_id,
#                 trigger_category_id=rule_data['trigger_category_id'],
#                 ai_prompt_template=rule_data.get(
#                     'ai_prompt_template',
#                     "User is near a {trigger_category}. Suggest healthy alternatives like {alternatives}."
#                 )
#             )
            
#             db.add(rule)
#             db.flush()  # Get rule ID
            
#             # Add recommended categories
#             for cat_id in rule_data.get('recommended_category_ids', []):
#                 cat = self.get_category_by_id(cat_id)
#                 if cat:
#                     rule.recommended_categories.append(db.query(Category).get(cat_id))
            
#             db.commit()
            
#             return {
#                 "status": "success",
#                 "message": "Rule created",
#                 "id": rule_id
#             }
            
#         except Exception as e:
#             db.rollback()
#             return {
#                 "status": "error",
#                 "message": f"Database error: {str(e)}"
#             }
#         finally:
#             db.close()
    
#     # ========== MENUS ==========
#     def get_menus_count(self) -> int:
#         """Get count of menus"""
#         db = SessionLocal()
#         try:
#             return db.query(Menu).count()
#         finally:
#             db.close()
    
#     # ========== HEALTH CHECK ==========
#     def health_check(self) -> Dict[str, Any]:
#         """Check database health"""
#         db = SessionLocal()
#         try:
#             categories_count = db.query(Category).count()
#             keywords_count = db.query(Keyword).count()
#             rules_count = db.query(Rule).count()
#             menus_count = db.query(Menu).count()
            
#             return {
#                 "status": "healthy",
#                 "database": "neon_postgresql",
#                 "counts": {
#                     "categories": categories_count,
#                     "keywords": keywords_count,
#                     "rules": rules_count,
#                     "menus": menus_count
#                 }
#             }
#         except Exception as e:
#             return {
#                 "status": "unhealthy",
#                 "database": "neon_postgresql",
#                 "error": str(e)
#             }
#         finally:
#             db.close()

# # Create global instance
# neon_db_service = NeonService()











# app/services/neon_service.py
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime

from app.db.neon_connection import SessionLocal, Category, Keyword, Rule, Menu

class NeonService:
    
    def __init__(self):
        """Initialize Neon service"""
        print("✅ NeonService initialized")
    
    # ========== CATEGORIES ==========
    def get_categories(self) -> List[Dict[str, Any]]:
        """Get all categories from Neon"""
        db = SessionLocal()
        try:
            categories = db.query(Category).all()
            result = []
            for cat in categories:
                result.append({
                    "_id": cat.id,
                    "id": cat.id,
                    "name": cat.name,
                    "description": cat.description,
                    "is_unhealthy": cat.is_unhealthy,
                    "created_at": cat.created_at.isoformat() if cat.created_at else None
                })
            return result
        except Exception as e:
            print(f"❌ Error getting categories: {e}")
            return []
        finally:
            db.close()
    
    def get_category_by_id(self, category_id: str) -> Optional[Dict[str, Any]]:
        """Get category by ID"""
        db = SessionLocal()
        try:
            category = db.query(Category).filter(Category.id == category_id).first()
            if category:
                return {
                    "id": category.id,
                    "name": category.name,
                    "description": category.description,
                    "is_unhealthy": category.is_unhealthy
                }
            return None
        finally:
            db.close()
    
    def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new category"""
        db = SessionLocal()
        try:
            # Check if category already exists
            existing = db.query(Category).filter(Category.name == category_data["name"]).first()
            if existing:
                return {
                    "status": "error",
                    "message": f"Category '{category_data['name']}' already exists"
                }
            
            # Generate ID
            category_id = str(uuid.uuid4())
            
            category = Category(
                id=category_id,
                name=category_data["name"],
                description=category_data.get("description"),
                is_unhealthy=category_data.get("is_unhealthy", True)
            )
            
            db.add(category)
            db.commit()
            
            return {
                "status": "success",
                "message": "Category created",
                "id": category_id
            }
            
        except Exception as e:
            db.rollback()
            return {
                "status": "error",
                "message": f"Database error: {str(e)}"
            }
        finally:
            db.close()
    
    # ========== KEYWORDS ==========
    def get_keywords(self) -> List[Dict[str, Any]]:
        """Get all keywords from Neon"""
        db = SessionLocal()
        try:
            keywords = db.query(Keyword).all()
            result = []
            for kw in keywords:
                result.append({
                    "_id": kw.id,
                    "id": kw.id,
                    "keyword": kw.keyword,
                    "category_id": kw.category_id,
                    "match_type": kw.match_type
                })
            return result
        except Exception as e:
            print(f"❌ Error getting keywords: {e}")
            return []
        finally:
            db.close()
    
    def create_keyword(self, keyword_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a keyword for category detection"""
        db = SessionLocal()
        try:
            # Check if category exists
            category = self.get_category_by_id(keyword_data['category_id'])
            if not category:
                return {
                    "status": "error",
                    "message": f"Category '{keyword_data['category_id']}' not found"
                }
            
            # Generate ID
            keyword_id = str(uuid.uuid4())
            
            keyword = Keyword(
                id=keyword_id,
                keyword=keyword_data["keyword"],
                category_id=keyword_data["category_id"],
                match_type=keyword_data.get("match_type", "partial")
            )
            
            db.add(keyword)
            db.commit()
            
            return {
                "status": "success",
                "message": "Keyword added",
                "id": keyword_id
            }
            
        except Exception as e:
            db.rollback()
            return {
                "status": "error",
                "message": f"Database error: {str(e)}"
            }
        finally:
            db.close()
    
    # ========== RULES ==========
    def get_rules(self) -> List[Dict[str, Any]]:
        """Get all rules from Neon"""
        db = SessionLocal()
        try:
            rules = db.query(Rule).all()
            result = []
            for rule in rules:
                rule_data = {
                    "_id": rule.id,
                    "id": rule.id,
                    "trigger_category_id": rule.trigger_category_id,
                    "ai_prompt_template": rule.ai_prompt_template
                }
                
                # Get recommended categories
                recommended_ids = []
                recommended_names = []
                for cat in rule.recommended_categories:
                    recommended_ids.append(cat.id)
                    recommended_names.append(cat.name)
                
                rule_data["recommended_category_ids"] = recommended_ids
                rule_data["recommended_category_names"] = recommended_names
                
                result.append(rule_data)
            return result
        except Exception as e:
            print(f"❌ Error getting rules: {e}")
            return []
        finally:
            db.close()
    
    def create_rule(self, rule_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a recommendation rule"""
        db = SessionLocal()
        try:
            # Validate trigger category exists
            trigger_cat = self.get_category_by_id(rule_data['trigger_category_id'])
            if not trigger_cat:
                return {
                    "status": "error",
                    "message": f"Trigger category '{rule_data['trigger_category_id']}' not found"
                }
            
            # Check if rule exists
            existing = db.query(Rule).filter(
                Rule.trigger_category_id == rule_data['trigger_category_id']
            ).first()
            
            if existing:
                return {
                    "status": "error",
                    "message": f"Rule for '{rule_data['trigger_category_id']}' already exists"
                }
            
            # Create rule
            rule_id = str(uuid.uuid4())
            rule = Rule(
                id=rule_id,
                trigger_category_id=rule_data['trigger_category_id'],
                ai_prompt_template=rule_data.get(
                    'ai_prompt_template',
                    "User is near a {trigger_category}. Suggest healthy alternatives like {alternatives}."
                )
            )
            
            db.add(rule)
            db.flush()  # Get rule ID
            
            # Add recommended categories
            for cat_id in rule_data.get('recommended_category_ids', []):
                cat = self.get_category_by_id(cat_id)
                if cat:
                    rule.recommended_categories.append(db.query(Category).get(cat_id))
            
            db.commit()
            
            return {
                "status": "success",
                "message": "Rule created",
                "id": rule_id
            }
            
        except Exception as e:
            db.rollback()
            return {
                "status": "error",
                "message": f"Database error: {str(e)}"
            }
        finally:
            db.close()
    
    # ========== HEALTH CHECK ==========
    def health_check(self) -> Dict[str, Any]:
        """Check database health"""
        try:
            db = SessionLocal()
            categories_count = db.query(Category).count()
            keywords_count = db.query(Keyword).count()
            rules_count = db.query(Rule).count()
            menus_count = db.query(Menu).count()
            
            return {
                "status": "healthy",
                "database": "neon_postgresql",
                "counts": {
                    "categories": categories_count,
                    "keywords": keywords_count,
                    "rules": rules_count,
                    "menus": menus_count
                }
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "database": "neon_postgresql",
                "error": str(e)
            }
        finally:
            db.close()

# Create global instance
neon_db_service = NeonService()