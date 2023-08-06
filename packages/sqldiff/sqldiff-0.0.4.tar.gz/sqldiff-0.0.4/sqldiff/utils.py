def make_tuple(obj):
    """
    Converts param object to tuple considering if the provided object is iterable.
    :param obj: Any iterable or non-iterable argument
    :return: tuple(obj) if param is iterable, (param,) otherwise [one element tuple with obj param as an element]
    """
    try:
        iter(obj)
        if isinstance(obj, str):
            obj_tuple = (obj,)
        else:
            obj_tuple = tuple(obj)
    except TypeError:
        obj_tuple = (obj,)
    return obj_tuple

