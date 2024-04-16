# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db

IllnessRouter = APIRouter(tags=["Illness"])

# CRUD operations for manage_illness

@IllnessRouter.get("/manage_illness/", response_model=list)
async def read_illness(
    db=Depends(get_db)
):
    query = "SELECT illness_Id, nurseID, illness FROM manage_illness"
    db[0].execute(query)
    illness = [{
            "illness_Id": manage_ill[0],
            "nurseID": manage_ill[1],
            "illness": manage_ill[2]
        } 
            for manage_ill in db[0].fetchall()]
    return illness

@IllnessRouter.get("/manage_illness/{illness_Id}", response_model=dict)
async def read_illness(
    illness_Id: int, 
    db=Depends(get_db)
):
    query = "SELECT illness_Id, nurseID, illness FROM manage_illness WHERE illness_Id = %s"
    db[0].execute(query, (illness_Id,))
    manage_ill = db[0].fetchone()
    if manage_ill:
        return {
            "illness_Id": manage_ill[0],
            "nurseID": manage_ill[1],
            "illness": manage_ill[2]
        }
    raise HTTPException(status_code=404, detail="Illness not found")

@IllnessRouter.post("/manage_illness/", response_model=dict)
async def create_illness(
    nurseID: int = Form(...), 
    illness: str = Form(...),
    db=Depends(get_db)
):
    query = "INSERT INTO manage_illness (nurseID, illness) VALUES (%s, %s)"
    db[0].execute(query, (nurseID, illness))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_manage_id = db[0].fetchone()[0]
    db[1].commit()

    return {
    "illness_Id": new_manage_id,
    "nurseID": nurseID,
    "illness": illness
}

@IllnessRouter.put("/manage_illness/{illness_Id}", response_model=dict)
async def update_illness(
    illness_Id: int,
    nurseID: int = Form(...), 
    illness: str = Form(...),
    db=Depends(get_db)
):
    # Update illness information in the database 
    query = "UPDATE manage_illness SET nurseID = %s, illness = %s WHERE illness_Id = %s"
    db[0].execute(query, (nurseID, illness, illness_Id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Illness updated successfully"}
    
    # If no rows were affected, illness not found
    raise HTTPException(status_code=404, detail="Illness not found")

@IllnessRouter.delete("/manage_illness/{illness_Id}", response_model=dict)
async def delete_illness(
    illness_Id: int,
    db=Depends(get_db)
):
    try:
        # Check if the illness exists
        query_check_illness = "SELECT illness_Id FROM manage_illness WHERE illness_Id = %s"
        db[0].execute(query_check_illness, (illness_Id,))
        existing_illness = db[0].fetchone()

        if not existing_illness:
            raise HTTPException(status_code=404, detail="Illness not found")

        # Delete the illness
        query_delete_illness = "DELETE FROM manage_illness WHERE illness_Id = %s"
        db[0].execute(query_delete_illness, (illness_Id,))
        db[1].commit()

        return {"message": "Illness deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
