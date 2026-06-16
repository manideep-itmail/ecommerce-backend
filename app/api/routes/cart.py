from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.product import Product
from app.models.order import CartItem
from app.schemas.order import CartItemCreate, CartItemUpdate, CartResponse, CartItemResponse

router = APIRouter()

@router.get("", response_model=CartResponse)
async def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    
    total = 0
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            total += product.price * item.quantity
    
    return {
        "items": cart_items,
        "total": total
    }

@router.post("/items", response_model=CartItemResponse)
async def add_to_cart(
    cart_item: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if product exists
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check if item already in cart
    existing_item = db.query(CartItem).filter(
        (CartItem.user_id == current_user.id) & 
        (CartItem.product_id == cart_item.product_id)
    ).first()
    
    if existing_item:
        existing_item.quantity += cart_item.quantity
        db.add(existing_item)
    else:
        new_item = CartItem(
            user_id=current_user.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )
        db.add(new_item)
    
    db.commit()
    db.refresh(new_item if not existing_item else existing_item)
    
    return new_item if not existing_item else existing_item

@router.put("/items/{item_id}", response_model=CartItemResponse)
async def update_cart_item(
    item_id: int,
    cart_item_data: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart_item = db.query(CartItem).filter(
        (CartItem.id == item_id) & (CartItem.user_id == current_user.id)
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    cart_item.quantity = cart_item_data.quantity
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    
    return cart_item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart_item = db.query(CartItem).filter(
        (CartItem.id == item_id) & (CartItem.user_id == current_user.id)
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    db.delete(cart_item)
    db.commit()

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
