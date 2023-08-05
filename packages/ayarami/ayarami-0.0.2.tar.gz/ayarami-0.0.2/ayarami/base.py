from typing import Union, Dict, Any
from types import ModuleType

DEFAULT_SETTINGS_NAME = "_default"


class Settings:
    _instances: Dict[str, "Settings"] = {}
    __slots__ = (
        "_name",
        "_registry",
    )

    @classmethod
    def get_instance(cls, name: str) -> "Settings":
        if name == DEFAULT_SETTINGS_NAME and name not in cls._instances:
            cls(DEFAULT_SETTINGS_NAME)
        return cls._instances[name]

    @classmethod
    def del_instance(cls, name: str):
        if name == DEFAULT_SETTINGS_NAME:
            raise ValueError("Default settings object cannot be deleted. Please use clear method.")
        instance = cls._instances.pop(name)
        del instance

    @classmethod
    def set_instance(cls, instance: "Settings"):
        if instance._name in cls._instances:
            raise ValueError("name is not unique")
        cls._instances[instance._name] = instance

    def __init__(self, name: str = DEFAULT_SETTINGS_NAME):
        self._name = name
        self._registry = {}
        self.set_instance(self)

    def configure(self, module: Union[str, ModuleType]):
        if isinstance(module, str):
            import importlib
            real_module = importlib.import_module(module)
        elif isinstance(module, ModuleType):
            real_module = module
        else:
            raise ValueError("module argument must be either a module or an importable string value of a module")

        for variable in dir(real_module):
            if not variable.startswith("_") and variable.upper() == variable:
                self._registry[variable] = getattr(real_module, variable)

    def __getattr__(self, item: str) -> Any:
        if not self._registry:
            raise ValueError("Settings object is not configured.")
        return self._registry[item]

    def clear(self):
        self._registry = {}
