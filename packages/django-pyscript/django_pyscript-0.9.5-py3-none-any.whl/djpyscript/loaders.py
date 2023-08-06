import importlib.abc


class StringLoader(importlib.abc.SourceLoader):
    """ A custom StringLoader, that fakes a source loader
    """

    def __init__(self, data):
        self.data = data

    def get_source(self, fullname):
        return self.data

    def get_source(self, fullname):
        return self.data
    
    def get_data(self, path):
        return self.data
    
    def get_filename(self, fullname):
        return "<not a real path>/" + fullname + ".py"
