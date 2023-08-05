from typing import Callable, Dict, List, Optional, Tuple, Union

import pandas as pd


class FunctionCall(object):
    def __init__(self, columns, function, output_names=None):
        self.columns = columns
        self.function = function
        self.output_names = output_names

    def __call__(self, data_dict) -> None:
        # Check that the column names exist in the data dictionary
        invalid_columns = set(self.columns).difference(data_dict.keys())
        if len(invalid_columns) > 0:
            raise ValueError("Specified column names do not exist: " + str(invalid_columns))

        # Create dataframe from the selected columns
        input_data = _merge_columns_by_index(self.columns, data_dict)

        # Apply function call, passing in the dataframe
        output_data = self.function(input_data)

        # Check that function returns a pandas dataframe
        if not isinstance(output_data, pd.DataFrame):
            raise TypeError(
                "Output of "
                + self.function.__name__
                + " must be a pandas DataFrame in order to be pipeline compatible."
            )

        # Store updates to be added to data dict
        update_dict = {}

        # Inplace update
        if self.output_names is None:
            for colname in output_data.columns:
                update_dict[colname] = pd.DataFrame(output_data[colname])

        # Not inplace update
        else:
            for i, colname in enumerate(output_data.columns):
                update_dict[self.output_names[i]] = pd.DataFrame(output_data[colname])
                update_dict[self.output_names[i]].columns = [self.output_names[i]]

        # Update data dictionary
        data_dict.update(update_dict)

    def __repr__(self):
        try:
            function_name = str(self.function.func.__name__)
        except AttributeError:
            function_name = str(self.function.__name__)
        if self.output_names is None:
            return "(" + ", ".join(str(col) for col in self.columns) + " -> " + function_name + ")"
        else:
            return (
                "("
                + ", ".join(str(col) for col in self.columns)
                + " -> "
                + function_name
                + " -> "
                + ", ".join(str(name) for name in self.output_names)
                + ")"
            )


class Pipeline(object):
    """
    Pipeline class for chaining together any arbitrary sequence of functions together.

    Example:

        Interpolate data and smooth one of the DataFrame columns::

            >>> from inso_toolbox.imputer import interpolate
            >>> from inso_toolbox.smoother import smoother_sg
            >>> from inso_toolbox import Pipeline
            >>>
            >>> # Let data be a pandas DataFrame with columns "id1" and "id2"
            >>> p = Pipeline()
            >>> p.add_sequential(["id1", "id2"], interpolate(kind="linear", method="average"))
            >>> p.add_sequential("id2", smoother_sg(polyorder=3), "id2_smoothed")
            >>> p.run(data)
    """

    def __init__(self):
        self.queue = []  # Function queue

    def add_sequential(
        self,
        columns: Union[str, List[str]],
        functions: Union[Callable, List[Callable]],
        output_names: Union[str, List[str]] = None,
    ) -> None:
        """
        Specify functions to apply on certain columns present in a DataFrame.

        Args:
            columns (Union[str, List[str]]): Column names for which the functions will be applied on.
            functions (Union[Callable, List[Callable]]): Functions to apply on the specified columns.
                The functions are executed in a sequential manner, one column at a time.
            output_names (Union[str, List[str]]): Final output column names.
                Default behaviour is to overwrite the input data.

        Returns:
            None
        """
        # Clean input data
        columns, functions, output_names = self._clean_add_sequential_input(columns, functions, output_names)

        # Fix inplace operator
        for i, column in enumerate(columns):
            for j, function in enumerate(functions):
                if output_names is None:
                    item = FunctionCall([column], function)
                else:
                    output_name = output_names[i]
                    if j == 0:
                        item = FunctionCall([column], function, [output_name])
                    else:
                        item = FunctionCall([output_name], function)
                self.queue.append(item)

    def run(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Run all functions that have been added to the Pipeline.

        Args:
            data (pd.DataFrame): Data to run the functions on.
                Data column names must match those that have been added to the Pipeline.

        Returns:
            pd.DataFrame
        """
        # Check for valid input
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")

        # Change data to a dictionary
        data_dict = {}
        for colname in data.columns:
            data_dict[colname] = pd.DataFrame(data[colname])

        # Loop through each FunctionCall, calling the object
        for function_call in self.queue:
            function_call(data_dict)

        # Concatenate the data dictionary back to a DataFrame
        data = _merge_columns_by_index(list(data_dict.keys()), data_dict)

        # Return final data
        return data

    def _clean_add_sequential_input(
        self, columns: Union[str, List], functions: Union[Callable, List], output_names: Union[str, List[str], None],
    ) -> Tuple[List, List, Optional[List]]:
        """
        Returns the cleaned version of columns functions and output_names
        """
        # Convert columns, functions and output_names as lists if not already so
        columns = [columns] if isinstance(columns, str) else columns
        functions = [functions] if callable(functions) else functions
        output_names = [output_names] if isinstance(output_names, str) else output_names

        # Assert that they are all lists now
        for lst, lst_name in zip([columns, functions, output_names], ["columns", "functions", "output_names"]):
            if lst_name == "output_names" and lst is None:
                continue
            if not isinstance(lst, List):
                raise TypeError("Incorrect input type for argument " + lst_name)

        # Check for valid input
        if output_names is not None:
            if len(columns) != len(output_names):
                raise TypeError("Number of output names must match the number of columns")
            if len(set(output_names)) != len(output_names):
                raise TypeError("Output names must be unique")

        # Check that all inserted functions are callable
        for function in functions:
            if not callable(function):
                raise TypeError("Incorrect function call got " + str(function) + " instead of a callable object")

        return columns, functions, output_names

    def __repr__(self):
        return str(self.queue)


def _merge_columns_by_index(columns: List[str], data_dict: Dict) -> pd.DataFrame:
    """
    Convenience method to merge columns together. Raises ValueError if indices don't match.
    """
    data = data_dict[columns[0]]

    for i in range(1, len(columns)):
        colname = columns[i]
        try:
            pd.testing.assert_index_equal(data.index, data_dict[colname].index)
        except AssertionError:
            raise ValueError("All indices must match to merge these time series:\n", columns)
        data = pd.concat((data, data_dict[colname]), axis="columns")

    return data
