from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    
    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total: float

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    shipping_address: str
    notes: Optional[str] = None

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    total_amount: float
    shipping_address: str
    items: List[OrderItemResponse]
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrderUpdateStatus(BaseModel):
    status: str
