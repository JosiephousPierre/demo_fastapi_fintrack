# model/consult.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db

ConsultRouter = APIRouter(tags=["Consult"])

# CRUD operations

@ConsultRouter.get("/consult/", response_model=list)
async def read_consult(
    db=Depends(get_db)
):
    query = "SELECT Consultation_Id, student_Id, nurseID, illness, medicine, date, time_In, check_Out FROM consult"
    db[0].execute(query)
    consult = [{
        "Consultation_Id": c[0],
        "student_Id": c[1],
        "nurseID": c[2],
        "illness": c[3],
        "medicine": c[4],
        "date": c[5],
        "time_In": c[6],
        "check_Out": c[7],
    } for c in db[0].fetchall()]
    return consult

@ConsultRouter.get("/consult/{consult_id}", response_model=dict)
async def read_manage(
    consult_id: int, 
    db=Depends(get_db)
):
    query = "SELECT Consultation_Id, student_Id, nurseID, illness, medicine, date, time_In, check_Out FROM consult WHERE Consultation_Id = %s"
    db[0].execute(query, (consult_id,))
    consult = db[0].fetchone()
    if consult:
        return {
            "Consultation_Id": consult[0],
            "student_Id": consult[1],
            "nurseID": consult[2],
            "illness": consult[3],
            "medicine": consult[4],
            "date": consult[5],
            "time_In": consult[6],
            "check_Out": consult[7],
        }
    raise HTTPException(status_code=404, detail="Consultation not found")

@ConsultRouter.post("/consult/", response_model=dict)
async def create_consult(
    student_Id: int = Form(...), 
    nurseID: int = Form(...), 
    illness: str = Form(...), 
    medicine: str = Form(...),
    date: str = Form(...),
    time_In: str = Form(...),
    check_Out: str = Form(...), 
    db=Depends(get_db)
):

    query = "INSERT INTO consult (student_Id, nurseID, illness, medicine, date, time_In, check_Out) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    db[0].execute(query, (student_Id, nurseID, illness, medicine, date, time_In, check_Out))
    db[1].commit()

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_consult_id = db[0].fetchone()[0]

    return  {
        "Consultation_Id": new_consult_id,
        "student_Id": student_Id,
        "nurseID": nurseID,
        "illness": illness,
        "medicine": medicine,
        "date": date,
        "time_In": time_In,
        "check_Out": check_Out,
    }

@ConsultRouter.put("/consult/{consult_id}", response_model=dict)
async def update_consult(
    consult_id: int,
    student_Id: int = Form(...), 
    nurseID: int = Form(...), 
    illness: str = Form(...), 
    medicine: str = Form(...), 
    date: str = Form(...),
    time_In: str = Form(...),
    check_Out: str = Form(...),  
    db=Depends(get_db)
):

    # Update consultation information in the database 
    query = "UPDATE consult SET student_Id = %s, nurseID = %s, illness = %s, medicine = %s, date = %s, time_In = %s, check_Out = %s WHERE Consultation_Id = %s"
    db[0].execute(query, (student_Id, nurseID, illness, medicine, date, time_In, check_Out, consult_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Consultation updated successfully"}
    
    # If no rows were affected, consultation not found
    raise HTTPException(status_code=404, detail="Consultation not found")

@ConsultRouter.delete("/consult/{consult_id}", response_model=dict)
async def delete_consult(
    consult_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the consultation exists
        query_check_consultation = "SELECT Consultation_Id FROM consult WHERE Consultation_Id = %s"
        db[0].execute(query_check_consultation, (consult_id,))
        existing_consultation = db[0].fetchone()

        if not existing_consultation:
            raise HTTPException(status_code=404, detail="Consultation not found")

        # Delete the consultation
        query_delete_consultation = "DELETE FROM consult WHERE Consultation_Id = %s"
        db[0].execute(query_delete_consultation, (consult_id,))
        db[1].commit()

        return {"message": "Consultation deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()