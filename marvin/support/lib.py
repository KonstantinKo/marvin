"""
    A junk drawer for reusable convenience methods.

    Let's keep this as small as possible.
"""

def flatten(iterable):
    """
        Flatten a 2-dimensional list without touching strings.
        Why doesn't python have this internally?
    """
    output_array = []

    for item in iterable:
        if isinstance(item, list):
            for subitem in flatten(item):
                output_array.append(subitem)
        else:
            output_array.append(item)

    return output_array
