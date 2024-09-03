''' main.py'''

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from router import project_router, task_router
import aerich_config

app = FastAPI(
        title="Task-Service",
        version="1.0.0",
        description="Сервис для создания и хранения проектов и задач.",
    )

app.include_router(project_router)
app.include_router(task_router)

register_tortoise(
    app,
    db_url=aerich_config.DATABASE_URL,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)
