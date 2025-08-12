"""
ValueConverter.py
------------------
A utility class for converting token values using either:

1. Manual conversion (user specifies token decimals)
2. Dynamic conversion (reads token decimals from a pandas DataFrame column)

Author: Your Name
Date: YYYY-MM-DD
"""

from pathlib import Path
import pandas as pd


class ValueConverter:
    """
    A utility for converting token values based on decimal precision.

    Methods
    -------
    value_converter_manual(value, decimals):
        Converts a numeric value using a manually specified token decimal.
    
    value_converter_dynamic(df, value_col, decimal_col):
        Converts a DataFrame column dynamically based on a decimal column.
    """

    @staticmethod
    def value_converter_manual(value, decimals):
        """
        Convert a value using a manually provided token decimal.

        Parameters
        ----------
        value : float or int
            The raw value to convert.
        decimals : int
            The number of decimal places for the token.

        Returns
        -------
        float
            The converted value.
        """
        return value / (10 ** decimals)

    @staticmethod
    def value_converter_dynamic(df, value_col, decimal_col):
        """
        Convert values in a DataFrame dynamically using a decimal column.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        value_col : str
            The name of the column with raw values.
        decimal_col : str
            The name of the column with decimal values.

        Returns
        -------
        pandas.DataFrame
            A copy of the DataFrame with an added 'converted_value' column.
        """
        df_copy = df.copy()
        df_copy["converted_value"] = df_copy[value_col] / (10 ** df_copy[decimal_col])
        return df_copy


# --------------------------------------------------
# Example Usage
# --------------------------------------------------
# Uncomment the following lines to test this script directly.

# if __name__ == "__main__":
#     # Example 1: Manual conversion
#     manual_result = ValueConverter.value_converter_manual(123456789, 6)
#     print("Manual Conversion:", manual_result)
#
#     # Example 2: Dynamic conversion with pandas DataFrame
#     data = {
#         "token_value": [123456789, 987654321],
#         "token_decimals": [6, 8]
#     }
#     df = pd.DataFrame(data)
#     converted_df = ValueConverter.value_converter_dynamic(df, "token_value", "token_decimals")
#     print("\nDynamic Conversion DataFrame:")
#     print(converted_df)
#
# --------------------------------------------------
# Importing from a Local Directory in Jupyter Notebook:
# --------------------------------------------------
# from pathlib import Path
# import sys
#
# # Add the path to the directory where ValueConverter.py is stored
# sys.path.append(str(Path("/Users/WilliamWombat/jupyter_notebooks/data_science")))
#
# # Import the class
# from ValueConverter import ValueConverter
#
# # Manual conversion usage
# result = ValueConverter.value_converter_manual(123456789, 6)
# print(result)
#
# # Dynamic conversion usage
# import pandas as pd
# df = pd.DataFrame({"value": [123456789, 987654321], "decimals": [6, 8]})
# converted = ValueConverter.value_converter_dynamic(df, "value", "decimals")
# print(converted)
