# # app/db/neon_connection.py
# from sqlalchemy import create_engine, Column, String, Boolean, Text, DateTime, ForeignKey, Table
# from sqlalchemy.orm import declarative_base, relationship, sessionmaker
# from sqlalchemy.dialects.postgresql import JSONB
# from datetime import datetime
# from app.config import settings

# Base = declarative_base()

# # Association table
# rule_categories = Table(
#     'rule_categories',
#     Base.metadata,
#     Column('rule_id', String, ForeignKey('rules.id')),
#     Column('category_id', String, ForeignKey('categories.id'))
# )

# class Category(Base):
#     __tablename__ = "categories"
    
#     id = Column(String, primary_key=True, index=True)
#     name = Column(String(255), nullable=False)
#     description = Column(Text, nullable=True)
#     is_unhealthy = Column(Boolean, default=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     keywords = relationship("Keyword", back_populates="category")

# class Keyword(Base):
#     __tablename__ = "keywords"
    
#     id = Column(String, primary_key=True, index=True)
#     keyword = Column(String(255), nullable=False, index=True)
#     category_id = Column(String, ForeignKey("categories.id"), nullable=False)
#     match_type = Column(String(50), default="partial")
#     created_at = Column(DateTime, default=datetime.utcnow)
    
#     category = relationship("Category", back_populates="keywords")

# class Rule(Base):
#     __tablename__ = "rules"
    
#     id = Column(String, primary_key=True, index=True)
#     trigger_category_id = Column(String, ForeignKey("categories.id"), nullable=False)
#     ai_prompt_template = Column(Text, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     recommended_categories = relationship("Category", secondary=rule_categories)
#     trigger_category = relationship("Category", foreign_keys=[trigger_category_id])

# class Menu(Base):
#     __tablename__ = "menus"
    
#     id = Column(String, primary_key=True, index=True)
#     place_id = Column(String(255), nullable=False, index=True)
#     place_name = Column(String(255), nullable=False)
#     source = Column(String(100), default="google")
#     items = Column(JSONB, nullable=False, default=[])
#     last_updated = Column(DateTime, default=datetime.utcnow)
#     created_at = Column(DateTime, default=datetime.utcnow)

# # ========== NEON DATABASE CONNECTION ==========
# def get_engine():
#     """Create SQLAlchemy engine for Neon PostgreSQL"""
#     if not settings.DATABASE_URL:
#         raise ValueError("DATABASE_URL must be set for Neon PostgreSQL")
    
#     print(f"🔗 Connecting to Neon PostgreSQL...")
    
#     engine = create_engine(
#         settings.DATABASE_URL,
#         echo=False,
#         pool_pre_ping=True,
#         pool_size=5,
#         max_overflow=10,
#         pool_recycle=300
#     )
#     return engine

# # Create session factory
# engine = get_engine()
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_db():
#     """Dependency to get database session"""
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def test_connection():
#     """Test Neon connection - ADD THIS FUNCTION"""
#     try:
#         db = SessionLocal()
#         result = db.execute("SELECT version();")
#         version = result.fetchone()[0]
#         print(f"✅ Neon PostgreSQL: {version}")
        
#         # Check tables
#         result = db.execute("""
#             SELECT table_name 
#             FROM information_schema.tables 
#             WHERE table_schema = 'public'
#             ORDER BY table_name;
#         """)
#         tables = [row[0] for row in result]
        
#         if tables:
#             print(f"✅ Found {len(tables)} tables")
#         else:
#             print("⚠️ No tables found")
        
#         db.close()
#         return True
#     except Exception as e:
#         print(f"❌ Neon connection failed: {e}")
#         return False# app/db/neon_connection.py
from sqlalchemy import create_engine, Column, String, Boolean, Text, DateTime, ForeignKey, Table, text  # ADD text import
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.config import settings

Base = declarative_base()

# Association table
rule_categories = Table(
    'rule_categories',
    Base.metadata,
    Column('rule_id', String, ForeignKey('rules.id')),
    Column('category_id', String, ForeignKey('categories.id'))
)

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_unhealthy = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    keywords = relationship("Keyword", back_populates="category")

class Keyword(Base):
    __tablename__ = "keywords"
    
    id = Column(String, primary_key=True, index=True)
    keyword = Column(String(255), nullable=False, index=True)
    category_id = Column(String, ForeignKey("categories.id"), nullable=False)
    match_type = Column(String(50), default="partial")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    category = relationship("Category", back_populates="keywords")

class Rule(Base):
    __tablename__ = "rules"
    
    id = Column(String, primary_key=True, index=True)
    trigger_category_id = Column(String, ForeignKey("categories.id"), nullable=False)
    ai_prompt_template = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    recommended_categories = relationship("Category", secondary=rule_categories)
    trigger_category = relationship("Category", foreign_keys=[trigger_category_id])

class Menu(Base):
    __tablename__ = "menus"
    
    id = Column(String, primary_key=True, index=True)
    place_id = Column(String(255), nullable=False, index=True)
    place_name = Column(String(255), nullable=False)
    source = Column(String(100), default="google")
    items = Column(JSONB, nullable=False, default=[])
    last_updated = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

# ========== NEON DATABASE CONNECTION ==========
def get_engine():
    """Create SQLAlchemy engine for Neon PostgreSQL"""
    if not settings.DATABASE_URL:
        raise ValueError("DATABASE_URL must be set for Neon PostgreSQL")
    
    print(f"🔗 Connecting to Neon PostgreSQL...")
    
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_recycle=300
    )
    return engine

# Create session factory
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """Test Neon connection - FIXED with text()"""
    try:
        db = SessionLocal()
        # FIX: Use text() for SQL expressions
        result = db.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"✅ Neon PostgreSQL: {version}")
        
        # Check tables
        result = db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """))
        tables = [row[0] for row in result]
        
        if tables:
            print(f"✅ Found {len(tables)} tables")
        else:
            print("⚠️ No tables found")
        
        db.close()
        return True
    except Exception as e:
        print(f"❌ Neon connection failed: {e}")
        return False