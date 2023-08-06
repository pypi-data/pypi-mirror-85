#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import warnings
from typing import (
    Optional,
    List,
    Any,
    Union,
    overload,
)

# create LOGGER with this namespace's name
import pandas
from pandas import DataFrame, Series

_logger = logging.getLogger("trashpanda")
_logger.setLevel(logging.ERROR)
# create console handler and set level to debug
writes_logs_onto_console = logging.StreamHandler()
# add formatter to ch
writes_logs_onto_console.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(name)s - %(module)s - %(funcName)s "
        "- %(lineno)s - %(levelname)s - %(message)s"
    )
)


__version__ = "0.1b0.post1"
__all__ = ["add_columns_to_dataframe", "add_missing_indexes_to_series"]


DEFAULT_NA = pandas.NA


@overload
def get_intersection(
    source: DataFrame, targeted_indexes: Union[List, pandas.Index]
) -> DataFrame:
    pass


@overload
def get_intersection(
    source: Series, targeted_indexes: Union[List, pandas.Index]
) -> Series:
    pass


def get_intersection(
    source: Union[DataFrame, Series], targeted_indexes: Union[List, pandas.Index]
) -> Union[DataFrame, Series]:
    """
    Intersects Series or DataFrame by requested indexes. A subsection from the
    *source* is made for the *targeted_indexes*, which must not necessaraly
    be whithin the *source*.

    Args:
        source(Union[DataFrame, Series]):
            Values from which an intersection will be retrieved.

        targeted_indexes(Index):
            The indexes which the returned Series should contain.

    Returns:
        Union[DataFrame, Series]

    Examples:
        >>> from pandas import Series, DataFrame
        >>> sample_series = Series(list(range(3)), index=list(iter("abc")), name="foo")
        >>> get_intersection(sample_series, ["b", "c", "d"])
        b    1
        c    2
        Name: foo, dtype: int64
        >>> get_intersection_of_series(sample_series, ["x", "y", "z"])
        Series([], Name: foo, dtype: int64)
        >>> sample_frame = DataFrame(
        ...     list(range(3)), index=list(iter("abc")), columns=["foo"]
        ... )
        >>> get_intersection(sample_frame, ["b", "c", "d"])
           foo
        b    1
        c    2
        >>> get_intersection(sample_frame, ["x", "y", "z"])
        Empty DataFrame
        Columns: [foo]
        Index: []

    """
    existing_indexes = source.index
    possible_indexes = existing_indexes.intersection(targeted_indexes)
    requested_series = source.loc[possible_indexes]
    return requested_series


def add_columns_to_dataframe(
    frame_to_enlarge: DataFrame,
    column_names: List[str],
    fill_value: Optional[Any] = None,
) -> DataFrame:
    """
    Adds columns to a dataframe. By default the columns are filled with
    pandas.NA values if no *fill_value* is explizitly given.

    Args:
        frame_to_enlarge(DataFrame):
            pandas.DataFrame which gets additional columns.

        column_names(List[str]):
            Names of additional columns to create.

        fill_value(Optional[Any]):
            Value which will fill the newly created columns. Default pandas.NA

    Returns:
        DataFrame

    Examples:
        >>> from pandas import DataFrame
        >>> import numpy
        >>> sample_frame = DataFrame(numpy.arange(4).reshape((2,2)), columns=["a", "b"])
        >>> sample_frame
           a  b
        0  0  1
        1  2  3
        >>> add_columns_to_dataframe(sample_frame, ["c", "d"], "+")
           a  b  c  d
        0  0  1  +  +
        1  2  3  +  +
        >>> add_columns_to_dataframe(sample_frame, ["c", "d"])
           a  b     c     d
        0  0  1  <NA>  <NA>
        1  2  3  <NA>  <NA>
    """
    if fill_value is None:
        fill_value = DEFAULT_NA

    for column_name_to_add in column_names:
        frame_to_enlarge[column_name_to_add] = fill_value
    return frame_to_enlarge


def override_left_with_right_dataframe(
    left_target: DataFrame, overriding_right: DataFrame
) -> DataFrame:
    """
    Overrides overlapping items of left with right.

    Args:
        left_target(DataFrame):
            Dataframe which should be overridden.

        overriding_right(DataFrame):
            The new values as frame, which overrides the *left target*.

    Returns:
        DataFrame

    Examples:
        >>> from pandas import DataFrame
        >>> import numpy as np
        >>> left = DataFrame(np.full(3, 1), index=list(iter("abc")), columns=["v"])
        >>> left
           v
        a  1
        b  1
        c  1
        >>> right = DataFrame(np.full(2, 2), index=list(iter("ad")), columns=["v"])
        >>> right
           v
        a  2
        d  2
        >>> override_left_with_right_dataframe(left, right)
           v
        a  2
        b  1
        c  1
        d  2
        >>> double_data = [list(range(1, 3)) for i in range(3)]
        >>> left = DataFrame(double_data, index=list(iter("abc")), columns=["m", "x"])
        >>> left
           m  x
        a  1  2
        b  1  2
        c  1  2
        >>> double_data = [list(range(3, 5)) for i in range(2)]
        >>> right = DataFrame(double_data, index=list(iter("ad")), columns=["x", "m"])
        >>> right
           x  m
        a  3  4
        d  3  4
        >>> override_left_with_right_dataframe(left, right)
           m  x
        a  4  3
        b  1  2
        c  1  2
        d  4  3
        >>> right = DataFrame(double_data, index=list(iter("ad")), columns=["z", "m"])
        >>> right
           z  m
        a  3  4
        d  3  4
        >>> override_left_with_right_dataframe(left, right)
           m    x     z
        a  4  2.0     3
        b  1  2.0  <NA>
        c  1  2.0  <NA>
        d  4  NaN     3

    """
    old_frame = left_target.copy()
    columns_to_add = overriding_right.columns.difference(left_target.columns)
    if not columns_to_add.empty:
        for column_name in columns_to_add:
            old_frame[column_name] = pandas.NA
    targeted_columns = overriding_right.columns
    same_indexes = overriding_right.index.intersection(old_frame.index)
    new_indexes = overriding_right.index.difference(old_frame.index)
    old_frame.loc[same_indexes, targeted_columns] = overriding_right.loc[same_indexes]
    new_rows = overriding_right.loc[new_indexes]
    overridden_frame = pandas.concat([old_frame, new_rows], sort=True)
    return overridden_frame


