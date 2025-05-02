"""
Reset or create the admin user.
Run this script to ensure the admin user exists with ID 1.
Save this as reset_admin.py
"""
from user_management import check_admin_user_exists, create_admin_user

print("Checking for admin user...")
admin_exists = check_admin_user_exists()

if not admin_exists:
    print("Creating admin user...")
    admin_code = create_admin_user()
    if admin_code:
        print("===========================================")
        print(f"ADMIN USER CREATED/RESET")
        print(f"Admin code: {admin_code}")
        print("===========================================")
        print("Use this code to log in as administrator.")
    else:
        print("Failed to create admin user.")
else:
    print("Admin user already exists.")
    reset = input("Do you want to reset the admin user code? (y/n): ")
    if reset.lower() == 'y':
        admin_code = create_admin_user()
        if admin_code:
            print("===========================================")
            print(f"ADMIN USER RESET")
            print(f"New admin code: {admin_code}")
            print("===========================================")
            print("Use this code to log in as administrator.")
        else:
            print("Failed to reset admin user.")