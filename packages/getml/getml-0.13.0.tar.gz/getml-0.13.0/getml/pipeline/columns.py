# Copyright 2020 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
Custom class for handling the columns of a pipeline.
"""

import json
import numbers

import numpy as np
import pandas as pd

import getml.communication as comm

from getml.data.helpers import (
    _is_typed_list
)

from .helpers import (
    _attach_empty,
    _check_df_types,
    _set_unused,
    _transform_peripheral
)


class Columns():
    """
    Custom class for handling the
    columns inserted into the pipeline.

    Example:

        .. code-block:: python

            names, importances = my_pipeline.columns.importances()

            # Sets all categorical and numerical columns that are not
            # in the top 20% to unused.
            my_pipeline.columns.select(
                population_table,
                peripheral_tables,
                share_selected_columns=0.2
            )
    """

    # ----------------------------------------------------------------

    def __init__(self, name, targets, peripheral):

        if not isinstance(name, str):
            raise ValueError(
                "'name' must be a str.")

        if not _is_typed_list(targets, str):
            raise TypeError(
                "'targets' must be a list of str.")

        self.name = name

        self.targets = targets

        self.peripheral = peripheral

        self.peripheral_names = [p.name for p in self.peripheral]

    # ----------------------------------------------------------------

    def _get_column_importances(self, target_num, sort):

        cmd = dict()

        cmd["type_"] = "Pipeline.column_importances"
        cmd["name_"] = self.name

        cmd["target_num_"] = target_num

        # ------------------------------------------------------------

        sock = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Success!":
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        msg = comm.recv_string(sock)

        json_obj = json.loads(msg)

        # ------------------------------------------------------------

        descriptions = np.asarray(json_obj["column_descriptions_"])
        importances = np.asarray(json_obj["column_importances_"])

        # ------------------------------------------------------------

        if not sort:
            return descriptions, importances

        # ------------------------------------------------------------

        indices = np.argsort(importances)[::-1]

        # ------------------------------------------------------------

        return (
            descriptions[indices],
            importances[indices]
        )

    # ----------------------------------------------------------------

    def _to_pandas(self, target_num, target_name):

        descriptions, importances = self._get_column_importances(
            target_num=target_num,
            sort=False
        )

        markers = np.asarray([
            d["marker_"] for d in descriptions
        ])

        tables = np.asarray([
            d["table_"] for d in descriptions
        ])

        names = np.asarray([
            d["name_"] for d in descriptions
        ])

        max_length = np.max([
            len(names),
            len(importances)
        ])

        data_frame = pd.DataFrame(
            index=np.arange(max_length)
        )

        data_frame["population/peripheral"] = _attach_empty(
            markers.tolist(), max_length, "--")

        data_frame["table"] = _attach_empty(
            tables.tolist(), max_length, "--")

        data_frame["name"] = _attach_empty(
            names.tolist(), max_length, "--")

        data_frame["importance"] = _attach_empty(
            importances.tolist(), max_length, np.NaN)

        data_frame["target"] = [target_name] * max_length

        return data_frame

    # ----------------------------------------------------------------

    def importances(self, target_num=0, sort=True):
        """
        Returns the data for the column importances.

        Column importances extend the idea of feature importances
        to the columns originally inserted into the pipeline.
        Each column is assigned an importance value that measures
        its contribution to the predictive performance. All
        columns importances add up to 1.

        Args:
            target_num (int):
                Indicates for which target you want to view the
                importances.
                (Pipelines can have more than one target.)

            sort (bool):
                Whether you want the results to be sorted.

        Return:
            (:class:`numpy.ndarray`, :class:`numpy.ndarray`):
                - The first array contains the names of
                  the columns.
                - The second array contains their importances.
                  By definition, all importances add up to 1.
        """

        # ------------------------------------------------------------

        descriptions, importances = self._get_column_importances(
            target_num=target_num,
            sort=sort
        )

        # ------------------------------------------------------------

        names = np.asarray([
            d["marker_"] + " " + d["table_"] + "." + d["name_"]
            for d in descriptions
        ])

        # ------------------------------------------------------------

        return names, importances

    # ----------------------------------------------------------------

    def select(
            self,
            population_table,
            peripheral_tables=None,
            share_selected_columns=0.5):
        """
        Sets all categorical or numerical columns that are not
        sufficiently important to unused.

        Args:
            population_table (:class:`getml.data.DataFrame`):
                Main table containing the target variable(s) and
                corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable.

            peripheral_tables (List[:class:`getml.data.DataFrame`] or dict):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable.

            share_selected_columns(numerical): The share of columns
                to keep. Must be between 0.0 and 1.0.
            """

        # ------------------------------------------------------------

        peripheral_tables = _transform_peripheral(
            peripheral_tables, self.peripheral)

        _check_df_types(population_table, peripheral_tables)

        # ------------------------------------------------------------

        if not isinstance(share_selected_columns, numbers.Real):
            raise TypeError("'share_selected_columns' must be a real number!")

        if share_selected_columns < 0.0 or share_selected_columns > 1.0:
            raise ValueError(
                "'share_selected_columns' must be between 0 and 1!")

        # ------------------------------------------------------------

        if peripheral_tables and len(peripheral_tables) != len(self.peripheral_names):
            raise ValueError("""There must be exactly
                                one peripheral table for
                                every peripheral placeholder!""")

        # ------------------------------------------------------------

        descriptions, _ = self._get_column_importances(
            target_num=-1,
            sort=True
        )

        # ------------------------------------------------------------

        keep = int(np.ceil(share_selected_columns * len(descriptions)))

        remove_columns = descriptions[keep:]

        # ------------------------------------------------------------

        if peripheral_tables:
            for data_frame, name in zip(peripheral_tables, self.peripheral_names):
                cols = [desc["name_"] for desc in remove_columns
                        if desc["table_"] == name
                        and desc["marker_"] == "[PERIPHERAL]"]

                _set_unused(data_frame, cols)

        # ------------------------------------------------------------

        cols = [desc["name_"] for desc in remove_columns
                if desc["marker_"] == "[POPULATION]"]

        _set_unused(population_table, cols)

    # ----------------------------------------------------------------

    def to_pandas(self):
        """Returns all information related to the columns
           in a pandas data frame."""

        data_frame = None

        for t_num, t_name in enumerate(self.targets):
            current_df = self._to_pandas(t_num, t_name)

            if data_frame is None:
                data_frame = current_df
                continue

            data_frame = pd.concat(
                [data_frame, current_df],
                ignore_index=True
            )

        return data_frame

    # ----------------------------------------------------------------
