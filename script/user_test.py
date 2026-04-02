from db.db import users_collection, appointments_collection
from db.models import RegisterUser, ValidateUser



def register_user():
    print("\n--- Register User ---")
    
    name = input("Enter name: ")
    mobile = input("Enter mobile: ")
    dob_input = input("Enter DOB (DD-MM-YYYY): ")

    try:
        user = RegisterUser(
            name=name,
            mobile=mobile,
            date_of_birth=dob_input
        )

        # Check if user already exists
        existing_user = users_collection.find_one({"mobile": user.mobile})
        if existing_user:
            print("User already exists")
            return

        # Insert into DB
        users_collection.insert_one(user.model_dump())

        print("✅ User added successfully")

    except Exception as e:
        print(f"❌ Error: {e}")


def validate_user():
    print("\n--- Validate User ---")

    mobile = input("Enter mobile: ")
    dob_input = input("Enter DOB (DD-MM-YYYY): ")

    try:
        user = ValidateUser(
            mobile=mobile,
            date_of_birth=dob_input
        )

        # Find user
        existing_user = users_collection.find_one({
            "mobile": user.mobile,
            "dob": user.date_of_birth
        })

        if existing_user:
            print("✅ User validated")
        else:
            print("❌ User not found / cannot be validated")

    except Exception as e:
        print(f"❌ Error: {e}")


# ---------------- MAIN ---------------- #

def main():
    print("Choose option:")
    print("1 → Register")
    print("2 → Login")

    choice = input("Enter choice (1/2): ")

    if choice == "1":
        register_user()
    elif choice == "2":
        validate_user()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()