def add_missing_indexes_to_series(
    target_series: Series, new_indexes: pandas.Index, fill_value: Optional[Any] = None
) -> Series:
    """
    Adds different (missing) indexes to series.

    Args:
        target_series(Series):
            Series in which missing indexes should be added.

        new_indexes(pandas.Index):
            Indexes, which should be in the *target series*.

        fill_value(Optional[Any]):
            An optional fill value for the freshly added items.

    Returns:
        Series

    Examples:
        >>> from pandas import Series, Index
        >>> import numpy as np
        >>> target = Series(np.full(3, 1), index=list(iter("abc")), name="foo")
        >>> target
        a    1
        b    1
        c    1
        Name: foo, dtype: int64
        >>> new_indexes_to_add = Index(list(iter("ad")))
        >>> add_missing_indexes_to_series(target, new_indexes_to_add)
        a       1
        b       1
        c       1
        d    <NA>
        Name: foo, dtype: object
        >>> add_missing_indexes_to_series(target, new_indexes_to_add, "X")
        a    1
        b    1
        c    1
        d    X
        Name: foo, dtype: object

    """
    if fill_value is None:
        fill_value = DEFAULT_NA

    old_series = target_series.copy()
    try:
        missing_indexes = new_indexes.difference(old_series.index)
    except AttributeError:
        raise TypeError("new_indexes must be of pandas.Index type.")
    new_rows = Series([fill_value] * len(missing_indexes), index=missing_indexes)
    overridden_series = pandas.concat([old_series, new_rows], sort=True)
    overridden_series.name = old_series.name
    return overridden_series


def get_intersection_of_series(
    full_series: Series, targeted_indexes: Union[List, pandas.Index]
) -> Series:
    """
    Intersects series by requested indexes. A subsection from the
    *full_series* is made for the *targeted_indexes*, which must not necessaraly
    be whithin the *full_series*.

    Args:
        full_series(Series):
            Values from which an intersection will be retrieved.

        targeted_indexes(Union[List, pandas.Index]):
            The indexes which the returned Series should contain.

    Returns:
        Series

    .. warning::
        This method will be removed in the next release.
        Use :func:`trashpanda.get_intersection` instead.

    Examples:
        >>> from pandas import Series
        >>> sample_series = Series(list(range(3)), index=list(iter("abc")), name="foo")
        >>> get_intersection_of_series(sample_series, ["b", "c", "d"])
        b    1
        c    2
        Name: foo, dtype: int64
        >>> get_intersection_of_series(sample_series, ["x", "y", "z"])
        Series([], Name: foo, dtype: int64)

    """
    warnings.warn(
        "`get_intersection_of_series` will be removed in the next release. "
        "Use `get_intersection` instead.",
        DeprecationWarning,
    )
    return get_intersection(source=full_series, targeted_indexes=targeted_indexes)


def override_left_with_right_series(
    left_target: Series, overriding_right: Series
) -> Series:
    """
    Overrides overlapping items of left with right.

    Args:
        left_target(DataFrame):
            Series which should be overridden.

        overriding_right(DataFrame):
            The new values as Series, which overrides the *left target*.

    Returns:
        Series

    Examples:
        >>> from pandas import Series
        >>> import numpy as np
        >>> left = Series(np.full(3, 1), index=list(iter("abc")))
        >>> left
        a    1
        b    1
        c    1
        dtype: int64
        >>> right = Series(np.full(2, 2), index=list(iter("ad")))
        >>> right
        a    2
        d    2
        dtype: int64
        >>> override_left_with_right_series(left, right)
        a    2
        b    1
        c    1
        d    2
        dtype: int64

    """
    old_series = left_target.copy()
    same_indexes = overriding_right.index.intersection(old_series.index)
    new_indexes = overriding_right.index.difference(old_series.index)
    old_series.loc[same_indexes] = overriding_right.loc[same_indexes]
    new_items = overriding_right.loc[new_indexes]
    overridden_series = pandas.concat([old_series, new_items], sort=True)
    return overridden_series


if __name__ == "__main__":
    import doctest

    doctest.testmod()
