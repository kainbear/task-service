'''schemas.py'''

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class ProjectType(str, Enum):
    '''Класс схемы статуса выполнения проекта'''
    ATWORK = 'at work'
    COMPLITED = 'complited'
    FAILED = 'failed'

class ProjectBase(BaseModel):
    '''Класс модели проекта'''
    name: str
    type: ProjectType = Field(description="Type of project: 'at work', 'complited', 'failed'")


    @field_validator('name')
    def to_lower(cls, v):
        return v.lower() if isinstance(v, str) else v

class ProjectCreate(ProjectBase):
    '''Класс модели проекта создания'''
    pass

class ProjectResponse(ProjectBase):
    '''Класс модели проекта создания'''
    id : int
    name : str
    type: ProjectType = Field(description="Type of project: 'at work', 'complited', 'failed'")

class Project(ProjectBase):
    '''Класс модели проекта айди'''
    id: int

    class ConfigDict:
        '''Класс конфига проекта'''
        from_attributes = True

class TaskType(str, Enum):
    '''Класс схемы статуса выполнения задачи'''
    ATWORK = 'at work'
    COMPLITED = 'complited'
    FAILED = 'failed'

class TaskBase(BaseModel):
    '''Класс модели задачи и зависимости'''
    title: str
    description: str
    due_date: datetime
    actual_due_date: datetime | None = None
    hours_spent: int = 0
    user_id : int | None = None
    project_id: Optional[int] = None
    type: TaskType = Field(description="Type of task: 'at work', 'complited', 'failed'")

    @field_validator('title', 'description')
    def to_lower(cls, v):
        return v.lower() if isinstance(v, str) else v

class TaskUpdate(BaseModel):
    '''Класс модели обновления задачи'''
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    actual_due_date: Optional[datetime] = None
    hours_spent: Optional[int] = None
    user_id: Optional[int] = None
    project_id: Optional[int] = None
    type: Optional[TaskType] = Field(description="Type of task: 'at work', 'completed', 'failed'")

    @field_validator('title', 'description')
    def to_lower(cls, v):
        return v.lower() if isinstance(v, str) else v

class TaskCreate(BaseModel):
    '''Класс модели создания задачи'''
    title: str
    description: str
    due_date: datetime
    actual_due_date: datetime | None = None
    hours_spent: int = 0
    user_id : int | None = None
    project_id: int
    type: TaskType = Field(description="Type of task: 'at work', 'complited', 'failed'")

    @field_validator('title', 'description')
    def to_lower(cls, v):
        return v.lower() if isinstance(v, str) else v

    class Meta:
        '''Класс таблицы задач'''
        table = "tasks"

class Task(TaskBase):
    '''Класс модели проекта к задаче'''
    id: int
    project: Project

    @field_validator('title', 'description')
    def to_lower(cls, v):
        return v.lower() if isinstance(v, str) else v

    class ConfigDict:
        '''Класс модели конфига задачи'''
        from_attributes = True
