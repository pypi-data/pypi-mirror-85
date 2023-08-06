PG-DB
=====

PG-DB is simple [Psycopg](https://www.psycopg.org) wrapper.

Usage
-----

First create an DB object and initialise it with the application,
```python
from pg_db import DB

db = DB('test', 'root', debug=True)

def set_user(name):
    db.connect()
    db.execute("INSERT INTO users VALUES('Wendys');", (name, ))
    db.commit()
    db.close()

set_user('xyz')
```

can select one row,
```python
def get_user(id):
    db.connect()
    row = db.one("SELECT name FROM users WHERE id=%s", (id, ), as_dict=True)
    db.close()
    return row['name']

print(get_user(1))
```

can select all rows,
```python
def get_users():
    db.connect()
    rows = db.all("SELECT name FROM users;")
    db.close()
    return rows

print(get_users())
```

Usage on Quart
-----

First create a Quart wrapper file (db.py),
```python
from functools import wraps
from pg_db import DB
from quart import flash, redirect, request, session, url_for  # make_response
from quart_auth import current_user

class db(DB):
  def wrapper(self, func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
      try:
        self.connect(session['schema'] if 'schema' in session else 'public',
                     'QUART_AUTH' in request.cookies and await current_user.readonly)
        return await func(*args, **kwargs)
      except Exception as e:
        self.rollback()
        if self.debug:
          raise e
        await flash("db error -> " + str(e))
        return redirect(url_for(request.endpoint))
        # return await make_response("db error -> " + str(e), 500)
      finally:
        try:
          self.close()
        except:
          pass
    return wrapped
```

Then enable db object from db.py globally for a Quart app,
```python
from json import dumps
from .db import db

app = Quart(__name__)
db = db(AppConfig.DB_NAME, AppConfig.DB_USER, AppConfig.DEBUG)

@app.route('/get_users')
@db.wrapper
async def get_users():
    return dumps(db.all("SELECT name FROM users;"))
```

Contributing
------------

PG-DB is developed on [GitLab](https://gitlab.com/wcorrales/pg-db). You are very welcome to
open [issues](https://gitlab.com/wcorrales/pg-db/issues) or
propose [merge requests](https://gitlab.com/wcorrales/pg-db/merge_requests).

Help
----

This README is the best place to start, after that try opening an
[issue](https://gitlab.com/wcorrales/pg-db/issues).
