#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `gridsource` package."""

import os
import shutil
from pprint import pprint as pp

import numpy as np
import pandas as pd
import pytest

from gridsource import Data as IVData
from gridsource import ValidData as VData
from gridsource.validation import DataFrameSchematizer


def test_DFS_00_schema_bulding():
    """test DataFrameSchematizer class.
    DataFrameSchematizer class is purely internal and wrapped by VData or IVData
    """
    v = DataFrameSchematizer()
    columns_specs = """\
---
id:
  types: integer
  unique: true
  mandatory: true
name:
  types: string
  mandatory: true
firstname:
  types: string
age:
  types: integer
  minimum: 0
life_nb:
  types: integer
  mandatory: true
  maximum: 4
"""
    v.add_columns(columns_specs)
    # build valid jsonschema
    schema = v.build()
    expected_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": {
            "age": {
                "items": {
                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                    "minimum": 0,
                },
                "type": "array",
                "uniqueItems": False,
            },
            "firstname": {
                "items": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                "type": "array",
                "uniqueItems": False,
            },
            "id": {"items": {"type": "integer"}, "type": "array", "uniqueItems": True},
            "life_nb": {
                "items": {"maximum": 4, "type": "integer"},
                "type": "array",
                "uniqueItems": False,
            },
            "name": {
                "items": {"type": "string"},
                "type": "array",
                "uniqueItems": False,
            },
        },
        "required": ["id", "name", "life_nb"],
        "type": "object",
    }

    assert schema == expected_schema


def test_DFS_01_validation():
    """test DataFrameSchematizer class validation.
    DataFrameSchematizer class is purely internal and wrapped by VData or IVData


    This test-case mainly check **default** values on a simple one-row dataframe

    | Value        | default | mandatory | result    | check |
    |--------------+---------+-----------+-----------+-------|
    | blank or nan |         | True      | FAIL      | da    |
    | blank or nan |         | False     | blank nan | db    |
    | blank or nan | 1       | True      | 1         | dc    |
    | blank or nan | 1       | False     | 1         | dd    |
    | 2            |         | True      | 2         | de    |
    | 2            |         | False     | 2         | df    |
    | 2            | 1       | True      | 2         | dg    |
    | 2            | 1       | False     | 2         | dh    |
    """
    v = DataFrameSchematizer()
    columns_specs = """\
---
da:
  types: integer
  mandatory: true
db:
  types: integer
  mandatory: false
dc:
  types: integer
  mandatory: true
  default: 1
dd:
  types: integer
  mandatory: false
  default: 1
de:
  types: integer
  mandatory: true
df:
  types: integer
  mandatory: false
dg:
  types: integer
  mandatory: true
  default: 1
dh:
  types: integer
  mandatory: false
  default: 1
"""
    v.add_columns(columns_specs)
    df = pd.DataFrame(
        {
            "da": {1: None},
            "db": {},
            "dc": {1: np.nan},
            "dd": {1: None},
            "de": {1: 2},
            "df": {1: 2},
            "dg": {1: 2},
            "dh": {1: 2},
        }
    )
    df, is_valid, errors = v.validate_dataframe(df)
    assert is_valid is False
    expected_errors = {("da", 0): ["None is not of type 'integer'"]}
    assert errors == expected_errors
    # check that values have been correctly filled
    expected_df = pd.DataFrame(
        {
            "da": {1: None},
            "db": {1: np.nan},
            "dc": {1: 1},
            "dd": {1: 1},
            "de": {1: 2},
            "df": {1: 2},
            "dg": {1: 2},
            "dh": {1: 2},
        }
    )
    assert pd.testing.assert_frame_equal(df, expected_df, check_dtype=False) is None


def test_VData_00():
    data = VData()
    # ------------------------------------------------------------------------
    # Create a schema for "test" tab
    # This example show a YAML schema syntax,
    # but json or plain dict is also OK:
    from io import StringIO

    data.set_schema(
        "test",
        "---"
        "\nid:"
        "\n  types: integer"
        "\n  unique: true"
        "\n  mandatory: true"
        "\nname:"
        "\n  types: string"
        "\n  mandatory: true"
        "\nfirstname:"
        "\n  types: string"
        "\nage:"
        "\n  types: integer"
        "\n  minimum: 0"
        "\nlife_nb:"
        "\n  types: integer"
        "\n  mandatory: true"
        "\n  maximum: 4",
    )
    # ------------------------------------------------------------------------
    # create dummy data
    data._data["test"] = pd.DataFrame(
        {
            "id": {7: 0, 1: 1, 2: 5},
            "name": {7: "Doe", 1: "Fante", 2: "Mercury"},
            "firstname": {7: "John", 2: "Freddy", 1: "Richard"},
            "age": {7: "42", 1: 22},
            "life_nb": {7: 5, 1: "hg", 2: 15},
        }
    )
    expected_report = {
        ("age", 0): [
            "'42' is not valid under any of the given schemas",
            "'42' is not of type 'integer'",
            "'42' is not of type 'null'",
        ],
        ("life_nb", 0): ["5 is greater than the maximum of 4"],
        ("life_nb", 1): ["'hg' is not of type 'integer'"],
        ("life_nb", 2): ["15 is greater than the maximum of 4"],
    }
    df, is_valid, errors = data._validate_tab("test")
    assert is_valid is False
    assert errors == expected_report


