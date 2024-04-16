# model/consulted_illness.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db


ConsultedIllnessRouter = APIRouter(tags=["Consulted Illness"])

# CRUD operations

@ConsultedIllnessRouter.get("/consulted_illness/", response_model=list)
async def read_consulted_illnesses(
    db=Depends(get_db)
):
    query = "SELECT consIllness_Id, illness_Id, Consultation_Id FROM consulted_illness"
    db[0].execute(query)
    consulted_illnesses = [{
            "consIllness_Id": row[0],
            "illness_Id": row[1],
            "Consultation_Id": row[2]
        } 
            for row in db[0].fetchall()]
    return consulted_illnesses

@ConsultedIllnessRouter.get("/consulted_illness/{consIllness_Id}", response_model=dict)
async def read_consulted_illness(
    consIllness_Id: int, 
    db=Depends(get_db)
):
    query = "SELECT consIllness_Id, illness_Id, Consultation_Id FROM consulted_illness WHERE consIllness_Id = %s"
    db[0].execute(query, (consIllness_Id,))
    consulted_illness = db[0].fetchone()
    if consulted_illness:
        return {
            "consIllness_Id": consulted_illness[0],
            "illness_Id": consulted_illness[1],
            "Consultation_Id": consulted_illness[2]
        }
    raise HTTPException(status_code=404, detail="Consulted Illness not found")

@ConsultedIllnessRouter.post("/consulted_illness/", response_model=dict)
async def create_consulted_illness(
    illness_Id: int = Form(...),
    Consultation_Id: int = Form(...), 
    db=Depends(get_db)
):

    query = "INSERT INTO consulted_illness (illness_Id, Consultation_Id) VALUES (%s, %s)"
    db[0].execute(query, (illness_Id, Consultation_Id))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_consIllness_Id = db[0].fetchone()[0]
    db[1].commit()

    return {
    "consIllness_Id": new_consIllness_Id,
    "illness_Id": illness_Id,
    "Consultation_Id": Consultation_Id
}

@ConsultedIllnessRouter.put("/consulted_illness/{consIllness_Id}", response_model=dict)
async def update_consulted_illness(
    consIllness_Id: int,
    illness_Id: int = Form(...),
    Consultation_Id: int = Form(...),
    db=Depends(get_db)
):

    # Update consulted illness information in the database 
    query = "UPDATE consulted_illness SET illness_Id = %s, Consultation_Id = %s WHERE consIllness_Id = %s"
    db[0].execute(query, (illness_Id, Consultation_Id, consIllness_Id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Consulted Illness updated successfully"}
    
    # If no rows were affected, consulted illness not found
    raise HTTPException(status_code=404, detail="Consulted Illness not found")

@ConsultedIllnessRouter.delete("/consulted_illness/{consIllness_Id}", response_model=dict)
async def delete_consulted_illness(
    consIllness_Id: int,
    db=Depends(get_db)
):
    try:
        # Check if the consulted illness exists
        query_check_consulted_illness = "SELECT consIllness_Id FROM consulted_illness WHERE consIllness_Id = %s"
        db[0].execute(query_check_consulted_illness, (consIllness_Id,))
        existing_consulted_illness = db[0].fetchone()

        if not existing_consulted_illness:
            raise HTTPException(status_code=404, detail="Consulted Illness not found")

        # Delete the consulted illness
        query_delete_consulted_illness = "DELETE FROM consulted_illness WHERE consIllness_Id = %s"
        db[0].execute(query_delete_consulted_illness, (consIllness_Id,))
        db[1].commit()

        return {"message": "Consulted Illness deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
