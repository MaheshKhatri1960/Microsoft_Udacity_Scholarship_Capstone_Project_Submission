import json
import logging
import os
import pickle
import numpy as np
import pandas as pd
import joblib

from azureml.core.model import Model

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType

input_sample = pd.DataFrame({"age": pd.Series([0.0], dtype="float64"), "anaemia": pd.Series([0.0], dtype="float64"), "creatinine_phosphokinase": pd.Series([0.0], dtype="float64"), "diabetes": pd.Series([0.0], dtype="float64"), "ejection_fraction": pd.Series([0.0], dtype="float64"), "high_blood_pressure": pd.Series([0.0], dtype="float64"), "platelets": pd.Series([0.0], dtype="float64"), "serum_creatinine": pd.Series([0.0], dtype="float64"), "serum_sodium": pd.Series([0.0], dtype="float64"), "sex": pd.Series([0.0], dtype="float64"), "smoking": pd.Series([0.0], dtype="float64"), "time": pd.Series([0.0], dtype="float64")})
output_sample = np.array([0])


# -

def init():
    global model
    # This name is model.id of model that we want to deploy deserialize the model file back
    # into a sklearn model
    model_path = Model.get_model_path("best-automl-model")
    print(model_path)
    path = os.path.normpath(model_path)
    path_split = path.split(os.sep)
    try:
        model = joblib.load(model_path)
    except Exception as e:
        raise

@input_schema('data', PandasParameterType(input_sample))
@output_schema(NumpyParameterType(output_sample))
def run(data):
    try:
        result = model.predict(data)
        return json.dumps({"result": result.tolist()})
    except Exception as e:
        result = str(e)
        return json.dumps({"error": result})