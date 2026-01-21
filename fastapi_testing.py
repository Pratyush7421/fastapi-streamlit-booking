from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import csv
import os
# print(os.getcwd())

app = FastAPI()

csv_file = "slots.csv"

class Slot(BaseModel):
    id: int
    time: str
    status: str = "available"

slots: List[Slot] = []

# Load from CSV on startup
def load_slots():
    if not os.path.exists(csv_file):
        return
    with open(csv_file, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            slots.append(Slot(id=int(row["id"]), time=row["time"], status=row["status"]))

# Save to CSV
def save_slots():
    with open(csv_file, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "time", "status"])
        writer.writeheader()
        for slot in slots:
            writer.writerow(slot.dict())

load_slots()

@app.post("/slot/create")
def create_slot(time: str):
    slot_id = len(slots) + 1
    new_slot = Slot(id=slot_id, time=time)
    slots.append(new_slot)
    save_slots()
    return {"message": "slot created", "slot": new_slot}

@app.get("/slots")
def get_slots():
    return slots

@app.post("/slot/book/{slot_id}")
def book_slot(slot_id: int, user: str):
    for slot in slots:
        if slot.id == slot_id:
            if slot.status == "booked":
                raise HTTPException(status_code=400, detail="Slot already booked")
            slot.status = "booked"
            save_slots()
            return {"message": f"slot {slot_id} booked by {user}"}
    raise HTTPException(status_code=404, detail="Slot not found")

@app.delete("/slot/cancel/{slot_id}")
def cancel_booking(slot_id: int):
    for slot in slots:
        if slot.id == slot_id:
            if slot.status == "available":
                raise HTTPException(status_code=400, detail="Slot is not booked yet")
            slot.status = "available"
            save_slots()
            return {"message": f"slot {slot_id} booking cancelled"}
    raise HTTPException(status_code=404, detail="Slot not found")

@app.get("/slots/available")
def available_slots():
    return [slot for slot in slots if slot.status == "available"]




# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List
# import openpyxl
# import os

# app = FastAPI()
# EXCEL_FILE = "slots.xlsx"

# class Slot(BaseModel):
#     id: int
#     time: str
#     status: str = "available"
#     user: str = "-"

# slots: List[Slot] = []

# def init_excel():
#     if not os.path.exists(EXCEL_FILE):
#         wb = openpyxl.Workbook()
#         sheet = wb.active
#         sheet.append(["id", "time", "status", "user"])
#         wb.save(EXCEL_FILE)

# def save_to_excel():
#     wb = openpyxl.Workbook()
#     sheet = wb.active
#     sheet.append(["id", "time", "status", "user"])
#     for s in slots:
#         sheet.append([s.id, s.time, s.status, s.user])
#     wb.save(EXCEL_FILE)

# @app.on_event("startup")
# def load_slots():
#     init_excel()
#     wb = openpyxl.load_workbook(EXCEL_FILE)
#     sheet = wb.active
#     for row in sheet.iter_rows(min_row=2, values_only=True):
#         slots.append(Slot(id=row[0], time=row[1], status=row[2], user=row[3]))
#     wb.close()

# @app.post("/slot/create")
# def create_slot(time: str):
#     slot_id = len(slots) + 1
#     new_slot = Slot(id=slot_id, time=time)
#     slots.append(new_slot)
#     save_to_excel()
#     return {"message": "slot created", "slot": new_slot}

# @app.get("/slots")
# def get_slots():
#     return slots

# @app.post("/slot/book/{slot_id}")
# def book_slot(slot_id: int, user: str):
#     for slot in slots:
#         if slot.id == slot_id:
#             if slot.status == "booked":
#                 raise HTTPException(status_code=400, detail="Slot already booked")
#             slot.status = "booked"
#             slot.user = user
#             save_to_excel()
#             return {"message": f"Slot {slot_id} booked by {user}"}
#     raise HTTPException(status_code=404, detail="Slot not found")

# @app.delete("/slot/cancel/{slot_id}")
# def cancel_booking(slot_id: int):
#     for slot in slots:
#         if slot.id == slot_id:
#             if slot.status == "available":
#                 raise HTTPException(status_code=400, detail="Not booked yet")
#             slot.status = "available"
#             slot.user = "-"
#             save_to_excel()
#             return {"message": f"Slot {slot_id} booking cancelled"}
#     raise HTTPException(status_code=404, detail="Slot not found")

# @app.get("/slots/available")
# def available_slots():
#     return [slot for slot in slots if slot.status == "available"]


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List

# app = FastAPI()

# class Slot(BaseModel):
#     id: int
#     time: str
#     status: str = "available"

# slots: List[Slot] = []

# @app.post("/slot/create")
# def create_slot(time: str):
#     slot_id = len(slots) + 1
#     new_slot = Slot(id=slot_id, time=time)
#     slots.append(new_slot)
#     return {"message": "slot created", "slot": new_slot}

# @app.get("/slots")
# def get_slots():
#     return slots

# @app.post("/slot/book/{slot_id}")
# def book_slot(slot_id: int, user: str):
#     for slot in slots:
#         if slot.id == slot_id:
#             if slot.status == "booked":
#                 raise HTTPException(status_code=400, detail="Slot already booked")
#             slot.status = "booked"
#             return {"message": f"slot {slot_id} booked by {user}"}
#     raise HTTPException(status_code=404, detail="Slot not found")

# @app.delete("/slot/cancel/{slot_id}")
# def cancel_booking(slot_id: int):
#     for slot in slots:
#         if slot.id == slot_id:
#             if slot.status == "available":
#                 raise HTTPException(status_code=400, detail="Slot is not booked yet")
#             slot.status = "available"
#             return {"message": f"slot {slot_id} booking cancelled"}
#     raise HTTPException(status_code=404, detail="Slot not found")

# @app.get("/slots/available")
# def available_slots():
#     return [slot for slot in slots if slot.status == "available"]




# from fastapi import FastAPI
# app = FastAPI()
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}
# @app.get("/users/{user_id}/items/{item_id}")
# def read_user_item(user_id: int, item_id: int, q: str = None):
#     return {"user_id": user_id, "item_id": item_id, "q": q}