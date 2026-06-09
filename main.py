from itertools import product
from fastapi import Depends,FastAPI
from models import Product
from database import session,engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "welcome"

products = [
    Product(id=1,name="phone", description="budget phone",price = 699.99, quantity=10),
    Product(id=2,name="laptop", description="movie",price = 699.91, quantity=11),
    Product(id=3,name="phone", description="budget phone",price = 699.92, quantity=20),
    Product(id=6,name="charger", description="charge",price = 699.93, quantity=30),
    ]
   
def get_db(): 
    db = session()
    try:
      yield db

    finally:
    
         db.close()

   
def init_db():
   db = session()

   count = db.query(database_models.Product).count();
   
   if count == 0:
     for product in products():
         db.add(database_models.Product(**product.model_dump))
         db.commit()

init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
   
   db_products = db.query(database_models.Product).all()

   return db_products

@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
   
   db_product = db.query(database_models.Product).filter(database_models.id == id).first()
   if product.id == id:
          return db_product
   
          return "product not found"

@app.post("/product")
def add_product(product:Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product 

@app.put("/product")
def update_product(id:int, product: Product):
      
      db_product = db.query(database_models.Product).filter(database_models.id == id).first()
      if db_product:
          db_product:name = product.name
          db.product.description = product.description
          db.product.price = product.price
          db.product.quantity = product.quantity
          db.commit()

          return "Product updated successfully"
      else:
          return "no product found"


@app.delete("/product")
def delete_product(id: int, db: Session = Depends(get_db)):

    db_product = db.query(database_models.Product).filter(database_models.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    else:  
        return "no product found"

           
    