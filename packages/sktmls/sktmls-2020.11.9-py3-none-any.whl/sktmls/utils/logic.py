from functools import reduce

import numpy as np


class LogicProcessor:
    """
    상품 선택 로직 등을 프로세스하는 클래스입니다.

    아래 operations를 참조하여 json 형식의 로직을 구현하면 됩니다.
    자세한 사용법에 대한 문서를 추가 예정입니다.
    """

    def __init__(self):
        self.operations = {
            "==": self._soft_equals,
            "===": self._hard_equals,
            "!=": lambda a, b: not self._soft_equals(a, b),
            "!==": lambda a, b: not self._hard_equals(a, b),
            ">": lambda a, b: self._less(b, a),
            ">=": lambda a, b: self._less(b, a) or self._soft_equals(a, b),
            "<": self._less,
            "<=": self._less_or_equal,
            "!": lambda a: not a,
            "!!": bool,
            "%": lambda a, b: a % b,
            "and": lambda *args: reduce(lambda total, arg: total and arg, args, True),
            "or": lambda *args: reduce(lambda total, arg: total or arg, args, False),
            "?:": lambda a, b, c: b if a else c,
            "if": self._if,
            "if_min": self._if_min,
            "if_max": self._if_max,
            "if_closest": self._if_closest,
            "if_closest_upper": self._if_closest_upper,
            "if_closest_lower": self._if_closest_lower,
            "in": lambda a, b: a in b if "__contains__" in dir(b) else False,
            "cat": lambda *args: "".join(str(arg) for arg in args),
            "+": self._plus,
            "*": lambda *args: reduce(lambda total, arg: total * float(arg), args, 1),
            "-": self._minus,
            "/": lambda a, b=None: a if b is None else float(a) / float(b),
            "min": lambda *args: min(args),
            "max": lambda *args: max(args),
            "merge": self._merge,
            "count": lambda *args: sum(1 if a else 0 for a in args),
            "abs": lambda a: abs(a),
            "closest": self._closest,
            "closest_upper": self._closest_upper,
            "closest_lower": self._closest_lower,
            "return": lambda *args: args,
        }

    def _if(self, *args):
        for i in range(0, len(args) - 1, 2):
            if args[i]:
                return args[i + 1]
        if len(args) % 2:
            return args[-1]
        else:
            return None

    def _if_min(self, *args):
        min_arg = np.argmin([args[i] for i in range(0, len(args) - 1, 2)])
        return args[min_arg * 2 + 1]

    def _if_max(self, *args):
        max_arg = np.argmax([args[i] for i in range(0, len(args) - 1, 2)])
        return args[max_arg * 2 + 1]

    def _if_closest(self, arg, *comps):
        args = list(comps)
        for i in range(0, len(args) - 1, 2):
            args[i] = abs(arg - args[i])
        return self._if_min(*args)

    def _if_closest_upper(self, arg, *comps):
        args = []
        for i in range(0, len(comps) - 1, 2):
            if comps[i] > arg:
                args.append(comps[i])
                args.append(comps[i + 1])
        if not args:
            return None
        return self._if_closest(arg, *args)

    def _if_closest_lower(self, arg, *comps):
        args = []
        for i in range(0, len(comps) - 1, 2):
            if comps[i] < arg:
                args.append(comps[i])
                args.append(comps[i + 1])
        if not args:
            return None
        return self._if_closest(arg, *args)

    def _soft_equals(self, a, b):
        if isinstance(a, str) or isinstance(b, str):
            return str(a) == str(b)
        if isinstance(a, bool) or isinstance(b, bool):
            return bool(a) is bool(b)
        return a == b

    def _hard_equals(self, a, b):
        if type(a) != type(b):
            return False
        return a == b

    def _less(self, a, b, *args):
        types = set([type(a), type(b)])
        if float in types or int in types:
            try:
                a, b = float(a), float(b)
            except TypeError:
                return False
        return a < b and (not args or self._less(b, *args))

    def _less_or_equal(self, a, b, *args):
        return (self._less(a, b) or self._soft_equals(a, b)) and (not args or self._less_or_equal(b, *args))

    def _to_numeric(self, arg):
        if isinstance(arg, str):
            if "." in arg:
                return float(arg)
            else:
                return int(arg)
        return arg

    def _plus(self, *args):
        return sum(self._to_numeric(arg) for arg in args)

    def _minus(self, *args):
        if len(args) == 1:
            return -self._to_numeric(args[0])
        return self._to_numeric(args[0]) - self._to_numeric(args[1])

    def _closest(self, arg, *comps):
        closest = comps[0]
        min_diff = abs(arg - comps[0])
        for i in range(1, len(comps)):
            diff = abs(arg - comps[i])
            if min_diff > diff:
                min_diff = diff
                closest = comps[i]
        return closest

    def _closest_upper(self, arg, *comps):
        args = [c for c in comps if c > arg]
        if not args:
            return None
        return self._closest(arg, *args)

    def _closest_lower(self, arg, *comps):
        args = [c for c in comps if c < arg]
        if not args:
            return None
        return self._closest(arg, *args)

    def _merge(self, *args):
        ret = []
        for arg in args:
            if isinstance(arg, list) or isinstance(arg, tuple):
                ret += list(arg)
            else:
                ret.append(arg)
        return ret

    def _get_var(self, data, var_name, not_found=None):
        try:
            for key in str(var_name).split("."):
                try:
                    data = data[key]
                except TypeError:
                    data = data[int(key)]
        except (KeyError, TypeError, ValueError):
            return not_found
        else:
            return data

    def _missing(self, data, *args):
        not_found = object()
        if args and isinstance(args[0], list):
            args = args[0]
        ret = []
        for arg in args:
            if self._get_var(data, arg, not_found) is not_found:
                ret.append(arg)
        return ret

    def _missing_some(self, data, min_required, args):
        if min_required < 1:
            return []
        found = 0
        not_found = object()
        ret = []
        for arg in args:
            if self._get_var(data, arg, not_found) is not_found:
                ret.append(arg)
            else:
                found += 1
                if found >= min_required:
                    return []
        return ret

    def apply(self, tests, data=None):
        """
        ## Args

        - tests: (dict) 테스트 할 json 형식의 로직
        - data: (optional) (dict) 로직에서 참조할 데이터 dict (기본값: None)
        """
        if tests is None or not isinstance(tests, dict):
            return tests

        operator = list(tests.keys())[0]
        data = data or {}
        values = tests[operator]

        if not isinstance(values, list) and not isinstance(values, tuple):
            values = [values]

        values = [self.apply(val, data) for val in values]

        if operator == "var":
            return self._get_var(data, *values)
        if operator == "missing":
            return self._missing(data, *values)
        if operator == "missing_some":
            return self._missing_some(data, *values)

        if operator not in self.operations:
            raise ValueError("없는 operator입니다. %s" % operator)

        return self.operations[operator](*values)
