# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db


MedicineRouter = APIRouter(tags=["Medicine"])

# CRUD operations

@MedicineRouter.get("/manage_med/", response_model=list)
async def read_medicine(
    db=Depends(get_db)
):
    query = "SELECT medicine_ID, nurseID, brandName, drugName, expiration, quantity FROM manage_med"
    db[0].execute(query)
    medicine = [{
            "medicine_ID": manage_med[0],
            "nurseID": manage_med[1],
            "brandName": manage_med[2],
            "drugName": manage_med[3],
            "expiration": manage_med[4],
            "quantity": manage_med[5]
        } 
            for manage_med in db[0].fetchall()]
    return medicine

@MedicineRouter.get("/manage_med/{medicine_Id}", response_model=dict)
async def read_medicine(
    medicine_ID: int, 
    db=Depends(get_db)
):
    query = "SELECT medicine_ID, nurseID, brandName, drugName, expiration, quantity FROM manage_med WHERE medicine_ID = %s"
    db[0].execute(query, (medicine_ID,))
    manage = db[0].fetchone()
    if manage:
        return {
            "medicine_ID": manage[0],
            "nurseID": manage[1],
            "brandName": manage[2],
            "drugName": manage[3],
            "expiration": manage[4],
            "quantity": manage[5]
        }
    raise HTTPException(status_code=404, detail="Medicine not found")

@MedicineRouter.post("/manage_med/", response_model=dict)
async def create_medicine(
    nurseID: str = Form(...), 
    brandName: str = Form(...),
    drugName: str = Form(...),
    expiration: str = Form(...),
    quantity: int = Form(...), 
    db=Depends(get_db)
):

    query = "INSERT INTO manage_med (nurseID, brandName, drugName, expiration, quantity) VALUES (%s, %s, %s, %s, %s)"
    db[0].execute(query, (nurseID, brandName, drugName, expiration, quantity))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_manage_id = db[0].fetchone()[0]
    db[1].commit()

    return {
    "medicine_ID": new_manage_id,
    "nurseID": nurseID,
    "brandName": brandName,
    "drugName": drugName,
    "expiration": expiration,
    "quantity": quantity
}

@MedicineRouter.put("/manage_med/{student_Id}", response_model=dict)
async def update_medicine(
    medicine_ID: int,
    nurseID: str = Form(...), 
    brandName: str = Form(...),
    drugName: str = Form(...),
    expiration: str = Form(...),
    quantity: int = Form(...),
    db=Depends(get_db)
):

    # Update user information in the database 
    query = "UPDATE manage_med SET nurseID = %s, brandName = %s, drugName = %s, expiration = %s, quantity = %s WHERE medicine_ID = %s"
    db[0].execute(query, (nurseID, brandName, drugName, expiration, quantity, medicine_ID))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Medicine updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="Medicine not found")

@MedicineRouter.delete("/manage_med/{medicine_ID}", response_model=dict)
async def delete_medicine(
    medicine_ID: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_manage = "SELECT medicine_ID FROM manage_med WHERE medicine_ID = %s"
        db[0].execute(query_check_manage, (medicine_ID,))
        existing_manage = db[0].fetchone()

        if not existing_manage:
            raise HTTPException(status_code=404, detail="Medicine not found")

        # Delete the user
        query_delete_manage = "DELETE FROM manage_med WHERE medicine_ID = %s"
        db[0].execute(query_delete_manage, (medicine_ID,))
        db[1].commit()

        return {"message": "Medicine deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
