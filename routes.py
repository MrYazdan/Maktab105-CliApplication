from core.router import Router, Route, Callback
from admin.state import StateManager as AdminStateManager


def simple(route):
    pass


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
