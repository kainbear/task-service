'''models.py'''

from tortoise import fields
from tortoise.models import Model

class Project(Model):
    '''Класс модели проекта'''
    id = fields.IntField(pk=True)
    name = fields.CharField(64, unique=True)
    type = fields.CharField(max_length=20)  # 'at work', 'complited', 'failed'

    class Meta:
        '''Класс таблицы проекта'''
        table = "projects"

class Tasks(Model):
    '''Класс модели заданий'''
    id = fields.IntField(pk=True)
    user_id = fields.IntField(null=True)
    project = fields.ForeignKeyField('models.Project', related_name='tasks',
                                      on_delete=fields.CASCADE)
    title = fields.CharField(250,null=True)
    description = fields.CharField(250,null=True)
    due_date = fields.DatetimeField(null=True)
    actual_due_date = fields.DatetimeField(null=True)
    hours_spent = fields.IntField(default=0,null=True)
    type = fields.CharField(max_length=20)  # 'at work', 'complited', 'failed'

    class Meta:
        '''Класс таблицы задач'''
        table = "tasks"
