import operator

import numpy as np
import pandas as pd
import pandas.util.testing as tm
import pytest

import moneypandas as mpd


@pytest.fixture
def series():
    return pd.Series(mpd.MoneyArray([None, 1, 2], 'USD'))


@pytest.fixture
def frame():
    return pd.DataFrame({"A": mpd.MoneyArray([None, 1, 2], 'GBP'),
                         "B": [0, 1, 2],
                         "C": mpd.MoneyArray([np.nan, 1, 2], 'USD')})


@pytest.fixture(params=['series', 'frame'])
def obj(request, series, frame):
    if request.param == 'series':
        return series
    elif request.param == 'frame':
        return frame


# -----
# Tests
# -----
@pytest.mark.parametrize('method', [
    operator.methodcaller('head'),
    operator.methodcaller('rename', str),
])
def test_works_generic(obj, method):
    method(obj)


@pytest.mark.parametrize('method', [
    operator.methodcaller('info'),
])
def test_works_frame(frame, method):
    method(frame)


def test__take(frame):
    return frame.take([0], axis=0)


def test_iloc_series(series):
    series.iloc[slice(None)]
    series.iloc[0]
    series.iloc[[0]]
    series.iloc[[0, 1]]


def test_iloc_frame(frame):
    frame.iloc[:, 0]
    frame.iloc[:, [0]]
    frame.iloc[:, [0, 1]]
    frame.iloc[:, [0, 2]]

    frame.iloc[0, 0]
    frame.iloc[0, [0]]
    frame.iloc[0, [0, 1]]
    frame.iloc[0, [0, 2]]

    frame.iloc[[0], 0]
    frame.iloc[[0], [0]]
    frame.iloc[[0], [0, 1]]
    frame.iloc[[0], [0, 2]]


def test_loc_series(series):
    series.loc[:]
    series.loc[0]
    series.loc[1]
    series.loc[[0, 1]]


def test_loc_frame(frame):
    frame.loc[:, 'A']
    frame.loc[:, ['A']]
    frame.loc[:, ['A', 'B']]
    frame.loc[:, ['A', 'C']]

    frame.loc[0, 'A']
    frame.loc[0, ['A']]
    frame.loc[0, ['A', 'B']]
    frame.loc[0, ['A', 'C']]

    frame.loc[[0], 'A']
    frame.loc[[0], ['A']]
    frame.loc[[0], ['A', 'B']]
    frame.loc[[0], ['A', 'C']]


def test_reindex(frame):
    result = frame.reindex([0, 10])
    expected = pd.DataFrame({"A": mpd.MoneyArray([None, np.nan], 'USD'),
                             "B": [0, np.nan],
                             "C": mpd.MoneyArray([None, np.nan], 'USD')},
                            index=[0, 10])
    tm.assert_frame_equal(result, expected)


def test_isna(series):
    expected = pd.Series([True, False, False], index=series.index,
                         name=series.name)
    result = pd.isna(series)
    tm.assert_series_equal(result, expected)

    result = series.isna()
    tm.assert_series_equal(result, expected)


def test_isna_frame(frame):
    result = frame.isna()
    expected = pd.DataFrame({"A": [True, False, False],
                             "B": [False, False, False],
                             "C": [True, False, False]})
    tm.assert_frame_equal(result, expected)


@pytest.mark.xfail(reason="Not implemented")
def test_fillna():
    result = pd.Series(mpd.MoneyArray([1, 0], 'USD')).fillna(method='ffill')
    expected = pd.Series(mpd.MoneyArray([1, 1], 'USD'))
    tm.assert_series_equal(result, expected)


@pytest.mark.xfail(reason="Not implemented")
def test_dropna():
    missing = pd.Series(mpd.MoneyArray([1, 0], 'USD'))
    result = missing.dropna()
    expected = pd.Series(mpd.MoneyArray([1], 'USD'))
    tm.assert_series_equal(result, expected)

    result = missing.to_frame().dropna()
    expected = expected.to_frame()
    tm.assert_frame_equal(result, expected)
