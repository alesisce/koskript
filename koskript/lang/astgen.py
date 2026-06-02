from lark import Transformer
from .emtypes import *

class KoskriptTransformer(Transformer):
    def start(self, tree): return (tree)

    def NUMBER(self, token): return IntLit(value=int(token))
    def NAME(self, token): return NameRef(name=str(token))
    def STRING(self, token): return StrLit(value=token[1:-1])
    def bool_true(self, tree): return BoolLit(value=True)
    def bool_false(self, tree): return BoolLit(value=False)

    def inttype(self, tree): return ValueType.INTEGER
    def strtype(self, tree): return ValueType.STRING
    def booltype(self, tree): return ValueType.BOOL
    def arraytype(self, tree): return ValueType.ARRAY
    def maptype(self, tree): return ValueType.MAP

    def array(self, tree): return ArrayLit(value=tree)
    def map(self, tree): return MapLit(value=tree)
    def map_obj(self, tree): return MapValue(key=tree[0], value=tree[1])

    def arg_list(self, tree): return tree

    def add_stmt(self, tree):
        left, right = tree
        return AddStmt(left=left, right=right)
    
    def sub_stmt(self, tree):
        left, right = tree
        return SubStmt(left=left, right=right)
    
    def mul_stmt(self, tree):
        left, right = tree
        return MulStmt(left=left, right=right)
    
    def div_stmt(self, tree):
        left, right = tree
        return DivStmt(left=left, right=right)

    def param_list(self, tree):
        res = []
        for i in tree:
            res.append(Param(t=i[0], name=i[1]))
        return res
    
    def param(self, tree):
        return [tree[0], tree[1]]
    
    def block(self, tree):
        return tree
    
    # conditions and comparisons
    def and_cond(self, tree):
        right, left = tree
        return AndCond(left=left, right=right)
    
    def not_cond(self, tree):
        return NotCond(tree)
    
    def or_cond(self, tree):
        right, left = tree
        return OrCond(left=left, right=right)


    def equ(self, tree):
        left, right = tree
        return EquComp(left=left, right=right)
    def nequ(self, tree):
        left, right = tree
        return NequComp(left=left, right=right)
    def gte(self, tree):
        left, right = tree
        return GteComp(left=left, right=right)
    def lte(self, tree):
        left, right = tree
        return LteComp(left=left, right=right)
    def lt(self, tree):
        left, right = tree
        return LtComp(left=left, right=right)
    def gt(self, tree):
        left, right = tree
        return GtComp(left=left, right=right)
    
    def member_access(self, tree):
        attrs = tree[1:]
        if not attrs:
            return tree[0]

        return MemberAccess(name=tree[0], attrs=tree[1:])

    def if_stmt(self, tree):
        condition = tree[0]
        block = tree[1]
        anexed_ifs = tree[2:]

        return IfStmt(
            condition=condition,
            body=block,
            if_tree=anexed_ifs
        )
    
    def elseif_stmt(self, tree):
        condition, block = tree
        return ElseIfStmt(
            condition=condition,
            body=block
        )

    def elsestmt(self, tree):
        return ElseStmt(
            body=tree[0]
        )

    # declarations
    def local_decl(self, tree):
        t, name, expr = tree

        return LocalDecl(
            t=t,
            name=name.name, 
            value=expr
        )

    def decl(self, tree):
        name, expr = tree
        return DeclStmt(
            name=name.name, value=expr
        )

    def fn_def(self, tree):
        t, name, params, block = tree
        return FnDef(
            t=t,
            name=name.name,
            params=params,
            body=block
        )
    
    def fn_def_nargs(self, tree):
        t, name, block = tree
        return FnDef(
            t=t,
            name=name.name,
            params=[],
            body=block
        )

    # flow
    def return_stmt(self, tree):
        if len(tree) >= 1:
            return ReturnStmt(value=tree[0])
        return ReturnStmt(value=None)
    
    def while_stmt(self, tree):
        condition, block = tree
        return WhileStmt(condition=condition, body=block)
    
    def for_stmt(self, tree):
        vartype, varname, iterable, block = tree
        return ForStmt(t=vartype, var=varname.name, iterable=iterable.name, body=block)
    
    def foritem_stmt(self, tree):
        keytype, key, valuetype, value, iterable, block = tree
        return ForItemStmt(kt=keytype, key=key.name, vt=valuetype, var=value.name, iterable=iterable.name, body=block)
    
    # Otros
    def fn_call(self, tree):
        name = tree[0]
        args = tree[1] if len(tree) > 1 else []
        return FnCall(name=name, args=args)