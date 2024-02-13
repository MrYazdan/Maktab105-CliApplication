# :book: Maktab105 Advanced Python Cli Course Repository

> Memory: Teaching Python Bootcamp (cli crash course) - maktab-105 - [maktab sharif academy](https://maktabsharif.ir)

---

##### ⚡ Routing - `routes.py`:
```python
router = Router(
    Route("Main", description="Maktab Store - cli project", children=[
        Route("Login", description="login to an account -- description",
              callback=Callback('admin.callbacks', 'login'),
              condition=lambda: not AdminStateManager.get_user()),
        Route("Register", callback=Callback('admin.callbacks', 'register'),
              condition=lambda: not AdminStateManager.get_user()),
        Route("Admin Panel", children=[
            Route("Register Product", callback=simple),
            Route("Sub Panel", children=[
                Route("Register Product", callback=simple),
            ])
        ]),
        Route("All products", callback=simple),
        Route("Logout", callback=Callback('admin.callbacks', 'logout'), condition=AdminStateManager.get_user),
    ])
)
```

##### ♻️ Lifecycles with hooks - `main.py`:
```python
import atexit
import signal
import models

from routes import router
from core.hook import Hook
from core.store import DataBase
from core.lifecycle import Lifecycle

if __name__ == '__main__':
    # Database
    db = DataBase("db.bin")
    db.register(models.User)

    # Signal => interceptor terminate
    signal.signal(signal.SIGTERM, lambda signum, frame: db.save())

    # Exit:
    atexit.register(db.save)

    # Hooks:
    Hook.register([
        Hook(Hook.MODE.INITIAL, db.load),
        Hook(Hook.MODE.FINISH, db.save),
    ])

    # Lifecycle
    with Lifecycle(Hook.registered) as lifecycle:
        router()
```
