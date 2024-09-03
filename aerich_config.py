'''aerich_config.py'''

DATABASE_URL = "postgres://kainbear:sups4@postgres-tasks:5432/tasks"

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models" : {
            "models" : ["models","aerich.models"],
            "default_connection": "default",
        },
    },
}
