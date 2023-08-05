# -*- coding: utf-8 -*-

"""Validator module.
"""

import logging
import os
import re
from collections import defaultdict
from pprint import pprint
import pint_pandas as pintpandas

import jsonschema
import pandas as pd

import simplejson as json
import yaml


# use short units
pintpandas.PintType.ureg.default_format = "~P"


class DataFrameSchematizer:
    """
    utility class to build a schema (jsonschema) for a Pandas DataFrame

    Given a DataFrame like:

    >>> df = pd.DataFrame({ "id": {7: 0, 1: 1, 2:5},
    ...                    "name": {7: "Doe", 1: "Fante", 2: "Mercury"},
    ...                    "firstname": {7: "John", 2: "Freddy", 1:"Richard"},
    ...                    "age": {7: '42', 1: 22},
    ...                    "life_nb": {7: 5, 1: 'hg', 2: 15}})

    We can build a column-wise schema:

    >>> v = DataFrameSchematizer()
    >>> v.add_column(name='id', types='integer', unique=True, mandatory=True)
    >>> v.add_column(name='name', types='string', mandatory=True)
    >>> v.add_column(name='firstname', types='string')
    >>> v.add_column(name='age', types='integer', mandatory=False, default=0)
    >>> v.add_column(name='life_nb', types='integer', mandatory=True, maximum=4)
    >>> v._is_units  # no units declared in any column
    False

    And validate the DataFrame:

    >>> df, is_valid, errors = v.validate_dataframe(df)
    >>> pprint(errors)
    {('age', 0): ["'42' is not valid under any of the given schemas",
                  "'42' is not of type 'integer'",
                  "'42' is not of type 'null'"],
     ('life_nb', 0): ['5 is greater than the maximum of 4'],
     ('life_nb', 1): ["'hg' is not of type 'integer'"],
     ('life_nb', 2): ['15 is greater than the maximum of 4']}

    The schema used for validation can be accessed by:

    >>> schema = v.build()
    >>> pprint(schema)
    {'$schema': 'http://json-schema.org/draft-07/schema#',
     'properties': {'age': {'items': {'anyOf': [{'type': 'integer'},
                                                {'type': 'null'}],
                                      'default': 0},
                            'type': 'array',
                            'uniqueItems': False},
                    'firstname': {'items': {'anyOf': [{'type': 'string'},
                                                      {'type': 'null'}]},
                                  'type': 'array',
                                  'uniqueItems': False},
                    'id': {'items': {'type': 'integer'},
                           'type': 'array',
                           'uniqueItems': True},
                    'life_nb': {'items': {'maximum': 4, 'type': 'integer'},
                                'type': 'array',
                                'uniqueItems': False},
                    'name': {'items': {'type': 'string'},
                             'type': 'array',
                             'uniqueItems': False}},
     'required': ['id', 'name', 'life_nb'],
     'type': 'object'}

    We can also build a basic schema and populate `DataFrameSchematizer` with it:

    >>> schema = {
    ...           'id': {'types': 'integer', 'unique': True, 'mandatory': True},
    ...           'name': {'types': 'string', 'mandatory': True},
    ...           'firstname': {'types': 'string'},
    ...           'age': {'types': 'integer', 'minimum': 0, 'default':0},
    ...           'life_nb': {'types': 'integer', 'mandatory': True, 'maximum': 4}
    ...           }

    >>> v = DataFrameSchematizer()
    >>> v.add_columns(schema)

    Or via a JSON string

    >>> schema = (
    ...   '{"id": {"types": "integer", "unique": true, "mandatory": true}, "name": '
    ...   '{"types": "string", "mandatory": true}, "firstname": {"types": "string"}, '
    ...   '"age": {"types": "integer", "minimum": 0, "default": 0}, "life_nb": {"types": "integer", '
    ...   '"mandatory": true, "maximum": 4}}')
    >>> v.add_columns(schema)
    >>> df, is_valid, errors = v.validate_dataframe(df)
    >>> pprint(errors)
    {('age', 0): ["'42' is not valid under any of the given schemas",
                  "'42' is not of type 'integer'",
                  "'42' is not of type 'null'"],
     ('life_nb', 0): ['5 is greater than the maximum of 4'],
     ('life_nb', 1): ["'hg' is not of type 'integer'"],
     ('life_nb', 2): ['15 is greater than the maximum of 4']}

    Or via a YAML string

    >>> schema = '''
    ... ---
    ... id:
    ...   types: integer
    ...   unique: true
    ...   mandatory: true
    ... name:
    ...   types: string
    ...   mandatory: true
    ... firstname:
    ...   types: string
    ... age:
    ...   types: integer
    ...   minimum: 0
    ...   default: 0
    ... life_nb:
    ...   types: integer
    ...   mandatory: true
    ...   maximum: 4
    ... '''
    >>> v.add_columns(schema)

    And validate the DataFrame:

    >>> df, is_valid, errors = v.validate_dataframe(df)
    >>> pprint(errors)
    {('age', 0): ["'42' is not valid under any of the given schemas",
                  "'42' is not of type 'integer'",
                  "'42' is not of type 'null'"],
     ('life_nb', 0): ['5 is greater than the maximum of 4'],
     ('life_nb', 1): ["'hg' is not of type 'integer'"],
     ('life_nb', 2): ['15 is greater than the maximum of 4']}
    """

    def __init__(self):
        self.columns_specs = {}
        self.required = []
        self._is_units = False
        self._units = None


    def build(self):
        """build and return schema"""
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {},
            # "required": []
        }
        for colname, desc in self.columns_specs.items():
            schema["properties"][colname] = desc
        schema["required"] = self.required
        return schema

    def _add_columns_from_json(self, jsontxt):
        specs = json.loads(jsontxt)
        self.add_columns(specs)

    def _add_columns_from_yaml(self, yamltxt):
        specs = yaml.load(yamltxt, Loader=yaml.FullLoader)
        self.add_columns(specs)

    def add_columns_from_string(self, txt):
        """create columns checker from string. First test json, then yaml"""
        try:
            self._add_columns_from_json(jsontxt=txt)
        except:
            self._add_columns_from_yaml(yamltxt=txt)

    def add_columns(self, specs):
        if isinstance(specs, str):
            self.add_columns_from_string(specs)
            return
        # --------------------------------------------------------------------
        # specs is a dictionnary mapping DataFrame columns to its spec
        for colname, colspec in specs.items():
            self.add_column(name=colname, **colspec)

    def add_column(
        self, name, types=("integer",), unique=False, mandatory=False, units=None, **kwargs
    ):
        """add a column to the schema"""
        if isinstance(types, str):
            types = (types,)
        types = list(types)
        if mandatory:
            self.required.append(name)
        else:
            types.append("null")
        # ---------------------------------------------------------
        if len(types) > 1:
            items = {"anyOf": [{"type": typ} for typ in types]}
        else:
            items = {"type": types[0]}
        items.update(kwargs)
        ref = {
            "type": "array",
            "items": items,
            "uniqueItems": unique,
        }
        # ---------------------------------------------------------------------
        # handle units specifications
        if units:
            ref['units'] = units
            self._is_units = True

        self.columns_specs[name] = ref

    def validate_dataframe(self, df):
        """validate dataframe against self.schema()"""
        schema = self.build()
        # ---------------------------------------------------------------------
        # builds mult-header from dataframes if schemas are units-aware
        if self._is_units:
            df.columns = pd.MultiIndex.from_tuples(zip(df.columns, df.iloc[0].fillna("")))
            df = df.iloc[1:]
            df = df.pint.quantify(level=-1)
        # ---------------------------------------------------------------------
        # first: fill empty values as requested by schema
        _fillnas = {
            k: schema["properties"][k]["items"].get("default")
            for k, v in schema["properties"].items()
        }
        fillnas = {
            k: v for k, v in _fillnas.items() if k in df.columns and v is not None
        }
        if fillnas:
            df = df.fillna(value=fillnas, downcast="infer")
        # ---------------------------------------------------------------------
        # convert read units to schema expected units (if required)
        if self._is_units:
            _target_units = {
                k: schema["properties"][k].get("units", "")
                for k in schema["properties"]
            }
            for col, units in _target_units.items(): 
                df[col] = df[col].pint.to(units)
            df = df.pint.dequantify()
            self._units = dict(df.columns.tolist())  #  {'id': '', 'distA': 'm',... }
            df.columns = df.columns.levels[0]
        # ---------------------------------------------------------------------
        # second: validate
        validator = jsonschema.Draft7Validator(schema)
        # df -> dict -> json -> dict to convert NaN to None
        document = json.loads(json.dumps(df.to_dict(orient="list"), ignore_nan=True))
        report = defaultdict(list)
        for error in validator.iter_errors(document):
            try:
                col, row, *rows = error.absolute_path
            except ValueError:
                report["general"].append(error.message)
            else:
                report[(col, row)].append(error.message)
                report[(col, row)].extend([e.message for e in error.context])
        report = dict(report)
        return df, len(report) == 0, report


