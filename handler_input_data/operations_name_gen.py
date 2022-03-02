import math
import sympy
import keyword

"""

This script generates names for math functions, that can be used in input functions. /
Also generates forbidden worlds for variable's names.

"""

math_functions = {
    k: v for k, v in math.__dict__.items() if not k.startswith("__") and not
    (k == 'nan' or k == 'inf')
}
sympy_functions = {
    k: v for k, v in sympy.__dict__.items() if not k.startswith("__") and
                                               type(v) == sympy.core.function.FunctionClass
}

allowed_operations = list(set(math_functions.keys()) & set(sympy_functions.keys())) + ['pi', 'e', 'sqrt']
forbidden_names_for_variables = keyword.kwlist + allowed_operations
