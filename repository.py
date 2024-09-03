'''repository.py'''

from datetime import datetime
from typing import List, Optional
import httpx
from pydantic import BaseModel
from models import Project, Tasks
from schemas import ProjectBase, TaskCreate, ProjectCreate, TaskUpdate

USER_SERVICE_URL = "http://user-service:8003"

class Repository(BaseModel):
    '''Класс функций для роутера'''

    @classmethod
    async def check_user_exists(cls, user_id: int) -> bool:
        '''Функция для проверки существования пользователя через внешний сервис'''
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{USER_SERVICE_URL}/employee/search?id={user_id}")
            if response.status_code == 200:
                user_data = response.json()
                return bool(user_data)
            return False

    @classmethod
    async def get_all_projects(cls) -> List[Project]:
        '''Функция для получения списка всех проектов'''
        return await Project.all()

    @classmethod
    async def create_project(cls, project: ProjectCreate) -> Project:
        '''Функция для создания нового проекта'''
        return await Project.create(**project.model_dump())

    @classmethod
    async def update_project(cls, id: int, project: ProjectBase):
        '''Функция для обновления проекта'''
        proj = await Project.get_or_none(id=id)
        if proj:
            await proj.update_from_dict(project.model_dump(exclude_none=True))
            await proj.save()
            return proj
        return proj

    @classmethod
    async def delete_project(cls, id: int) -> bool:
        '''Функция для удаления проекта'''
        proj = await Project.get_or_none(id=id)
        if proj:
            await proj.delete()
            return True
        return False

    @classmethod
    async def get_all_tasks(cls) -> List[Tasks]:
        '''Функция для получения списка всех задач'''
        return await Tasks.all().prefetch_related('project')

    @classmethod
    async def get_task(
        cls,
        id: Optional[int] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        user_id: Optional[int] = None,
        project_id: Optional[int] = None,
        project: Optional[str] = None,
    ) -> List[Tasks]:
        '''Функция для получения задач по фильтрам'''
        query = Tasks.all().prefetch_related('project')
        if id:
            query = query.filter(id=id)
        if title:
            query = query.filter(title__icontains=title)
        if description:
            query = query.filter(description__icontains=description)
        if user_id:
            query = query.filter(user_id=user_id)
        if project_id:
            query = query.filter(project_id=project_id)
        if project:
            query = query.filter(project__name__icontains=project)
        return await query

    @classmethod
    async def create_task(cls, task: TaskCreate) -> Tasks:
        '''Функция для создания новой задачи'''
        project = await Project.get(id=task.project_id)
        if task.user_id:
            is_on_vacation = await cls.check_user_vacation_status(task.user_id, task.due_date)
            if is_on_vacation:
                raise ValueError("Employee is on vacation during the specified period")
        return await Tasks.create(project=project, **task.model_dump(exclude={"project_id"}))

    @classmethod
    async def update_task(cls, id: int, tasks: TaskUpdate):
        '''Функция для обновления задачи'''
        task = await Tasks.get_or_none(id=id)
        if task:
            if tasks.user_id:
                is_on_vacation = await cls.check_user_vacation_status(tasks.user_id, tasks.due_date)
                if is_on_vacation:
                    raise ValueError("Работник находится в отпуске")
            await task.update_from_dict(tasks.model_dump(exclude_none=True))
            await task.save()
            return task
        return task

    @classmethod
    async def check_user_vacation_status(cls, user_id: int, due_date: datetime) -> bool:
        '''Функция для проверки статуса отпуска сотрудника на указанную дату'''
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{USER_SERVICE_URL}/business_and_vacations/search?employee_id={user_id}&type=vacation")
            if response.status_code == 200:
                user_data = response.json()
                vacations = user_data[0].get('vacations', [])
                for vacation in vacations:
                    start_date = datetime.strptime(vacation['start_date'], '%Y-%m-%d').date()
                    end_date = datetime.strptime(vacation['end_date'], '%Y-%m-%d').date()
                    if start_date <= due_date.date() <= end_date:
                        return True
            return False

    @classmethod
    async def delete_task(cls, id: int) -> bool:
        '''Функция для удаления задачи'''
        task = await Tasks.get_or_none(id=id)
        if task:
            await task.delete()
            return True
        return False
