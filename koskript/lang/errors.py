class Errors:
    class MismatchType(Exception):
        def __init__(self, *args):
            super().__init__(*args)
    
    class ProtectedValue(Exception):
        def __init__(self, *args):
            super().__init__(*args)

    class RuntimeError(Exception):
        def __init__(self, *args):
            super().__init__(*args)