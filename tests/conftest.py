'''conftest.py'''

from typing import AsyncGenerator
from contextlib import asynccontextmanager
import httpx
import pytest_asyncio
from fastapi import FastAPI
from tortoise import Tortoise
from models import Project, Tasks
from router import task_router
from router import project_router

@pytest_asyncio.fixture
async def init_db()-> AsyncGenerator[None, None]:
    '''Функция для  инициализации бд для тестов'''
    await Tortoise.init(
         db_url="postgres://kainbear:sups4@127.0.0.1:5432/tasks",
         modules={'models': ['models']},)
    await Tortoise.generate_schemas()
    print("Tortoise is on")
    yield
    await Tortoise.close_connections()
    print("Tortoise is off")

@pytest_asyncio.fixture
async def app(init_db) -> AsyncGenerator[FastAPI, None]:
    '''Функция для жизненного цикла приложения для тестов'''
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        yield

    app = FastAPI(lifespan=lifespan)
    app.include_router(project_router)
    app.include_router(task_router)
    yield app

@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator[httpx.AsyncClient, None]:
    '''Функция для имитации пользователя'''
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://127.0.0.1:8000"
        ) as client:
        print("Client is on")
        yield client
        print("Client is off")

@pytest_asyncio.fixture
async def create_project():
    '''Функция для создания проекта в тестовой бд'''
    proj = await Project.create(
        name = "Project1",
        type = "at work"
    )
    yield proj
    await proj.delete()

@pytest_asyncio.fixture
async def create_project_another():
    '''Функция для создания проекта в тестовой бд'''
    proj = await Project.create(
        name = "Project2",
        type = "at work"
    )
    yield proj


@pytest_asyncio.fixture
async def create_task():
    '''Функция для создания задачи'''
    task = await Tasks.create(
        project_id = "2",
        name_employee = "Solodilov",
        task = "Сделать сайт",
        type = "at work",
    )
    yield task
