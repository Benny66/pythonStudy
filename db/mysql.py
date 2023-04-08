from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base # 导入映射声明函数


engine = create_engine("mysql+pymysql://root:root123456@127.0.0.1:33060/menu",echo=True) # 实例化数据库连接
Base = declarative_base()   # 实例化ORM的基类
DbSession = sessionmaker(bind=engine)
session = DbSession()
    

class MenuDB(Base):
    __tablename__ = 'm_menu'  # 表名
    __table_args__ = {'sqlite_autoincrement': True}

    # 表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, nullable=False)  
    name = Column(String(255), nullable=False)  
    video = Column(String(255), nullable=False)  
    image = Column(String(255), nullable=False)  
    tags = Column(String(255), nullable=False)  
    m_materials = Column(String(255), nullable=False)  
    a_materials = Column(String(255), nullable=False)  
    make_time = Column(Integer, default=0)
    step = Column(String, nullable=False) 
    view_volume = Column(Integer, default=0)
    collection_volume = Column(Integer, default=0)
    created_at = Column(String, default="1970-01-01 00:00:00")
    updated_at = Column(String, default="1970-01-01 00:00:00")

class CategoryDB(Base):
    __tablename__ = 'm_category'  # 表名
    __table_args__ = {'sqlite_autoincrement': True}

    # 表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)  
    created_at = Column(String, default="1970-01-01 00:00:00")
    updated_at = Column(String, default="1970-01-01 00:00:00")