# =============================================================================
# level 1 : read files on disk
# =============================================================================


@pytest.fixture
def datadir():
    """
    Basic IO Structure
    """
    test_dir = os.path.dirname(os.path.realpath(__file__))
    indir = os.path.join(test_dir, "data")
    outdir = os.path.join(test_dir, "_out")
    # ensure outdir exists and is empty
    if os.path.isdir(outdir):
        shutil.rmtree(outdir)
    os.makedirs(outdir)
    return indir, outdir


def test_IVData_00(datadir):
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_00.xlsx"))
    data.read_schema(os.path.join(indir, "test_00.schema.yaml"))
    for tab in ("names", "cars", "empty"):
        print('checking "%s"' % tab, end="... ")
        df, is_ok, errors = data._validate_tab(tab)
        try:
            assert is_ok is True
        except:
            print("OUPS!")
            breakpoint()
        else:
            print("OK")
        assert errors == {}
    # ------------------------------------------------------------------------
    # export and reimport to/from various formats
    for extension in (".cfg", ".xlsx", ".ini"):
        target = os.path.join(outdir, "test_00" + extension)
        print("test '%s' extension" % target)
        assert not os.path.isfile(target)
        data.to(target)
        assert os.path.isfile(target)
        # --------------------------------------------------------------------
        # read the newly created file
        data_new = IVData()
        data_new.read(target)
        data_new.read_schema(os.path.join(indir, "test_00.schema.yaml"))
        for tab in data._data.keys():
            print('checking "%s"' % tab, end="... ")
            df, is_ok, errors = data_new._validate_tab(tab)
            try:
                assert is_ok is True
            except:
                print("OUPS!")
            else:
                print("OK")
            assert errors == {}


def test_IVData_01(datadir):
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_00.xlsx"))
    data.read_schema(os.path.join(indir, "test_00.schema.yaml"))
    ret = data.validate()
    assert len(ret) == 0


def test_IVData_02(datadir):
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_00.xlsx"))
    data.read_schema(os.path.join(indir, "test_00.schema2.yaml"))
    ret = data.validate()
    assert ret == {
        "cars": {("Year", 2): ["None is not of type 'integer'"]},
        "names": {"general": ["'name' is a required property"]},
    }


def test_IVData_03(datadir):
    """ make schema a bit more complex: add generic keys """
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_02.xlsx"))
    data.read_schema(os.path.join(indir, "test_02.schema.yaml"), debug=True)
    ret = data.validate()
    print(ret)  # TODO: remove me!
    assert len(ret) == 2
    expected_errors = {
        "names": {"general": ["'life_nb' is a required property"]},
        "french_cars": {
            ("brand", 2): [
                "'Citroën' is not one of ['Peugeot', 'Toyota', 'Ford', 'Renault']"
            ]
        },
    }

    assert ret == expected_errors


def test_IVData_04(datadir):
    """check units"""
    indir, outdir = datadir
    data = IVData()
    data.read(os.path.join(indir, "test_03_units.ini"))
    # -------------------------------------------------------------------------
    # read and check schema
    data.read_schema(os.path.join(indir, "test_03_units.schema.yaml"), debug=True)
    expected_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": {
            "Volume": {
                "items": {
                    "anyOf": [{"type": "number"}, {"type": "null"}],
                    "default": 0,
                },
                "type": "array",
                "uniqueItems": False,
                "units": "m^3",
            },
            "distA": {
                "items": {"type": "number"},
                "type": "array",
                "uniqueItems": False,
                "units": "m",
            },
            "distB": {
                "items": {
                    "anyOf": [{"type": "number"}, {"type": "null"}],
                    "default": 0,
                },
                "type": "array",
                "uniqueItems": False,
                "units": "m",
            },
            "id": {"items": {"type": "integer"}, "type": "array", "uniqueItems": True},
        },
        "required": ["id", "distA"],
        "type": "object",
    }
    assert data._schemas["geom"].build() == expected_schema
    ret = data.validate()
    expected_geom = pd.DataFrame(
        {
            "Volume": {1: 1.0, 2: 2.0},
            "distA": {1: 0.001, 2: 0.002},
            "distB": {1: 14.3, 2: 15.0},
            "id": {1: 1.5064562386943998, 2: 0.8183568665087998},
        }
    )
    assert pd.testing.assert_frame_equal(data._data['geom'], expected_geom) is None
