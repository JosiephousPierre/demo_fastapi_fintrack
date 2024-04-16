# model/consulted_medication.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db


ConsultedMedicationRouter = APIRouter(tags=["Consulted Medication"])

# CRUD operations

@ConsultedMedicationRouter.get("/consulted_medication/", response_model=list)
async def read_consulted_medications(
    db=Depends(get_db)
):
    query = "SELECT prescription_Id, Consultation_Id, medicine_ID, quantity FROM consulted_med"
    db[0].execute(query)
    consulted_medications = [{
            "prescription_Id": row[0],
            "Consultation_Id": row[1],
            "medicine_ID": row[2],
            "quantity": row[3]
        } 
            for row in db[0].fetchall()]
    return consulted_medications

@ConsultedMedicationRouter.get("/consulted_medication/{prescription_Id}", response_model=dict)
async def read_consulted_medication(
    prescription_Id: int, 
    db=Depends(get_db)
):
    query = "SELECT prescription_Id, Consultation_Id, medicine_ID, quantity FROM consulted_med WHERE prescription_Id = %s"
    db[0].execute(query, (prescription_Id,))
    consulted_medication = db[0].fetchone()
    if consulted_medication:
        return {
            "prescription_Id": consulted_medication[0],
            "Consultation_Id": consulted_medication[1],
            "medicine_ID": consulted_medication[2],
            "quantity": consulted_medication[3]
        }
    raise HTTPException(status_code=404, detail="Consulted Medication not found")

@ConsultedMedicationRouter.post("/consulted_medication/", response_model=dict)
async def create_consulted_medication(
    Consultation_Id: int = Form(...),
    medicine_ID: int = Form(...),
    quantity: int = Form(...),
    db=Depends(get_db)
):

    query = "INSERT INTO consulted_med (Consultation_Id, medicine_ID, quantity) VALUES (%s, %s, %s)"
    db[0].execute(query, (Consultation_Id, medicine_ID, quantity))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_prescription_Id = db[0].fetchone()[0]
    db[1].commit()

    return {
    "prescription_Id": new_prescription_Id,
    "Consultation_Id": Consultation_Id,
    "medicine_ID": medicine_ID,
    "quantity": quantity
}

@ConsultedMedicationRouter.put("/consulted_medication/{prescription_Id}", response_model=dict)
async def update_consulted_medication(
    prescription_Id: int,
    Consultation_Id: int = Form(...),
    medicine_ID: int = Form(...),
    quantity: int = Form(...),
    db=Depends(get_db)
):

    # Update consulted medication information in the database 
    query = "UPDATE consulted_med SET Consultation_Id = %s, medicine_ID = %s, quantity = %s WHERE prescription_Id = %s"
    db[0].execute(query, (Consultation_Id, medicine_ID, quantity, prescription_Id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Consulted Medication updated successfully"}
    
    # If no rows were affected, consulted medication not found
    raise HTTPException(status_code=404, detail="Consulted Medication not found")

@ConsultedMedicationRouter.delete("/consulted_medication/{prescription_Id}", response_model=dict)
async def delete_consulted_medication(
    prescription_Id: int,
    db=Depends(get_db)
):
    try:
        # Check if the consulted medication exists
        query_check_consulted_medication = "SELECT prescription_Id FROM consulted_med WHERE prescription_Id = %s"
        db[0].execute(query_check_consulted_medication, (prescription_Id,))
        existing_consulted_medication = db[0].fetchone()

        if not existing_consulted_medication:
            raise HTTPException(status_code=404, detail="Consulted Medication not found")

        # Delete the consulted medication
        query_delete_consulted_medication = "DELETE FROM consulted_med WHERE prescription_Id = %s"
        db[0].execute(query_delete_consulted_medication, (prescription_Id,))
        db[1].commit()

        return {"message": "Consulted Medication deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
