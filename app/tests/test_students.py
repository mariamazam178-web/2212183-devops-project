def test_create_student(client):
    student_data = {
        "reg_no": "2023CS101",
        "name": "Test Student",
        "email": "test@example.com"
    }
    response = client.post("/students", json=student_data)
    assert response.status_code == 200
    data = response.json()
    assert data["reg_no"] == student_data["reg_no"]
    assert data["name"] == student_data["name"]
    assert data["email"] == student_data["email"]
    assert "id" in data

def test_get_all_students(client):
    # First create a student
    student_data = {
        "reg_no": "2023CS102",
        "name": "Another Student", 
        "email": "another@example.com"
    }
    client.post("/students", json=student_data)
    
    # Then get all students
    response = client.get("/students")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    # Check that our created student exists in the list
    reg_nos = [s["reg_no"] for s in data]
    assert "2023CS102" in reg_nos





def test_get_student_by_reg_no(client):
    # Create a student
    student_data = {
        "reg_no": "2023CS103",
        "name": "Find Me",
        "email": "find@example.com"
    }
    client.post("/students", json=student_data)
    
    # Get by registration number
    response = client.get("/students/2023CS103")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Find Me"

def test_get_nonexistent_student(client):
    response = client.get("/students/NONEXISTENT")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

def test_duplicate_registration(client):
    student_data = {
        "reg_no": "DUPLICATE123",
        "name": "First",
        "email": "first@example.com"
    }
    client.post("/students", json=student_data)
    
    # Try to create same reg_no again
    response = client.post("/students", json=student_data)
    assert response.status_code == 400"# Student CRUD tests" 
