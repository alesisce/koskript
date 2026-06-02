from .emtypes import *

class KoskripInterpreter(object):
    def __init__(self):
        self.globals = {"_": {}}
        self.scopes = []
        self._handlers = {
            LocalDecl:   self._local_decl,
            DeclStmt: self._decl,
            FnDef:       self._fn_def,
            FnCall:      self._fn_call,
            ReturnStmt:  self._return_stmt,
            WhileStmt:   self._while_stmt,
            ForStmt:     self._for_stmt,
            ForItemStmt: self._foritem_stmt,
            IfStmt: self._if_stmt,
            ElseIfStmt: self._else_if_stmt,
            ElseStmt: self._else_stmt
        }
        self.types = {
            ValueType.INTEGER: int,
            ValueType.STRING: str,
            ValueType.BOOL: bool,
            ValueType.ARRAY: list, 
            ValueType.MAP: dict
        }
    
    def execute(self, ast: list):
        for node in ast:
            value = self.visit(node)
            if value: return value

    def get_global(self, name: str) -> KoskriptValue | KoskriptObject:
        for scope in reversed(self.scopes):
            if scope in self.globals and name in self.globals[scope]:
                return self.globals[scope][name]
        
        if name in self.globals["_"]:
            return self.globals["_"][name]
        
        raise NameError(f"'{name}' is not defined")

    def set_global(self, name: str, value: KoskriptValue | KoskriptObject) -> None:
        if self.scopes:
            scope = self.scopes[-1]
            if scope not in self.globals:
                self.globals[scope] = {}
            self.globals[scope][name] = value
            return
        
        self.globals["_"][name] = value

    def visit(self, node):
        handler = self._handlers.get(type(node))
        if handler is None:
            raise RuntimeError(f"Unknown node: {type(node).__name__}")
        return handler(node)

    # EVALUATORS ####################################################################

    def expr_eval(self, expr):
        match expr:
            case IntLit(value):  return value
            case StrLit(value):  return value
            case BoolLit(value): return value
            case NameRef(name):  return self.get_global(name).value
            case AddStmt(l, r):  return self.expr_eval(l) + self.expr_eval(r)
            case SubStmt(l, r):  return self.expr_eval(l) - self.expr_eval(r)
            case MulStmt(l, r):  return self.expr_eval(l) * self.expr_eval(r)
            case DivStmt(l, r):  return self.expr_eval(l) / self.expr_eval(r)
            case ArrayLit(array): return [self.expr_eval(i) for i in array]

            case MapValue(key, value): return key, value
            case MapLit(values):
                res = {}
                for val in values:
                    res[self.expr_eval(val.key)] = self.expr_eval(val.value)
                return res

            case MemberAccess(name, attrs):
                value = self.expr_eval(name)

                if not isinstance(value, self.types.get(ValueType.MAP)):
                    raise Errors.MismatchType(f"member access only supported on map, got {value}")
                
                for attr in attrs:
                    try:
                        value = value[attr.name]
                    except:
                        raise Errors.RuntimeError(f"no member with the value {attr} is defined on {value}")

                return value
                
            case FnCall(n, arg): return self.fn_eval(n, arg)
            case _: raise RuntimeError(f"Unknown expr: {type(expr).__name__}")

    def fn_eval(self, name, args):
        if type(name) != MemberAccess:
            func: KoskriptObject = self.get_global(name)
        else:
            func: KoskriptObject = self.expr_eval(name)

        if not func:
            raise NameError(f"no define with the name {name} exists.")
        
        func_type: ObjectType = func.type
        func_return: ValueType = func.returntype
        func_params: list[Param] = func.params
        func_body = func.value

        if func_type == ObjectType.PYFN:
            return func_body(*[self.expr_eval(arg) for arg in args])

        self.scopes.append(f"{name}_func")
        for numparam, param in enumerate(func_params):
            value = KoskriptValue(param.t)
            value.set_value(self.expr_eval(args[numparam]))
            value.readonly = True

            self.set_global(param.name.name, value)

        status = self.execute(func_body)
        self.scopes.pop()
        return status
    
    def cond_eval(self, condition):
        match condition:
            case EquComp(l, r): return self.expr_eval(l) == self.expr_eval(r)
            case NequComp(l, r): return self.expr_eval(l) != self.expr_eval(r)
            case LteComp(l, r): return self.expr_eval(l) <= self.expr_eval(r)
            case GteComp(l, r): return self.expr_eval(l) >= self.expr_eval(r)
            case GtComp(l, r): return self.expr_eval(l) > self.expr_eval(r)
            case LtComp(l, r): return self.expr_eval(l) < self.expr_eval(r)

            case AndCond(l, r): return self.cond_eval(l) and self.cond_eval(r)
            case OrCond(l, r): return self.cond_eval(l) or self.cond_eval(r)

            case NotCond(com): return True if self.cond_eval(com[0]) == False else False
    

    # HANDLERS ######################################################################
    
    def _local_decl(self, node: LocalDecl):
        value = self.expr_eval(node.value)
        decltype = node.t
        name = node.name

        if not isinstance(value, self.types.get(decltype)):
            raise ValueError(f"expected type '{decltype}' on variable {name}")

        self.set_global(
            name,
            KoskriptValue(
                decltype,
                value
            )
        )


    def _decl(self, node: DeclStmt):
        variable = self.get_global(node.name)

        if not variable:
            raise NameError(f"{node.name} is not declared.")

        variable.set_value(self.expr_eval(node.value))

    def _fn_def(self, node: FnDef):
        self.set_global(
            name=node.name,
            value=KoskriptObject(
                returntype=node.t,
                type=ObjectType.FN,
                params=node.params,
                value=node.body
            )
        )

    def _fn_call(self, node: FnCall):
        return self.fn_eval(node.name, args=node.args)

    def _return_stmt(self, node: ReturnStmt):
        return self.expr_eval(node.value)

    def _while_stmt(self, node: WhileStmt):
        while self.cond_eval(node.condition):
            self.execute(node.body)

    def _for_stmt(self, node: ForStmt):
        array_variable = self.get_global(node.iterable)

        if not array_variable:
            raise NameError(f"{array_variable} is not declared.")
        
        if not array_variable.type == ValueType.ARRAY:
            raise ValueError(f"{array_variable} is not an array.")

        self.scopes.append(f"for_{node.iterable}")
        var = KoskriptValue(node.t)
        var.readonly = True
        self.set_global(node.var, var)


        array_value = iter(array_variable.value)
        while True:
            try:
                value = next(array_value)

                variable = self.get_global(node.var)
                variable.set_value(value=value, force=True)

                self.execute(node.body)
            except StopIteration:
                break
        
        self.scopes.pop()
        
    def _foritem_stmt(self, node: ForItemStmt):
        map_variable = self.get_global(node.iterable)

        if not map_variable:
            raise NameError(f"{map_variable} is not declared.")
        
        if not map_variable.type == ValueType.MAP:
            raise ValueError(f"{map_variable} is not a map.")

        self.scopes.append(f"foreach_{node.iterable}")
        keyvalue = KoskriptValue(node.kt)
        varvalue = KoskriptValue(node.vt)

        keyvalue.readonly = True
        varvalue.readonly = True

        self.set_global(node.key, keyvalue)
        self.set_global(node.var, varvalue)

        map_variable_value = iter(map_variable.value.items())

        while True:
            try:
                value = next(map_variable_value)
                kval = self.get_global(node.key)
                vval = self.get_global(node.var)

                kval.set_value(value[0], force=True)
                vval.set_value(value[1], force=True)

                self.execute(node.body)

            except StopIteration:
                break
        
        self.scopes.pop()
    
    def _if_stmt(self, node: IfStmt):
        condition = self.cond_eval(node.condition)

        if condition:
            self.execute(node.body)
            return   

        for obj in node.if_tree:
            if type(obj) == ElseIfStmt:
                res = self._else_if_stmt(obj)
                if res:
                    break
            else:
                self._else_stmt(obj)
                break

    def _else_if_stmt(self, node: ElseIfStmt):
        condition = self.cond_eval(node.condition)
        
        if not condition:
            return False
    
        self.execute(node.body)
        return True
    
    def _else_stmt(self, node: ElseStmt):
        self.execute(node.body)