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
    project = fields.ForeignKeyField('models.Project', related_name='tasks', on_delete=fields.CASCADE)
    name_employee = fields.CharField(64, null=True)
    task = fields.CharField(64)
    type = fields.CharField(max_length=20)  # 'at work', 'complited', 'failed'

    class Meta:
        '''Класс таблицы задач'''
        table = "tasks"