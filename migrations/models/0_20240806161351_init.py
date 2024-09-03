from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "projects" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL UNIQUE,
    "type" VARCHAR(20) NOT NULL
);
COMMENT ON TABLE "projects" IS 'Класс модели проекта';
CREATE TABLE IF NOT EXISTS "tasks" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" INT,
    "title" VARCHAR(250),
    "description" VARCHAR(250),
    "due_date" TIMESTAMPTZ,
    "actual_due_date" TIMESTAMPTZ,
    "hours_spent" INT   DEFAULT 0,
    "type" VARCHAR(20) NOT NULL,
    "project_id" INT NOT NULL REFERENCES "projects" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "tasks" IS 'Класс модели заданий';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
