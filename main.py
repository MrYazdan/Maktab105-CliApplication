import atexit
import signal

from core.hook import Hook
from core.store import DataBase
from core.lifecycle import Lifecycle
import models


def bye(*args, **kwargs):
    print("Bye Bye !")


# Exit:
atexit.register(bye)

# Signal => interceptor terminate
signal.signal(signal.SIGTERM, bye)

# Database
db = DataBase("db.bin")
db.register(models.User)

# Hooks:
Hook.register([
    Hook(Hook.MODE.INITIAL, db.load),
    Hook(Hook.MODE.FINISH, db.save),
])

# Lifecycle
with Lifecycle(Hook.registered) as lifecycle:
    print("Welcome to my application :\n")

    # models.User('fardin_zand', "1234567")
    # models.User('amirasdsli', "1234567")
    # models.User('hoseinsds', "1234567")
    # models.User('zahra23a', "1234567")
    # models.User('fatemeh_rr44', "1234567")
    # models.User("mryazdan_78", "ryrtruri")

    for i, u in enumerate(models.User.STORE):
        print(f"{i+1}: {u.profile()}")

    print()
