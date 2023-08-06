from abc import ABC, abstractmethod
from typing import Any, Dict, List, Sequence, Tuple, Type

import numpy
import pandas
from pydantic import BaseModel

from tktl.core.loggers import SdkLogger
from tktl.core.serializers import to_pydantic
from tktl.core.serializers.base import CustomDeserializingModelT
from tktl.core.t import RestSchemaTypes
from tktl.registration.validation import data_frame_convertible, series_convertible

logger = SdkLogger()

_SUPPORTED_TYPES = [pandas.DataFrame, pandas.Series, numpy.ndarray, Sequence, dict]


def check_supported_inputs(value):
    return any([isinstance(value, t_) for t_ in _SUPPORTED_TYPES])


class EndpointSchema(ABC):
    KIND: str

    def __init__(
        self,
        value: Any,
        endpoint_kind: str,
        endpoint_name: str,
        user_defined_model: Type[BaseModel] = None,
    ):
        self.endpoint_kind = endpoint_kind
        self.value = value
        self.is_supported = check_supported_inputs(value)
        if not self.is_supported:
            logger.warning(
                f"Schema discovery not supported for inputs of type {type(value)}"
            )
        if user_defined_model:
            value = user_defined_model
            print(value)

        self.pydantic: CustomDeserializingModelT = to_pydantic(
            value, unique_id=f"{endpoint_name}__{self.KIND}"
        )

    @property
    @abstractmethod
    def pandas_convertible(self):
        raise NotImplementedError

    def get_pandas_representation(self, **kwargs):
        if not self.pandas_convertible:
            raise ValueError("Pandas representation not available for this input")


class EndpointOutputSchema(EndpointSchema):
    KIND = "output"

    @property
    def pandas_convertible(self):
        return series_convertible(self.value)

    def get_pandas_representation(self, type_cast=None, reset_index=False):
        super(EndpointOutputSchema, self).get_pandas_representation()
        if isinstance(self.value, pandas.Series):
            if reset_index:
                self.value = self.value.reset_index(drop=True)
            name = self.value.name
            if not name:
                self.value.name = "Outcome"
            return self.value
        else:
            series = pandas.Series(self.value, name="Outcome")
            if type_cast:
                series = series.astype(type_cast)
            return series

    @property
    def names(self):
        if self.pandas_convertible:
            return self.get_pandas_representation().name
        else:
            return get_model_names(self.pydantic)


class EndpointInputSchema(EndpointSchema):
    KIND = "input"

    @property
    def pandas_convertible(self):
        return data_frame_convertible(self.value)

    def to_pandas(self, value):
        if isinstance(value, pandas.DataFrame):
            value.columns = self.names
            return value
        else:
            return pandas.DataFrame(value, columns=self.names)

    def get_pandas_representation(self, type_cast=None, reset_index=False):
        super(EndpointInputSchema, self).get_pandas_representation()
        df = pandas.DataFrame(self.value)
        df.columns = [str(c) for c in df.columns]
        if reset_index:
            df = df.reset_index(drop=True)
        return df

    @property
    def names(self):
        if self.pandas_convertible:
            return list(self.get_pandas_representation().columns)
        else:
            return get_model_names(self.pydantic)


def get_model_names(model: CustomDeserializingModelT):
    schema = model.schema()
    if schema["title"] == RestSchemaTypes.DICT.value:
        return list(schema["properties"].keys())
    elif (
        schema["title"] == RestSchemaTypes.SEQUENCE.value
        or schema["title"] == RestSchemaTypes.ARRAY.value
    ):
        return get_nested_type_names(schema)
    else:
        raise ValueError(f"Schema named: {schema['title']} is not recognized")


def get_nested_type_names(schema) -> List[str]:
    schema, inner_type = walk_sequence_schema(schema)
    n_features = schema[0]
    if len(schema) == 1:
        shapes = ""
    else:
        shapes_str = "x".join([str(dim) for dim in schema[1:]])
        shapes = f" (Shape: {shapes_str})"
    return [f"Feature {i}{shapes}" for i in range(n_features)]


def walk_sequence_schema(schema: Dict, shapes=()) -> Tuple[Tuple[int], str]:
    if schema["type"] == "array":
        shapes += (schema["maxItems"],)
        return walk_sequence_schema(schema["items"], shapes=shapes)
    if schema["type"] != "array":
        return shapes, schema["type"]
