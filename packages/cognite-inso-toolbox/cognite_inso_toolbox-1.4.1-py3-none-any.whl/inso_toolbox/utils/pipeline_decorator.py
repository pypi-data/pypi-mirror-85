import inspect
from functools import partial, wraps


def pipeline_function(func):
    """
    Method that makes a function suitable for being used in the Pipeline class.
    The first argument of func must be data: pd.DataFrame.
    This method should be used as a decorator.
    """
    # The first argument of func must be data: pd.DataFrame (set convention in inso-toolbox)
    arguments = inspect.getfullargspec(func).args
    if len(arguments) == 0 or arguments[0] != "data":
        raise TypeError(
            "The first argument of "
            + func.__name__
            + " must be 'data: pd.Dataframe' to be suitable for becoming a pipeline function.\n"
            + "Either remove @pipeline_function decorator or make 'data: pd.Dataframe' the first argument."
        )

    # Set original arguments and docstring
    @wraps(func)
    # Edit behaviour of function based on whether it is used as a function call or for piping
    def piped_function(*args, **kwargs):
        # Return function output if arguments are used or data is passed in
        if len(args) > 0 or "data" in kwargs:
            return func(*args, **kwargs)

        # Otherwise return a function with stored keyword arguments
        else:
            # Check for any invalid keywords (not done automatically by partial)
            invalid_keywords = set(kwargs.keys()).difference(set(arguments))
            if len(invalid_keywords) > 0:
                raise TypeError(
                    func.__name__
                    + " got unexpected keyword arguments: "
                    + ", ".join(str(keyword) for keyword in invalid_keywords)
                )
            # Return function with stored keyword arguments
            return partial(func, **kwargs)

    return piped_function
