from typing import Optional

import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel


class Employee(BaseModel):
    employee_name: str
    employee_address: str
    employee_age: int
    employee_salary: int
    employee_spouse: Optional[str] = None


app = FastAPI()

while True:
    try:
        cnx = mysql.connector.connect(user='root', password='ritvik',
                                      host='127.0.0.1',
                                      database='employee')
        curA = cnx.cursor(buffered=True)
        print("Database connected successfully!")
        break
    except Exception as error:
        print(f"Error: {error}")


@app.get("/")
def get_employees():
    query = "SELECT * FROM employee"
    response = []
    curA.execute(query)
    for (id, name, address, age, salary, spouse) in curA:
        response.append({
            "id": id,
            "name": name,
            "address": address,
            "age": age,
            "salary": salary,
            "spouse": spouse
        })
    return {
        "data": response
    }


@app.get("/{id}")
def get_employee(id: int):
    query = f"SELECT * FROM employee where id={id}"
    response = []
    curA.execute(query)
    for (id, name, address, age, salary, spouse) in curA:
        response.append({
            "id": id,
            "name": name,
            "address": address,
            "age": age,
            "salary": salary,
            "spouse": spouse
        })
    return {
        "data": response
    }


@app.post("/create")
def create_employee(employee: Employee):
    query = f"INSERT INTO employee (name, address, age, salary, spouse) VALUES ('{employee.employee_name}', '{employee.employee_address}', '{employee.employee_age}', '{employee.employee_salary}', '{employee.employee_spouse}')"
    curA.execute(query)
    return {"data": "Inserted Data"}


@app.put("/update/{id}")
def update_employee(id: int, employee: Employee):
    query = f"UPDATE employee SET name = '{employee.employee_name}', address= '{employee.employee_address}', age = {employee.employee_age}, salary = {employee.employee_salary}, spouse='{employee.employee_spouse}' Where id={id})"
    curA.execute(query)
    return {"data": "Updated Data"}


@app.delete("/delete/{id}")
def delete_employee(id: int):
    query = f"DELETE FROM employee where id={id}"
    curA.execute(query)
    return {"data": "Deleted Data"}


@app.delete("/delete")
def delete_employees():
    query = f"DELETE FROM employee"
    curA.execute(query)
    return {"data": "Deleted Data"}
