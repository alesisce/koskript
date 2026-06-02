from collections import namedtuple
from enum import Enum
from .errors import Errors

class ValueType(Enum):
    STRING = 0
    INTEGER = 1
    BOOL = 2
    ARRAY = 3
    MAP = 4

class ObjectType(Enum):
    FN = 0
    PYFN = 1

class KoskriptValue(object):
    def __init__(self, type_: ValueType, value = None):
        self.type = type_
        self.value = value
        
        self.readonly = False
        self._TYPE_MAP = {
            ValueType.STRING:  str,
            ValueType.INTEGER: int,
            ValueType.BOOL:    bool,
            ValueType.ARRAY: list,
            ValueType.MAP: dict
        }

    def __repr__(self):
        return f"KoskriptValue({self.type.value}, {self.value!r}, readonly={self.readonly})"

    def set_value(self, value, force=False):
        if self.value is None:
            self.value = value

        if self.readonly and not force:
            raise Errors.ProtectedValue("value is protected, cannot be modified directly.")
        
        expected = self._TYPE_MAP.get(self.type)
        if expected is None:
            raise Errors.RuntimeError("failed, type does not match with compatible types.")
        if not isinstance(value, expected):
            raise Errors.MismatchType(f"type mismatch, expected {self.type}.")

        self.value = value

class KoskriptObject(object):
    def __init__(self, returntype: ValueType = None, type: ObjectType = ObjectType.FN, params: list = [], value = []):
        self.type = type
        self.params = params
        self.value = value
        self.returntype = returntype
    
    def __repr__(self):
        return f"KoskriptObject(type={self.returntype}, {self.type}, {self.params}, {self.value!r})"

# Literals and references
IntLit = namedtuple("IntLit", ["value"])
StrLit = namedtuple("StrLit", ["value"])
BoolLit = namedtuple("BoolLit", ["value"])
ArrayLit = namedtuple("ArrayLit", ["value"])
MapLit = namedtuple("MapLit", ["value"])
MapValue = namedtuple("MapValue", ["key", "value"])
NameRef = namedtuple("NameRef", ["name"])
MemberAccess = namedtuple("MemberAccess", ["name", "attrs"])

# Node Objects
LocalDecl = namedtuple("LocalDecl", ["t", "name", "value"])
DeclStmt = namedtuple("DeclStmt", ["name", "value"])
ReturnStmt = namedtuple("ReturnStmt", ["value"])
FnDef  = namedtuple("FnDef",  ["t", "name", "params", "body"])
Param = namedtuple("Param", ["t", "name"])
FnCall = namedtuple("FnCall", ["name", "args"])
WhileStmt   = namedtuple("WhileStmt",   ["condition", "body"])
ForStmt     = namedtuple("ForStmt",     ["t", "var", "iterable", "body"])
ForItemStmt = namedtuple("ForItemStmt", ["kt", "key", "vt", "var", "iterable", "body"])
AddStmt = namedtuple("AddStmt", ["left", "right"])
SubStmt = namedtuple("SubStmt", ["left", "right"])
MulStmt = namedtuple("MulStmt", ["left", "right"])
DivStmt = namedtuple("DivStmt", ["left", "right"])
IfStmt = namedtuple("IfStmt", ["condition", "body", "if_tree"])
ElseIfStmt = namedtuple("ElseIfStmt", ["condition", "body"])
ElseStmt = namedtuple("ElseStmt", ["body"])

# Conditions
AndCond = namedtuple("AndCond", ["left", "right"])
OrCond = namedtuple("OrCond", ["left", "right"])
NotCond = namedtuple("NotCond", ["comparison"])

# Comparisons
EquComp = namedtuple("EquComp", ["left", "right"])
NequComp = namedtuple("NequComp", ["left", "right"])
LteComp = namedtuple("LteComp", ["left", "right"])
GteComp = namedtuple("GteComp", ["left", "right"])
LtComp = namedtuple("LtComp", ["left", "right"])
GtComp = namedtuple("GtComp", ["left", "right"])
