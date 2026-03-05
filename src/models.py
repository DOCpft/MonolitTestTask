from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Region(Base):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    prices = relationship('Price', back_populates='region')

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    products = relationship('Product', back_populates='category')

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    category = relationship('Category', back_populates='products')
    prices = relationship('Price', back_populates='product', cascade='all, delete-orphan')

class Price(Base):
    __tablename__ = 'prices'
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    region_id = Column(Integer, ForeignKey('regions.id'), primary_key=True)
    price = Column(Float, nullable=False)

    product = relationship('Product', back_populates='prices')
    region = relationship('Region', back_populates='prices')