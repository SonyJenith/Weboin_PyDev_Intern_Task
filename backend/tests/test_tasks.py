import pytest


def test_create_task(client, db, registered_user):
    """Test creating a task."""
    task_data = {"title": "Test Task", "description": "This is a test task"}
    headers = {"Authorization": f"Bearer {registered_user['token']}"}
    
    response = client.post("/tasks/", json=task_data, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["completed"] is False
    assert data["owner_id"] == registered_user["user_id"] if "user_id" in registered_user else True


def test_get_all_tasks(client, db, registered_user):
    """Test retrieving all tasks."""
    # Create a few tasks
    headers = {"Authorization": f"Bearer {registered_user['token']}"}
    for i in range(3):
        task_data = {"title": f"Task {i}", "description": f"Description {i}"}
        client.post("/tasks/", json=task_data, headers=headers)
    
    response = client.get("/tasks/", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["tasks"]) == 3
    assert data["page"] == 1
    assert data["page_size"] == 10


def test_get_task_by_id(client, db, registered_user):
    """Test retrieving a specific task by ID."""
    headers = {"Authorization": f"Bearer {registered_user['token']}"}
    
    # Create a task
    task_data = {"title": "Test Task", "description": "Description"}
    response = client.post("/tasks/", json=task_data, headers=headers)
    task_id = response.json()["id"]
    
    # Get the task
    response = client.get(f"/tasks/{task_id}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == task_data["title"]


def test_get_nonexistent_task(client, db, registered_user):
    """Test retrieving a nonexistent task."""
    headers = {"Authorization": f"Bearer {registered_user['token']}"}
    response = client.get("/tasks/999", headers=headers)
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_update_task(client, db, registered_user):
    """Test updating a task."""
    headers = {"Authorization": f"Bearer {registered_user['token']}"}
    
    # Create a task
    task_data = {"title": "Original Title", "description": "Original Description"}
    response = client.post("/tasks/", json=task_data, headers=headers)
    task_id = response.json()["id"]
    
    # Update the task
    update_data = {"title": "Updated Title", "description": "Updated Description"}
    response = client.put(f"/tasks/{task_id}", json=update_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]


def test_mark_task_completed(client, db, registered_user):
    """Test marking a task as completed."""
    headers = {"Authorization": f"Bearer {registered_user['token']}"}
    
    # Create a task
    task_data = {"title": "Test Task"}
    response = client.post("/tasks/", json=task_data, headers=headers)
    task_id = response.json()["id"]
    
    # Mark as completed
    update_data = {"completed": True}
    response = client.put(f"/tasks/{task_id}", json=update_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True


def test_delete_task(client, db, registered_user):
    """Test deleting a task."""
    headers = {"Authorization": f"Bearer {registered_user['token']}"}
    
    # Create a task
    task_data = {"title": "Test Task"}
    response = client.post("/tasks/", json=task_data, headers=headers)
    task_id = response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/tasks/{task_id}", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted"
    
    # Verify it's deleted
    response = client.get(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 404


def test_cannot_access_other_users_task(client, db, registered_user):
    """Test that a user cannot access another user's task."""
    headers = {"Authorization": f"Bearer {registered_user['token']}"}
    
    # Create a task
    task_data = {"title": "Test Task"}
    response = client.post("/tasks/", json=task_data, headers=headers)
    task_id = response.json()["id"]
    
    # Register another user
    other_user_data = {"username": "otheruser", "email": "other@example.com", "password": "pass123"}
    client.post("/auth/register", json=other_user_data)
    login_response = client.post("/auth/login", json={"username": "otheruser", "password": "pass123"})
    other_token = login_response.json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}
    
    # Try to access the task with other user's token
    response = client.get(f"/tasks/{task_id}", headers=other_headers)
    
    assert response.status_code == 404


def test_get_tasks_with_filter(client, db, registered_user):
    """Test retrieving tasks with completed filter."""
    headers = {"Authorization": f"Bearer {registered_user['token']}"}
    
    # Create some tasks
    task_data1 = {"title": "Pending Task"}
    response = client.post("/tasks/", json=task_data1, headers=headers)
    task1_id = response.json()["id"]
    
    task_data2 = {"title": "Completed Task"}
    response = client.post("/tasks/", json=task_data2, headers=headers)
    task2_id = response.json()["id"]
    
    # Mark second task as completed
    client.put(f"/tasks/{task2_id}", json={"completed": True}, headers=headers)
    
    # Get only completed tasks
    response = client.get("/tasks/?completed=true", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["completed"] is True


def test_get_tasks_pagination(client, db, registered_user):
    """Test task pagination."""
    headers = {"Authorization": f"Bearer {registered_user['token']}"}
    
    # Create 15 tasks
    for i in range(15):
        task_data = {"title": f"Task {i}"}
        client.post("/tasks/", json=task_data, headers=headers)
    
    # Get first page (default page_size=10)
    response = client.get("/tasks/?page=1", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 15
    assert len(data["tasks"]) == 10
    assert data["page"] == 1
    
    # Get second page
    response = client.get("/tasks/?page=2", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 5
    assert data["page"] == 2
