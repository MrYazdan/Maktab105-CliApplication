from importlib import import_module
from typing import Callable, Any

from core.state import RouteSateManager
from core.utils import banner


class Callback:
    # def __init__(self, _callable: Callable) -> None:
    #     assert callable(_callable), "_callable must be callable !"
    #     self.callable = _callable
    #

    def __init__(self, package: str, _callable: str):
        self.callable = getattr(import_module(package), _callable)

    def __call__(self, *args, **kwargs) -> Any:
        return self.callable(*args, **kwargs)


class Route:
    def __init__(self, name: str,
                 description: str | None = None,
                 children: list | None = None,
                 callback=None,
                 condition=lambda: True,
                 ) -> None:
        self.parent = None
        self.children = None

        self.name = name
        self.description = description
        self.callback = callback
        self.condition = condition

        children and self._set_parent(children)

    def _set_parent(self, children):
        for child in children:
            child.parent = self

        self.children = children

    def _get_route(self):
        try:
            banner(RouteSateManager.get_current_route())
            print(self.description or "", end="\n\n")

            if children := [child for child in self.children if child.condition()]:
                # submenu:
                for child in children:
                    print(f"\t{children.index(child) + 1}. {child.name}")
                print(f"\n\t0. " + ("Exit" if not self.parent else f"Back to {self.parent.name}"))

                index = int(input("\n> ")) - 1
                route = children[index] if index != -1 else self.parent

                if not route:
                    banner("Exit")

                    if input("Do you want to exit ? [y|N]").strip().lower()[0] == "y":
                        print("Bye Bye ...\n☆*: .｡. o(≧▽≦)o .｡.:*☆")
                        exit()
                    else:
                        self()
                return route
            else:
                return self
        except (ValueError, KeyboardInterrupt, IndexError):
            banner("Error")
            input("Please enter valid item\n\nPress enter to continue ...")
            self()

    def __call__(self, *args, **kwargs):
        RouteSateManager.add_route(self.name)

        route = self._get_route()

        if self.parent == route:
            RouteSateManager.delete_last_route()
            route()

        elif route.children:
            route()

        else:
            try:
                banner(route.name)
                route.description and print(route.description, "\n\n")

                route.callback and route.callback(route)
            except Exception as e:
                banner("Error")

            input("\nPress enter to continue ... ")
            RouteSateManager.delete_last_route()
            route.parent()


class Router:
    def __init__(self, route):
        self.route = route
        RouteSateManager.add_route(route.name)

    def __call__(self, *args, **kwargs):
        self.route()
