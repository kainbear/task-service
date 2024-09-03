'''router.py'''

from typing import Annotated, List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from repository import Repository
from schemas import Project, ProjectBase, ProjectCreate, ProjectResponse, Task, TaskCreate, TaskUpdate

project_router = APIRouter(prefix="/project", tags=["Projects"])
task_router = APIRouter(prefix="/task", tags=["Tasks"])

repo = Repository()

@project_router.get("/read_all")
async def read_all_projects():
    '''Функция получения всех проектов'''
    return await repo.get_all_projects()

@project_router.post("/add", response_model=ProjectResponse)
async def create_project(project: Annotated[ProjectCreate, Depends()]):
    '''Функция создания проектов'''
    return await repo.create_project(project)

@project_router.put("/update")
async def update_project(id: int, project: Annotated[ProjectBase, Depends()]):
    '''Функция обновления проектов'''
    proj = await repo.update_project(id, project)
    if proj is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj

@project_router.delete("/{id}")
async def delete_project(id: int):
    '''Функция для удаления проекта'''
    success = await repo.delete_project(id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"detail": "Project deleted"}

@task_router.get("/read_all")
async def read_all_tasks():
    '''Функция для получения всех задачи'''
    return await repo.get_all_tasks()

@task_router.post("/add")
async def create_task(task: Annotated[TaskCreate, Depends()]):
    '''Функция для создания задачи'''
    try:
        created_task = await repo.create_task(task)
        return created_task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@task_router.get("/search", response_model=List[Task])
async def search_task(
    id: Optional[int] = Query(default=None),
    title: Optional[str] = Query(default=None),
    description: Optional[str] = Query(default=None),
    user_id: Optional[int] = Query(default=None),
    project_id: Optional[int] = Query(default=None),
    project: Optional[str] = Query(default=None),
):
    '''Функция для поиска задачи'''
    tasks = await repo.get_task(
        id=id,
        title=title,
        description=description,
        user_id=user_id,
        project_id=project_id,
        project=project,
        )
    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks or Projects not found")
    return tasks

@task_router.put("/update")
async def update_task(id: int, task: Annotated[TaskUpdate, Depends()]):
    '''Функция для обновления задачи'''
    try:
        updated_task = await repo.update_task(id, task)
        if updated_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated_task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@task_router.delete("/{id}")
async def delete_task(id: int):
    '''Функция для удаления задачи'''
    success = await repo.delete_task(id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}
