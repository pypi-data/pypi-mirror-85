from typing import List

from django.db.models import FileField

from .fieldfiles import PyScriptFieldFile


class PyScriptField(FileField):
    """Custom FileField that can store a python script file and executes it by leveraging a custom FieldFile"""
    attr_class = PyScriptFieldFile

    def __init__(self, injected_parameters: List[str] = None, parameter_field: str = None, *args, **kwargs):
        if injected_parameters is None:
            injected_parameters = []

        self.parameter_field = parameter_field
        self.injected_parameters = injected_parameters
        super().__init__(*args, **kwargs)
