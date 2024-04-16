# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db


ManageRouter = APIRouter(tags=["Manage"])

# CRUD operations

@ManageRouter.get("/manage/", response_model=list)
async def read_manage(
    db=Depends(get_db)
):
    query = "SELECT student_Id, student_Lname, student_Fname, course FROM manage"
    db[0].execute(query)
    manage = [{
        "student_Id": manage[0], 
        "student_Lname": manage[1],
        "student_Fname": manage[2],
        "course": manage[3]
        } 
    for manage in db[0].fetchall()]
    return manage

@ManageRouter.get("/manage/{student_Id}", response_model=dict)
async def read_manage(
    student_Id: int, 
    db=Depends(get_db)
):
    query = "SELECT student_Id, student_Lname, student_Fname, course FROM manage WHERE student_Id = %s"
    db[0].execute(query, (student_Id,))
    manage = db[0].fetchone()
    if manage:
        return {
            "student_Id": manage[0], 
            "student_Lname": manage[1],
            "student_Fname": manage[2],
            "course": manage[3]
            }
    raise HTTPException(status_code=404, detail="Student not found")

@ManageRouter.post("/manage/", response_model=dict)
async def create_manage(
    nurseID: int = Form(...),
    course: str = Form(...), 
    student_Lname: str = Form(...), 
    student_Fname: str = Form(...), 
    db=Depends(get_db)
):

    query = "INSERT INTO manage (nurseID, course, student_Lname, student_Fname) VALUES (%s,%s, %s, %s)"
    db[0].execute(query, (nurseID, course, student_Lname, student_Fname))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_manage_id = db[0].fetchone()[0]
    db[1].commit()

    return {
        "student_Id": new_manage_id,
        "nurseID": nurseID,
        "student_Lname": student_Lname,
        "student_Fname": student_Fname,
        "course": course
        }

@ManageRouter.put("/manage/{student_Id}", response_model=dict)
async def update_manage(
    student_Id: int,
    nurseID: int,
    student_Lname: str = Form(...),
    student_Fname: str = Form(...),
    course: str = Form(...),
    db=Depends(get_db)
):

    # Update user information in the database 
    query = "UPDATE manage SET nurseID = %s, student_Lname = %s, student_Fname = %s, course = %s WHERE student_Id = %s"
    db[0].execute(query, (nurseID, student_Lname, student_Fname, course, student_Id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Student's data updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="Student not found")

@ManageRouter.delete("/manage/{student_Id}", response_model=dict)
async def delete_manage(
    student_Id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_manage = "SELECT student_Id FROM manage WHERE student_Id = %s"
        db[0].execute(query_check_manage, (student_Id,))
        existing_manage = db[0].fetchone()

        if not existing_manage:
            raise HTTPException(status_code=404, detail="Student not found")

        # Delete associated records in the consult table
        query_delete_consult = "DELETE FROM consult WHERE student_Id = %s"
        db[0].execute(query_delete_consult, (student_Id,))

        # Delete the user
        query_delete_manage = "DELETE FROM manage WHERE student_Id = %s"
        db[0].execute(query_delete_manage, (student_Id,))
        db[1].commit()

        return {"message": "Student deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