class ValidatorMixin:
    """mixin class built on top of jsonschema"""

    def validator_mixin_init(self):
        """called by Base class __init__()"""
        self._schemas = {}

    def set_schema(self, tabname, schema):
        """assign a schema to a tab"""
        tabnames = []
        if tabname.startswith("^") and tabname.endswith("$"):
            # generic tabname regex: collect _data tabnames
            # matching regex
            for data_tabname in self._data.keys():
                if re.match(tabname, data_tabname):
                    tabnames.append(data_tabname)
        else:
            # not a regex. Only one tabname to fill
            tabnames = [tabname]
        for tabname in tabnames:
            self._schemas[tabname] = DataFrameSchematizer()  # reset schematizer
            self._schemas[tabname].add_columns(schema)

    def read_schema(self, filepath, debug=False):
        """ assign a global schema by parsing the given filepath"""
        _, ext = os.path.splitext(filepath)
        with open(filepath, "r") as fh:
            schema_specs = fh.read()
        if ext == ".json":
            schemas = json.loads(schema_specs)
        elif ext == ".yaml":
            schemas = yaml.load(schema_specs, Loader=yaml.FullLoader)
        for tabname, schema in schemas.items():
            self.set_schema(tabname, schema)

    def _validate_tab(self, tabname):
        """validate a tab using the provided scheme"""
        if tabname not in self._schemas:
            return None, True, {}
        return self._schemas[tabname].validate_dataframe(self._data[tabname])

    def validate(self):
        """
        iterate through all tabs and validate eachone
        """
        # keep initial data before processing them
        if not hasattr(self, '_raw_data'):
            self._raw_data = {tabname: df.copy() for tabname, df in self._data.items()}
        ret = {}
        for tabname, df in self._data.items():
            df, is_ok, report = self._validate_tab(tabname)
            self._data[tabname] = df  # override with filled (fillna) dataframe
            if not is_ok:
                ret[tabname] = report
        return ret

    def dump_template(self):
        """return list of columns ready to be dumped as XLSX template"""
        dic = {}
        for tabname, schema in self._schemas.items():
            dic[tabname] = pd.DataFrame({k: [] for k in schema.columns_specs.keys()})
        return dic


if __name__ == "__main__":
    import doctest

    doctest.testmod(
        optionflags=doctest.ELLIPSIS
        | doctest.IGNORE_EXCEPTION_DETAIL
        | doctest.NORMALIZE_WHITESPACE
    )
