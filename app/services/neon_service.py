# app/services/neon_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

from app.db.neon_connection import get_session_local, Category, Keyword, Rule, Menu

class NeonDatabaseService:
    """Service layer for Neon PostgreSQL operations"""
    
    def __init__(self):
        self.SessionLocal = get_session_local
    
    # ========== CATEGORY OPERATIONS ==========
    
    def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new category"""
        session = self.SessionLocal()
        try:
            # Generate ID if not provided
            if 'id' not in category_data:
                category_data['id'] = str(uuid.uuid4())
            
            category = Category(**category_data)
            session.add(category)
            session.commit()
            session.refresh(category)
            
            return {
                "status": "success",
                "message": "Category created",
                "id": category.id
            }
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """Get all categories"""
        session = self.SessionLocal()
        try:
            categories = session.query(Category).all()
            return [
                {
                    "_id": cat.id,
                    "id": cat.id,
                    "name": cat.name,
                    "description": cat.description,
                    "is_unhealthy": cat.is_unhealthy,
                    "created_at": cat.created_at.isoformat() if cat.created_at else None
                }
                for cat in categories
            ]
        finally:
            session.close()
    
    def get_category_by_id(self, category_id: str) -> Optional[Dict[str, Any]]:
        """Get category by ID"""
        session = self.SessionLocal()
        try:
            category = session.query(Category).filter(Category.id == category_id).first()
            if category:
                return {
                    "_id": category.id,
                    "id": category.id,
                    "name": category.name,
                    "description": category.description,
                    "is_unhealthy": category.is_unhealthy
                }
            return None
        finally:
            session.close()
    
    # ========== KEYWORD OPERATIONS ==========
    
    def create_keyword(self, keyword_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a keyword for category detection"""
        session = self.SessionLocal()
        try:
            # Validate category exists
            category = session.query(Category).filter(Category.id == keyword_data['category_id']).first()
            if not category:
                raise ValueError(f"Category '{keyword_data['category_id']}' not found")
            
            # Generate ID
            keyword_data['id'] = str(uuid.uuid4())
            keyword = Keyword(**keyword_data)
            session.add(keyword)
            session.commit()
            session.refresh(keyword)
            
            return {
                "status": "success",
                "message": "Keyword added",
                "id": keyword.id
            }
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_keywords(self) -> List[Dict[str, Any]]:
        """Get all keywords"""
        session = self.SessionLocal()
        try:
            keywords = session.query(Keyword).all()
            return [
                {
                    "_id": kw.id,
                    "id": kw.id,
                    "keyword": kw.keyword,
                    "category_id": kw.category_id,
                    "match_type": kw.match_type
                }
                for kw in keywords
            ]
        finally:
            session.close()
    
    def search_keywords(self, search_term: str) -> List[Dict[str, Any]]:
        """Search keywords by term"""
        session = self.SessionLocal()
        try:
            keywords = session.query(Keyword).filter(
                Keyword.keyword.ilike(f"%{search_term}%")
            ).all()
            return [
                {
                    "id": kw.id,
                    "keyword": kw.keyword,
                    "category_id": kw.category_id,
                    "match_type": kw.match_type
                }
                for kw in keywords
            ]
        finally:
            session.close()
    
    # ========== RULE OPERATIONS ==========
    
    def create_rule(self, rule_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a recommendation rule"""
        session = self.SessionLocal()
        try:
            # Validate trigger category exists
            trigger_cat = session.query(Category).filter(Category.id == rule_data['trigger_category_id']).first()
            if not trigger_cat:
                raise ValueError(f"Trigger category '{rule_data['trigger_category_id']}' not found")
            
            # Get recommended categories
            recommended_categories = []
            for cat_id in rule_data.get('recommended_category_ids', []):
                rec_cat = session.query(Category).filter(Category.id == cat_id).first()
                if not rec_cat:
                    raise ValueError(f"Recommended category '{cat_id}' not found")
                recommended_categories.append(rec_cat)
            
            # Check if rule exists
            existing = session.query(Rule).filter(
                Rule.trigger_category_id == rule_data['trigger_category_id']
            ).first()
            if existing:
                raise ValueError(f"Rule for '{rule_data['trigger_category_id']}' already exists")
            
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
            
            # Add recommended categories
            rule.recommended_categories = recommended_categories
            
            session.add(rule)
            session.commit()
            
            return {
                "status": "success",
                "message": "Rule created",
                "id": rule.id
            }
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_rules(self) -> List[Dict[str, Any]]:
        """Get all rules with details"""
        session = self.SessionLocal()
        try:
            rules = session.query(Rule).all()
            result = []
            
            for rule in rules:
                rule_data = {
                    "_id": rule.id,
                    "id": rule.id,
                    "trigger_category_id": rule.trigger_category_id,
                    "ai_prompt_template": rule.ai_prompt_template,
                    "recommended_category_ids": [cat.id for cat in rule.recommended_categories],
                    "created_at": rule.created_at.isoformat() if rule.created_at else None
                }
                
                # Add trigger category name
                if rule.trigger_category:
                    rule_data["trigger_category_name"] = rule.trigger_category.name
                
                # Add recommended category names
                recommended_names = []
                for cat in rule.recommended_categories:
                    recommended_names.append(cat.name)
                rule_data["recommended_category_names"] = recommended_names
                
                result.append(rule_data)
            
            return result
        finally:
            session.close()
    
    def get_rule_by_trigger_category(self, category_id: str) -> Optional[Dict[str, Any]]:
        """Get rule by trigger category ID"""
        session = self.SessionLocal()
        try:
            rule = session.query(Rule).filter(Rule.trigger_category_id == category_id).first()
            if rule:
                return {
                    "id": rule.id,
                    "trigger_category_id": rule.trigger_category_id,
                    "ai_prompt_template": rule.ai_prompt_template,
                    "recommended_category_ids": [cat.id for cat in rule.recommended_categories]
                }
            return None
        finally:
            session.close()
    
    # ========== MENU OPERATIONS ==========
    
    def create_menu(self, menu_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update a menu"""
        session = self.SessionLocal()
        try:
            # Check if menu exists
            existing = session.query(Menu).filter(Menu.place_id == menu_data['place_id']).first()
            
            if existing:
                # Update existing menu
                existing.items = menu_data['items']
                existing.last_updated = datetime.utcnow()
                message = "Menu updated"
                menu_id = existing.id
            else:
                # Create new menu
                menu_id = str(uuid.uuid4())
                menu = Menu(
                    id=menu_id,
                    place_id=menu_data['place_id'],
                    place_name=menu_data['place_name'],
                    items=menu_data['items'],
                    source=menu_data.get('source', 'google'),
                    last_updated=datetime.utcnow()
                )
                session.add(menu)
                message = "Menu created"
            
            session.commit()
            
            return {
                "status": "success",
                "message": message,
                "id": menu_id
            }
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_menu_by_place_id(self, place_id: str) -> Optional[Dict[str, Any]]:
        """Get menu by place ID"""
        session = self.SessionLocal()
        try:
            menu = session.query(Menu).filter(Menu.place_id == place_id).first()
            if menu:
                return {
                    "_id": menu.id,
                    "id": menu.id,
                    "place_id": menu.place_id,
                    "place_name": menu.place_name,
                    "items": menu.items,
                    "source": menu.source,
                    "last_updated": menu.last_updated.isoformat() if menu.last_updated else None
                }
            return None
        finally:
            session.close()
    
    # ========== DATABASE UTILITIES ==========
    
    def health_check(self) -> Dict[str, Any]:
        """Database health check"""
        session = self.SessionLocal()
        try:
            categories_count = session.query(Category).count()
            keywords_count = session.query(Keyword).count()
            rules_count = session.query(Rule).count()
            menus_count = session.query(Menu).count()
            
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
            session.close()

# Singleton instance
neon_db_service = NeonDatabaseService()