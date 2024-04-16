# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db

AdminRouter = APIRouter(tags=["Admin"])

# CRUD operations for admin

@AdminRouter.get("/admin/", response_model=list)
async def read_admins(
    db=Depends(get_db)
):
    query = "SELECT nurseID, username, email FROM admin"
    db[0].execute(query)
    admins = [{
        "nurseID": admin[0], 
        "username": admin[1],
        "email": admin[2]
        } 
    for admin in db[0].fetchall()]
    return admins

@AdminRouter.get("/admin/{nurseID}", response_model=dict)
async def read_admin(
    nurseID: int, 
    db=Depends(get_db)
):
    query = "SELECT nurseID, username, email FROM admin WHERE nurseID = %s"
    db[0].execute(query, (nurseID,))
    admin = db[0].fetchone()
    if admin:
        return {
            "nurseID": admin[0], 
            "username": admin[1],
            "email": admin[2]
            }
    raise HTTPException(status_code=404, detail="Admin not found")

@AdminRouter.post("/admin/", response_model=dict)
async def create_admin(
    username: str = Form(...), 
    password: str = Form(...), 
    email: str = Form(...), 
    db=Depends(get_db)
):

    query = "INSERT INTO admin (username, password, email) VALUES (%s, %s, %s)"
    db[0].execute(query, (username, password, email))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_nurseID = db[0].fetchone()[0]
    db[1].commit()

    return {
        "nurseID": new_nurseID, 
        "username": username,
        "email": email
        }

@AdminRouter.put("/admin/{nurseID}", response_model=dict)
async def update_admin(
    nurseID: int,
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    db=Depends(get_db)
):

    # Update admin information in the database 
    query = "UPDATE admin SET username = %s, password = %s, email = %s WHERE nurseID = %s"
    db[0].execute(query, (username, password, email, nurseID))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Admin data updated successfully"}
    
    # If no rows were affected, admin not found
    raise HTTPException(status_code=404, detail="Admin not found")

@AdminRouter.delete("/admin/{nurseID}", response_model=dict)
async def delete_admin(
    nurseID: int,
    db=Depends(get_db)
):
    try:
        # Check if the admin exists
        query_check_admin = "SELECT nurseID FROM admin WHERE nurseID = %s"
        db[0].execute(query_check_admin, (nurseID,))
        existing_admin = db[0].fetchone()

        if not existing_admin:
            raise HTTPException(status_code=404, detail="Admin not found")

        # Delete the admin
        query_delete_admin = "DELETE FROM admin WHERE nurseID = %s"
        db[0].execute(query_delete_admin, (nurseID,))
        db[1].commit()

        return {"message": "Admin deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
