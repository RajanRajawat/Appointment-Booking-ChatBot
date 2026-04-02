from langchain.tools import tool
from db.models import RegisterUser, ValidateUser, ScheduleAppointment, CancelAppointment, RescheduleAppointment
from db.db import users_collection, appointments_collection
from bson import ObjectId








#-~                                                  DB Tools   


#!                       User   
#- Register 
@tool
def register_user(name: str, mobile: str, date_of_birth: str) -> str:
    """
    Create a new user account.

    Args:
        name: Full name of the user.
        mobile: 10 digit mobile number.
        date_of_birth: DOB in DD-MM-YYYY format.
    """

    try:
        user = RegisterUser(
            name=name,
            mobile=mobile,
            date_of_birth=date_of_birth
        )

        existing_user = users_collection.find_one({"mobile": user.mobile})
        if existing_user:
            return "User already exists"

        users_collection.insert_one(user.model_dump())

        return "User added successfully"

    except Exception as e:
        return f"Error: {str(e)}"
    

#- Verify User  
@tool
def verify_user(mobile: str, date_of_birth: str) -> str:
    """
    Verify if a user exists using mobile number and date of birth.

    Args:
        mobile: 10 digit mobile number of the user.
        date_of_birth: DOB in DD-MM-YYYY format.
    """

    try:
        user = ValidateUser(
            mobile=mobile,
            date_of_birth=date_of_birth
        )

        existing_user = users_collection.find_one({
            "mobile": user.mobile,
            "date_of_birth": user.date_of_birth
        })

        if existing_user:
            return f"User verified successfully. User ID: {str(existing_user['_id'])}"
        else:
            return "User not found or details do not match"

    except Exception as e:
        return f"Error: {str(e)}"
    



#!                       Appointment    



#- Schedule Appointment 
@tool
def schedule_appointment(user_id: str, date_of_appointment: str, time_of_appointment: str) -> str:
    """
    Schedule an appointment for a user.

    Args:
        user_id: MongoDB user ID.
        date_of_appointment: Date in DD-MM-YYYY format.
        time_of_appointment: Time in HH:MMPM or HH:MMAM format.
    """

    try:
        data = ScheduleAppointment(
            user_id=user_id,
            date_of_appointment=date_of_appointment,
            time_of_appointment=time_of_appointment.upper()
        )


        user = users_collection.find_one({"_id": ObjectId(data.user_id)})
        if not user:
            return "User not found. Please register first."


        existing = appointments_collection.find_one({
            "user_id": ObjectId(data.user_id),
            "date_of_appointment": data.date_of_appointment,
            "time_of_appointment": data.time_of_appointment
        })

        if existing:
            return "Appointment already exists for this date and time."


        result = appointments_collection.insert_one({
            "user_id": ObjectId(data.user_id),
            "date_of_appointment": data.date_of_appointment,
            "time_of_appointment": data.time_of_appointment
        })

        return f"Appointment scheduled successfully. Appointment ID: {str(result.inserted_id)}"

    except Exception as e:
        return f"Error: {str(e)}"
    


#- Update appointment   
@tool
def reschedule_appointment(appointment_id: str, date_of_appointment: str, time_of_appointment: str) -> str:
    """
    Reschedule an existing appointment.

    Args:
        appointment_id: MongoDB appointment ID.
        date_of_appointment: New date in DD-MM-YYYY format.
        time_of_appointment: New time in HH:MMPM or HH:MMAM format.
    """

    try:
        
        data = RescheduleAppointment(
            appointment_id=appointment_id,
            date_of_appointment=date_of_appointment,
            time_of_appointment=time_of_appointment.upper()
        )


        existing = appointments_collection.find_one({
            "_id": ObjectId(data.appointment_id)
        })

        if not existing:
            return "Appointment not found"

        
        result = appointments_collection.update_one(
            {"_id": ObjectId(data.appointment_id)},
            {
                "$set": {
                    "date_of_appointment": data.date_of_appointment,
                    "time_of_appointment": data.time_of_appointment
                }
            }
        )

        if result.modified_count:
            return "Appointment rescheduled successfully"
        else:
            return "No changes made (same date/time provided)"

    except Exception as e:
        return f"Error: {str(e)}"
    



#- Cancel appointment   
@tool
def cancel_appointment(appointment_id: str) -> str:
    """
    Cancel an existing appointment.

    Args:
        appointment_id: MongoDB appointment ID.
    """

    try:
        
        data = CancelAppointment(
            appointment_id=appointment_id
        )

        
        result = appointments_collection.delete_one(
            {"_id": ObjectId(data.appointment_id)}
        )

        if result.deleted_count:
            return "Appointment cancelled successfully"
        else:
            return "Appointment not found"

    except Exception as e:
        return f"Error: {str(e)}"
    

#- Get Appointments  

@tool
def view_appointments(user_id: str) -> str:
    """
    View all appointments for a user.

    Args:
        user_id: MongoDB user ID.
    """

    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return "User not found."

        appointments = list(appointments_collection.find({"user_id": ObjectId(user_id)}))

        if not appointments:
            return "No appointments found for this user."

        result = []
        for appt in appointments:
            result.append(
                f"Appointment ID: {str(appt['_id'])} | "
                f"Date: {appt['date_of_appointment']} | "
                f"Time: {appt['time_of_appointment']}"
            )

        return "\n".join(result)

    except Exception as e:
        return f"Error: {str(e)}"