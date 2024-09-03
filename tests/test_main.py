'''test_main.py'''

from httpx import AsyncClient
import pytest
from models import Tasks

@pytest.mark.asyncio
async def test_read_all_projects(client: AsyncClient, create_project):
    ''' Тест функции для  получения всех проектов'''
    await create_project
    response = await client.get("/project/read_all")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 0
    print("Response data:", data)

@pytest.mark.asyncio
async def test_create_project(client: AsyncClient):
    ''' Тест функции для  добавления проекта'''
    new_proj = {
        "name" : "Project0",
        "type" : "at work",
    }
    response = await client.post("/project/add", params=new_proj)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Project0".lower()
    assert data["type"] == "at work".lower()
    print("Response data:", data)

@pytest.mark.asyncio
async def test_update_project(client):
    ''' Тест функции для  обновления проекта'''
    new_proj = {
        "name" : "project5",
        "type" : "at work",
    }
    response = await client.post("/project/add", params=new_proj)
    assert response.status_code == 200
    data = response.json()
    print("Response data:", data)
    project_id = data["id"]
    project_name = data["name"]
    project_type = data["type"]

    updated_proj_data = {
        "name" : "project6",
        "type" : "complited",
    }
    response = await client.put(f"/project/update?id={project_id}&name={project_name}&type={project_type}",
                                params=updated_proj_data)
    assert response.status_code == 200
    updated_data = response.json()
    print("Updated Response Data:", updated_data)
    assert updated_data["name"] == "project6"
    assert updated_data["type"] == "complited"

@pytest.mark.asyncio
async def test_delete_project(client, create_project_another):
    ''' Тест функции для  удаления проекта'''
    response = await client.delete(f"/project/{create_project_another.id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Project deleted"
    data = response.json()
    print("Response data:", data )

    response = await client.get(f"/search?last_name={create_project_another.name}")
    assert response.status_code == 404
    data = response.json()
    print("Response data:", data )

@pytest.mark.asyncio
async def test_read_all_tasks(client: AsyncClient, create_task):
    ''' Тест функции для  получения всех проектов'''
    await create_task
    response = await client.get("/task/read_all")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 0
    print("Response data:", data)

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    ''' Тест функции для  добавления проекта'''
    new_task = {
        "project_id" : 2,
        "name_employee" : "Solodilov",
        "task" : "Сделать кибаб",
        "type" : "at work",
    }
    response = await client.post("/task/add", params=new_task)
    assert response.status_code == 200
    data = response.json()
    assert data["project_id"] == 2
    assert data["name_employee"] == "Solodilov".lower()
    assert data["task"] == "Сделать кибаб".lower()
    assert data["type"] == "at work".lower()
    print("Response data:", data)

@pytest.mark.asyncio
async def test_search_task(client, create_task):
    ''' Тест функции для  получения у работника отпуска или командировки'''
    await create_task
    task1 = await Tasks.create(
        project_id = 2,
        task_id=create_task.id,
        name_employee="Solodilov".lower(),
        task = "сделать".lower(),
        type="at work".lower(),
    )
    await task1
    response = await client.get(f"/task/search?task_id={create_task.id}&type=at work")
    assert response.status_code == 200
    data = response.json()
    print("response data:", data)

@pytest.mark.asyncio
async def test_update_task(client):
    ''' Тест функции для  обновления проекта'''
    new_task = {
        "task_id" : 1,
        "project_id" : 2,
        "name_employee" : "денисов",
        "task" : "сделать шаурму",
        "type" : "at work",
    }
    response = await client.post("/task/add", params=new_task)
    assert response.status_code == 200
    data = response.json()
    print("Response data:", data)
    task_id = data["id"]
    project_id = data["id"]

    updated_task_data = {
        "task_id" : 1,
        "project_id" : 3,
        "name_employee" : "мурченко",
        "task" : "сделать шаурму",
        "type" : "complited",
    }
    response = await client.put(f"/task/update?id={task_id}&project_id={project_id}&type={type}",
                                params=updated_task_data)
    assert response.status_code == 200
    updated_data = response.json()
    print("Updated Response Data:", updated_data)
    assert updated_data["project_id"] == 3
    assert updated_data["name_employee"] == "мурченко"
    assert updated_data["task"] == "сделать шаурму"
    assert updated_data["type"] == "complited"


@pytest.mark.asyncio
async def test_delete_task(client, create_task):
    ''' Тест функции для  удаления задачи'''
    response = await client.delete(f"/task/{create_task.id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Task deleted"
    data = response.json()
    print("Response data:", data )

    response = await client.get(f"/search?task={create_task.task}")
    assert response.status_code == 404
    data = response.json()
    print("Response data:", data )
