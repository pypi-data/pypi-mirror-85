import importlib.abc
import importlib.util
import inspect
from contextlib import suppress
from importlib.util import module_from_spec, spec_from_loader

from django.db.models.fields.files import FieldFile

from .loaders import StringLoader
from .extraction import cast_parameters, update_parameters


class PyScriptFieldFile(FieldFile):
    def __init__(self, instance, field, name):
        super().__init__(instance, field, name)
        self.initialize_internal()

    def initialize_internal(self):
        # This method has to be called by every other method, because it is non deterministic when
        # exactly the file will be uploaded and therefore when the module will be accessable
        if hasattr(self, "_module") and hasattr(self, "_callable") and hasattr(self, "_parameters"):
            return

        with suppress(FileNotFoundError, ValueError, Exception):
            self._module, self._callable = self.import_script()
            self._parameters = getattr(self.instance, self.field.parameter_field) if self.field.parameter_field else {}

    def import_script(self):
        # Imports the script and returns the module and the module's callable
        spec = spec_from_loader(self.name.split(".")[0], StringLoader(self.file.read()))
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module, module._CALLABLE

    def run_script(self, **injected_parameters):
        # Runs the script and injects the parameters, in case there any from the parameter field
        # As well as the paramters passed in through the injected_keyworks arguments
        self.initialize_internal()

        injected_parameters.update(self.get_casted_parameters())
        return self._callable(**injected_parameters)

    def run_script_with_handler(self, handler, **kwargs):
        """Runs an arbitrary handler of the stored module with some kwargs"""
        self.initialize_internal()
        return getattr(self._module, handler)(**kwargs)

    def extract_parameters(self):
        self.initialize_internal()
        parameter_field = getattr(self.instance, self.field.parameter_field)
        return update_parameters(self._callable, parameter_field, self.field.injected_parameters)

    def get_casted_parameters(self):
        self.initialize_internal()
        parameter_field = getattr(self.instance, self.field.parameter_field)
        return dict(cast_parameters(self._callable, parameter_field))
