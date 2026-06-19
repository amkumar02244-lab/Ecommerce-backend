from app.core.database import Base, engine
from app.repositories.user_repository import user_repository
from app.core.security import hash_password

def generate_default_users():
    # Ensure tables are created
    Base.metadata.create_all(bind=engine)
    
    # 1. Create Admin User
    admin_email = "admin@riyasboutique.com"
    if not user_repository.sku_exists(admin_email) if hasattr(user_repository, 'sku_exists') else not user_repository.email_exists(admin_email):
        admin_data = {
            "first_name": "Admin",
            "last_name": "User",
            "email": admin_email,
            "password": hash_password("Admin@123!"),
            "role": "admin",
            "is_active": True,
            "is_verified": True,
            "phone": "1234567890"
        }
        user_repository.create(admin_data)
        print(f"Created Admin: {admin_email} | Password: Admin@123!")
    else:
        print(f"Admin {admin_email} already exists.")

    # 2. Create Regular Customer
    customer_email = "customer@example.com"
    if not user_repository.email_exists(customer_email):
        customer_data = {
            "first_name": "Demo",
            "last_name": "Customer",
            "email": customer_email,
            "password": hash_password("Customer@123!"),
            "role": "customer",
            "is_active": True,
            "is_verified": True,
            "phone": "0987654321"
        }
        user_repository.create(customer_data)
        print(f"Created Customer: {customer_email} | Password: Customer@123!")
    else:
        print(f"Customer {customer_email} already exists.")

if __name__ == "__main__":
    generate_default_users()
