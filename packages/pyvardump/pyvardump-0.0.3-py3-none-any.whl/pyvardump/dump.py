"""
This is the main code
"""
import json
import sys
from pprint import pprint


def dump_print(obj):
    print(obj)


def dump_pprint(obj):
    pprint(obj)


def dump_obj(obj, level=0):
    try:
        for a in dir(obj):
            # print(a)
            if a.startswith("_"):
                continue
            if a in {"adjustments", "auto_shape_type"}:
                continue
            val = getattr(obj, a)
            # print(type(val))
            if type(val) in {int, float, str, list, dict, set}:
                print(level*' ', val)
            else:
                dump_obj(val, level=level+1)
    except TypeError:
        print(str(type(obj)))
    except AttributeError:
        print(str(type(obj)))


def dump_obj_2(obj, level=0):
    if hasattr(obj, '__dict__'):
        for key, value in obj.__dict__.items():
            if isinstance(value, (int, float, str, list, dict, set)):
                print(" " * level + "%s -> %s" % (key, value))
            else:
                dump_obj_2(value, level + 2)


def default_func(obj):
    try:
        return dir(obj)
        # return obj.__dict__
    except TypeError:
        return str(type(obj))
    except AttributeError:
        return str(type(obj))


def dump_json(obj):
    # json.dump(obj, fp=sys.stdout, indent=2, default=default_func)
    json.dump(obj, fp=sys.stdout, indent=2)


def object_to_members_or_string(obj):
    try:
        if hasattr(obj, "__dict__"):
            return vars(obj)
        return str(obj)
    except TypeError:
        return str(obj)


def flat_dump(obj) -> None:
    """
    Dump object to stdout. Only dumps the immediate members of the object
    :param obj:
    """
    print("===========start dump=======")
    try:
        for x in dir(obj):
            if x.startswith("_"):
                continue
            try:
                v = getattr(obj, x)
            except AttributeError:
                v = "AttributeError"
            print(f"{x} -> {v}")
    except TypeError:
        print("Cannot flat_dump")

