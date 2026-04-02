from db.db import users_collection, appointments_collection
from db.models import (
    ScheduleAppointment,
    RescheduleAppointment,
    CancelAppointment
)
from bson import ObjectId
from datetime import datetime


# ---------------- HELPERS ---------------- #

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except:
        return False


def validate_time(time_str):
    try:
        datetime.strptime(time_str, "%I:%M%p")  # 12-hour format with AM/PM
        return True
    except:
        return False


# ---------------- SCHEDULE ---------------- #

def schedule_appointment():
    print("\n--- Schedule Appointment ---")

    user_id = input("Enter user_id: ")
    date = input("Enter date (DD-MM-YYYY): ")
    time = input("Enter time (HH:MMPM or HH:MMAM): ")

    if not validate_date(date):
        print("❌ Invalid date format. Use DD-MM-YYYY")
        return

    if not validate_time(time):
        print("❌ Invalid time format. Use HH:MMPM or HH:MMAM (e.g., 02:30PM)")
        return

    try:
        data = ScheduleAppointment(
            user_id=user_id,
            date_of_appointment=date,
            time_of_appointment=time.upper()
        )

        # Check if user exists
        user = users_collection.find_one({"_id": ObjectId(data.user_id)})
        if not user:
            print("❌ User not found")
            return

        result = appointments_collection.insert_one({
            "user_id": ObjectId(data.user_id),
            "date_of_appointment": data.date_of_appointment,
            "time_of_appointment": data.time_of_appointment
        })

        print("✅ Appointment scheduled")
        print("Appointment ID:", result.inserted_id)

    except Exception as e:
        print(f"❌ Error: {e}")


# ---------------- RESCHEDULE ---------------- #

def reschedule_appointment():
    print("\n--- Reschedule Appointment ---")

    appointment_id = input("Enter appointment_id: ")
    date = input("Enter new date (DD-MM-YYYY): ")
    time = input("Enter new time (HH:MMPM or HH:MMAM): ")

    if not validate_date(date):
        print("❌ Invalid date format")
        return

    if not validate_time(time):
        print("❌ Invalid time format")
        return

    try:
        data = RescheduleAppointment(
            appointment_id=appointment_id,
            date_of_appointment=date,
            time_of_appointment=time.upper()
        )

        result = appointments_collection.update_one(
            {"_id": ObjectId(data.appointment_id)},
            {
                "$set": {
                    "date_of_appointment": data.date_of_appointment,
                    "time_of_appointment": data.time_of_appointment
                }
            }
        )

        if result.matched_count:
            print("✅ Appointment rescheduled")
        else:
            print("❌ Appointment not found")

    except Exception as e:
        print(f"❌ Error: {e}")


# ---------------- CANCEL ---------------- #

def cancel_appointment():
    print("\n--- Cancel Appointment ---")

    appointment_id = input("Enter appointment_id: ")

    try:
        data = CancelAppointment(
            appointment_id=appointment_id
        )

        result = appointments_collection.delete_one(
            {"_id": ObjectId(data.appointment_id)}
        )

        if result.deleted_count:
            print("✅ Appointment cancelled")
        else:
            print("❌ Appointment not found")

    except Exception as e:
        print(f"❌ Error: {e}")


# ---------------- MAIN ---------------- #

def main():
    print("\nChoose option:")
    print("1 → Schedule Appointment")
    print("2 → Reschedule Appointment")
    print("3 → Cancel Appointment")

    choice = input("Enter choice (1/2/3): ")

    if choice == "1":
        schedule_appointment()
    elif choice == "2":
        reschedule_appointment()
    elif choice == "3":
        cancel_appointment()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()