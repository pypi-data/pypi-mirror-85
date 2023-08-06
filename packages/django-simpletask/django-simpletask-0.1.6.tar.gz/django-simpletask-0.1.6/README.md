# django-simpletask

Django application provides simple task model and admin.


## Install

```
pip install django-simpletask
```

## Usage

**pro/settings**

```
INSTALLED_APPS = [
    'django_db_lock',
]
```

**Note:**

- Mostly you need a lock service, so we add django_db_lock in INSTALLED_APPS.

**app/models.py**

```
from django_simpletask.models import SimpleTask


class Task(SimpleTask):
    pass
```

**app/admin.py**

```
from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status"]
    readonly_fields = [] + Task.SIMPLE_TASK_FIELDS
```

**app/management/commands/doTasks.py**

```
import djclick as click
from app.models import SomeSimpleTaskModel

@click.command()
def main():
    SomeSimpleTaskModel.do_tasks()

```

## Release

### v0.1.6 2020/11/17

- Add reset action.
- Add SimpleTask.force_finish.
- Add multi-threads serve.

### v0.1.3 2020/11/09

- Add idle_sleep_time parameter for SimpleTask.serve_forever.

### v0.1.2 2020/11/09

- Add SimpleTask.serve and SimpleTask.serve_forever.

### v0.1.1 2020/10/30

- Add SimpleTask.do_tasks.

### v0.1.0 2020/10/26

- First release.
- Take from django-fastadmin. django-fastadmin should forcus on admin extensions, but NOT abstract models.
