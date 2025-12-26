# app/db/neon_connection.py
from sqlalchemy import create_engine, Column, String, Boolean, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.config import settings

Base = declarative_base()

# Association table for many-to-many relationships
rule_categories = Table(
    'rule_categories',
    Base.metadata,
    Column('rule_id', String, ForeignKey('rules.id')),
    Column('category_id', String, ForeignKey('categories.id'))
)

class Category(Base):
    """Category model for Neon PostgreSQL"""
    __tablename__ = "categories"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_unhealthy = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    keywords = relationship("Keyword", back_populates="category", cascade="all, delete-orphan")
    triggered_rules = relationship("Rule", back_populates="trigger_category", 
                                   foreign_keys="[Rule.trigger_category_id]")

class Keyword(Base):
    """Keyword model for Neon PostgreSQL"""
    __tablename__ = "keywords"
    
    id = Column(String, primary_key=True, index=True)
    keyword = Column(String(255), nullable=False, index=True)
    category_id = Column(String, ForeignKey("categories.id"), nullable=False)
    match_type = Column(String(50), default="partial")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", back_populates="keywords")

class Rule(Base):
    """Rule model for Neon PostgreSQL"""
    __tablename__ = "rules"
    
    id = Column(String, primary_key=True, index=True)
    trigger_category_id = Column(String, ForeignKey("categories.id"), nullable=False)
    ai_prompt_template = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    recommended_categories = relationship("Category", secondary=rule_categories)
    trigger_category = relationship("Category", back_populates="triggered_rules", 
                                    foreign_keys=[trigger_category_id])

class Menu(Base):
    """Menu model for Neon PostgreSQL"""
    __tablename__ = "menus"
    
    id = Column(String, primary_key=True, index=True)
    place_id = Column(String(255), nullable=False, index=True)
    place_name = Column(String(255), nullable=False)
    source = Column(String(100), default="google")
    items = Column(JSONB, nullable=False, default=[])  # JSONB for PostgreSQL/Neon
    last_updated = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database connection for Neon
def get_neon_engine():
    """Create SQLAlchemy engine for Neon PostgreSQL"""
    database_url = settings.DATABASE_URL
    
    if not database_url:
        raise ValueError("DATABASE_URL must be set for Neon PostgreSQL")
    
    print(f"🔗 Connecting to Neon PostgreSQL...")
    
    # Create engine with connection pooling
    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_recycle=300,
        pool_timeout=30,
        connect_args={
            'connect_timeout': 10,
            'application_name': 'health-recommender-api'
        }
    )
    return engine

def get_session_local():
    """Create session factory"""
    engine = get_neon_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

def init_db():
    """Initialize database tables in Neon (idempotent)"""
    try:
        engine = get_neon_engine()
        Base.metadata.create_all(bind=engine)
        print("✅ Neon PostgreSQL tables initialized")
    except Exception as e:
        print(f"⚠️ Note: {e}")

def check_connection():
    """Test Neon connection"""
    try:
        SessionLocal = get_session_local()
        session = SessionLocal()
        session.execute("SELECT 1")
        session.close()
        print("✅ Neon PostgreSQL connection successful")
        return True
    except Exception as e:
        print(f"❌ Neon PostgreSQL connection failed: {e}")
        return False