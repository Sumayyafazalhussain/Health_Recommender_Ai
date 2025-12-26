# app/services/postgres_service.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import settings
import logging
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class PostgreSQLService:
    """Direct PostgreSQL service using SQLAlchemy"""
    
    def __init__(self):
        self.engine = create_engine(
            settings.POSTGRES_URL,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600,
            echo=settings.DEBUG
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        logger.info("✅ PostgreSQLService initialized")
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    # ========== CATEGORY OPERATIONS ==========
    
    def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new category"""
        session = self.get_session()
        try:
            # Check if category already exists
            result = session.execute(
                text("SELECT id FROM categories WHERE name = :name"),
                {"name": category_data["name"]}
            )
            if result.fetchone():
                return {
                    "status": "error",
                    "message": f"Category '{category_data['name']}' already exists"
                }
            
            # Generate ID if not provided
            category_id = category_data.get("id", str(uuid.uuid4()))
            
            # Insert category
            session.execute(
                text("""
                    INSERT INTO categories (id, name, description, is_unhealthy)
                    VALUES (:id, :name, :description, :is_unhealthy)
                """),
                {
                    "id": category_id,
                    "name": category_data["name"],
                    "description": category_data.get("description"),
                    "is_unhealthy": category_data.get("is_unhealthy", True)
                }
            )
            session.commit()
            
            return {
                "status": "success",
                "message": "Category created",
                "id": category_id
            }
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating category: {e}")
            return {
                "status": "error",
                "message": f"Database error: {str(e)}"
            }
        finally:
            session.close()
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """Get all categories"""
        session = self.get_session()
        try:
            result = session.execute(
                text("SELECT id, name, description, is_unhealthy, created_at FROM categories ORDER BY name")
            )
            categories = []
            for row in result:
                categories.append({
                    "_id": row.id,
                    "id": row.id,
                    "name": row.name,
                    "description": row.description,
                    "is_unhealthy": row.is_unhealthy,
                    "created_at": row.created_at.isoformat() if row.created_at else None
                })
            return categories
        finally:
            session.close()
    
    def get_category_by_id(self, category_id: str) -> Optional[Dict[str, Any]]:
        """Get category by ID"""
        session = self.get_session()
        try:
            result = session.execute(
                text("SELECT id, name, description, is_unhealthy FROM categories WHERE id = :id"),
                {"id": category_id}
            )
            row = result.fetchone()
            if row:
                return {
                    "_id": row.id,
                    "id": row.id,
                    "name": row.name,
                    "description": row.description,
                    "is_unhealthy": row.is_unhealthy
                }
            return None
        finally:
            session.close()
    
    # ========== KEYWORD OPERATIONS ==========
    
    def create_keyword(self, keyword_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a keyword for category detection"""
        session = self.get_session()
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
            
            # Insert keyword
            session.execute(
                text("""
                    INSERT INTO keywords (id, keyword, category_id, match_type)
                    VALUES (:id, :keyword, :category_id, :match_type)
                """),
                {
                    "id": keyword_id,
                    "keyword": keyword_data["keyword"],
                    "category_id": keyword_data["category_id"],
                    "match_type": keyword_data.get("match_type", "partial")
                }
            )
            session.commit()
            
            return {
                "status": "success",
                "message": "Keyword added",
                "id": keyword_id
            }
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating keyword: {e}")
            return {
                "status": "error",
                "message": f"Database error: {str(e)}"
            }
        finally:
            session.close()
    
    def get_keywords(self) -> List[Dict[str, Any]]:
        """Get all keywords"""
        session = self.get_session()
        try:
            result = session.execute(
                text("""
                    SELECT k.id, k.keyword, k.category_id, k.match_type, k.created_at, c.name as category_name
                    FROM keywords k
                    LEFT JOIN categories c ON k.category_id = c.id
                    ORDER BY k.keyword
                """)
            )
            keywords = []
            for row in result:
                keywords.append({
                    "_id": row.id,
                    "id": row.id,
                    "keyword": row.keyword,
                    "category_id": row.category_id,
                    "category_name": row.category_name,
                    "match_type": row.match_type,
                    "created_at": row.created_at.isoformat() if row.created_at else None
                })
            return keywords
        finally:
            session.close()
    
    # ========== RULE OPERATIONS ==========
    
    def create_rule(self, rule_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a recommendation rule"""
        session = self.get_session()
        try:
            # Validate trigger category exists
            trigger_cat = self.get_category_by_id(rule_data['trigger_category_id'])
            if not trigger_cat:
                return {
                    "status": "error",
                    "message": f"Trigger category '{rule_data['trigger_category_id']}' not found"
                }
            
            # Validate recommended categories exist
            for cat_id in rule_data.get('recommended_category_ids', []):
                rec_cat = self.get_category_by_id(cat_id)
                if not rec_cat:
                    return {
                        "status": "error",
                        "message": f"Recommended category '{cat_id}' not found"
                    }
            
            # Check if rule exists
            result = session.execute(
                text("SELECT id FROM rules WHERE trigger_category_id = :trigger_category_id"),
                {"trigger_category_id": rule_data['trigger_category_id']}
            )
            if result.fetchone():
                return {
                    "status": "error",
                    "message": f"Rule for '{rule_data['trigger_category_id']}' already exists"
                }
            
            # Create rule
            rule_id = str(uuid.uuid4())
            
            session.execute(
                text("""
                    INSERT INTO rules (id, trigger_category_id, ai_prompt_template)
                    VALUES (:id, :trigger_category_id, :ai_prompt_template)
                """),
                {
                    "id": rule_id,
                    "trigger_category_id": rule_data['trigger_category_id'],
                    "ai_prompt_template": rule_data.get(
                        'ai_prompt_template',
                        "User is near a {trigger_category}. Suggest healthy alternatives like {alternatives}."
                    )
                }
            )
            
            # Add recommended categories to rule_categories table
            for cat_id in rule_data.get('recommended_category_ids', []):
                session.execute(
                    text("""
                        INSERT INTO rule_categories (rule_id, category_id)
                        VALUES (:rule_id, :category_id)
                    """),
                    {"rule_id": rule_id, "category_id": cat_id}
                )
            
            session.commit()
            
            return {
                "status": "success",
                "message": "Rule created",
                "id": rule_id
            }
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating rule: {e}")
            return {
                "status": "error",
                "message": f"Database error: {str(e)}"
            }
        finally:
            session.close()
    
    def get_rules(self) -> List[Dict[str, Any]]:
        """Get all rules with details"""
        session = self.get_session()
        try:
            # Get rules with trigger category name
            result = session.execute(
                text("""
                    SELECT r.id, r.trigger_category_id, r.ai_prompt_template, 
                           r.created_at, r.updated_at, c.name as trigger_category_name
                    FROM rules r
                    LEFT JOIN categories c ON r.trigger_category_id = c.id
                    ORDER BY r.created_at
                """)
            )
            
            rules = []
            for row in result:
                rule_data = {
                    "_id": row.id,
                    "id": row.id,
                    "trigger_category_id": row.trigger_category_id,
                    "trigger_category_name": row.trigger_category_name,
                    "ai_prompt_template": row.ai_prompt_template,
                    "created_at": row.created_at.isoformat() if row.created_at else None,
                    "updated_at": row.updated_at.isoformat() if row.updated_at else None
                }
                
                # Get recommended categories for this rule
                rec_result = session.execute(
                    text("""
                        SELECT rc.category_id, c.name as category_name
                        FROM rule_categories rc
                        LEFT JOIN categories c ON rc.category_id = c.id
                        WHERE rc.rule_id = :rule_id
                    """),
                    {"rule_id": row.id}
                )
                
                recommended_ids = []
                recommended_names = []
                for rec_row in rec_result:
                    recommended_ids.append(rec_row.category_id)
                    recommended_names.append(rec_row.category_name)
                
                rule_data["recommended_category_ids"] = recommended_ids
                rule_data["recommended_category_names"] = recommended_names
                
                rules.append(rule_data)
            
            return rules
            
        finally:
            session.close()
    
    # ========== DATABASE UTILITIES ==========
    
    def reset_database(self) -> Dict[str, Any]:
        """Reset database (for testing)"""
        session = self.get_session()
        try:
            # Delete in correct order (due to foreign keys)
            session.execute(text("DELETE FROM rule_categories"))
            session.execute(text("DELETE FROM keywords"))
            session.execute(text("DELETE FROM rules"))
            session.execute(text("DELETE FROM categories"))
            session.execute(text("DELETE FROM menus"))
            session.commit()
            
            return {
                "status": "success",
                "message": "Database reset"
            }
        except Exception as e:
            session.rollback()
            return {
                "status": "error",
                "message": f"Reset failed: {str(e)}"
            }
        finally:
            session.close()
    
    def health_check(self) -> Dict[str, Any]:
        """Database health check"""
        session = self.get_session()
        try:
            # Test connection
            session.execute(text("SELECT 1"))
            
            # Get counts
            categories_count = session.execute(text("SELECT COUNT(*) FROM categories")).scalar() or 0
            keywords_count = session.execute(text("SELECT COUNT(*) FROM keywords")).scalar() or 0
            rules_count = session.execute(text("SELECT COUNT(*) FROM rules")).scalar() or 0
            menus_count = session.execute(text("SELECT COUNT(*) FROM menus")).scalar() or 0
            
            return {
                "status": "healthy",
                "database": {
                    "categories": categories_count,
                    "keywords": keywords_count,
                    "rules": rules_count,
                    "menus": menus_count
                }
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": str(e)
            }
        finally:
            session.close()
    
    def test_connection(self) -> bool:
        """Test if can connect to database"""
        try:
            session = self.get_session()
            result = session.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            session.close()
            logger.info(f"✅ PostgreSQL connected: {version}")
            return True
        except Exception as e:
            logger.error(f"❌ PostgreSQL connection failed: {e}")
            return False

# Singleton instance
postgres_service = PostgreSQLService()