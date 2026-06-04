import sys
import os

from pair import *
from scheme_utils import *
from ucb import main, trace
from typing import cast
from scheme_classes import MacroProcedure

import scheme_forms

##############
# Eval/Apply #
##############


def scheme_eval(expr: str | Pair, env: Frame, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):
        assert isinstance(expr, str)
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError("malformed list: {0}".format(repl_str(expr)))
    first, rest = expr.first, expr.rest # type: ignore
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        proc = scheme_eval(first, env)
        if isinstance(proc, MacroProcedure):
            result_expr = eval_all(proc.body, proc.env.make_child_frame(proc.formals, rest))
            if isinstance(result_expr, Unevaluated):
                result_expr = scheme_eval(result_expr.expr, result_expr.env)
            return scheme_eval(result_expr, env)
        return scheme_apply(proc, rest.map(lambda x: scheme_eval(x, env)), env) # type: ignore
        # END PROBLEM 3


def scheme_apply(procedure: Procedure, args: Pair, env: Frame):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        lst = []
        while args is not nil:
            lst.append(args.first)
            args = args.rest
        if procedure.expect_env:
            lst.append(env)
        try:
            return procedure.py_func(*lst)
        except TypeError:
            raise SchemeError("incorrect number of arguments")
        # END PROBLEM 2
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        return eval_all(procedure.body, procedure.env.make_child_frame(procedure.formals, args))
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        return eval_all(procedure.body, env.make_child_frame(procedure.formals, args))
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)


def eval_all(expressions: Pair, env: Frame):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    expr = expressions
    result = None
    while expr is not nil:
        if expr.rest is nil:
            result = scheme_eval(expr.first, env, True)
        else:
            result = scheme_eval(expr.first, env)
        expr = expr.rest
    return result
    # END PROBLEM 6


##################
# Tail Recursion #
##################


class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env


def optimize_tail_calls(original_scheme_eval):
    """Return a properly tail recursive version of an eval function."""

    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        # BEGIN PROBLEM EC
        result = original_scheme_eval(expr, env)
        while isinstance(result, Unevaluated):
            result = original_scheme_eval(result.expr, result.env)
        return result
        # END PROBLEM EC

    return optimized_eval


################################################################
# Uncomment the following line to apply tail call optimization #
################################################################
scheme_eval = optimize_tail_calls(scheme_eval) # type: ignore
