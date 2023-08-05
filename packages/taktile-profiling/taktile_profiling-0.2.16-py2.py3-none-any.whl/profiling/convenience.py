import json
import logging
import os

from fastapi.encoders import jsonable_encoder

from .accuracy import calibration, largest_errors, metrics
from .dependence import partialdep
from .expectations import condexp
from .importance import varimp
from .shap import ShapExplainer
from .utils import create_description, df_to_dict, df_to_serializable_dict

BASE_RESULTS_PATH = os.environ.get("BASE_RESULTS_PATH", "results")


def mkdir(endpoint, spec_path=""):
    folder = os.path.join(BASE_RESULTS_PATH, endpoint.series_func.__name__, spec_path)
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def create_shapley_schema(endpoint):
    """Create shapley schema for endpoint"""
    x, y = endpoint.get_input_and_output_for_profiling(full_x=True)
    explainer = ShapExplainer(
        func=endpoint.series_func, X=x, profile_columns=endpoint.profile_columns
    )
    folder = mkdir(endpoint=endpoint)
    input_descriptions = [
        create_description(x[col]) for col in endpoint.profile_columns
    ]
    logging.info("Shapley - Creating schema")
    fname = "schema.json"
    fpath = os.path.join(folder, fname)
    data = create_explainer_schema(endpoint, explainer, input_descriptions)
    with open(fpath, "w") as f:
        json.dump(jsonable_encoder(data), f)


def create_explainer_schema(endpoint, explainer, input_descriptions):
    """Create schema for explainer input"""
    # create an example
    x, y = endpoint.get_input_and_output_for_profiling(full_x=False)
    x = x.sample(n=1)
    # Use explainer instead of endpoint because func is partialed out, only takes in profile_columns
    pred = explainer.func(x)
    baseline, explanation = explainer.explain(x)

    example = {
        "inputs": [df_to_serializable_dict(x.iloc[0])],
        "explanations": df_to_dict(explanation),
        "prediction": list(pred),
        "baseline": list(baseline),
    }
    # build schema
    schema = {"input_descriptions": input_descriptions, "example": example}
    return schema


def create_accuracy(endpoint):
    """Create accuracy profile for endpoint"""
    x, y = endpoint.get_input_and_output_for_profiling(full_x=True)
    func = endpoint.series_func
    kind = endpoint.KIND.value
    folder = mkdir(endpoint=endpoint, spec_path="accuracy")

    logging.info("Accuracy - Creating calibration plot")
    fname = "calibration.json"
    fpath = os.path.join(folder, fname)
    chart = calibration(func, x, y)
    chart.save(fpath, format="json")

    logging.info("Accuracy - Creating metrics table")
    fname = "metrics.json"
    fpath = os.path.join(folder, fname)
    metrics_table = metrics(func, x, y, kind)
    with open(fpath, "w") as f:
        f.write(metrics_table)

    logging.info("Accuracy - Finding largest errors")
    fname = "errors.json"
    fpath = os.path.join(folder, fname)
    errors_table = largest_errors(func, x, y, endpoint.profile_columns)
    with open(fpath, "w") as f:
        f.write(errors_table)


def create_dependence(endpoint):
    """Create partial dependence graphs for all variables"""
    x, y = endpoint.get_input_and_output_for_profiling(full_x=True, reset_index=True)
    func = endpoint.series_func
    folder = mkdir(endpoint=endpoint, spec_path="anatomy/partialdep")

    for var in endpoint.profile_columns:
        logging.info(f"Explanations - Creating partial dependence for {var}")
        fname = var + ".json"
        fpath = os.path.join(folder, fname)
        try:
            chart = partialdep(func, x, y, var)
            chart.save(fpath, format="json")
        except AttributeError:
            logging.warning(f"Could not generate valid chart for {var}")


def create_expectations(endpoint):
    """Create conditional expectations graphs for all variables"""
    x, y = endpoint.get_input_and_output_for_profiling(full_x=True, reset_index=True)
    func = endpoint.series_func
    folder = mkdir(endpoint=endpoint, spec_path="anatomy/condexp")

    for var in endpoint.profile_columns:
        logging.info(f"Explanations - Creating conditional expectations for {var}")
        fname = var + ".json"
        fpath = os.path.join(folder, fname)
        try:
            chart = condexp(func, x, y, var)
            chart.save(fpath, format="json")
        except AttributeError as e:
            logging.warning(f"Could not generate valid chart for {var}: {repr(e)}")
        except TypeError as e:
            # happens when object columns cannot be serialized to JSON
            # https://github.com/altair-viz/altair/issues/1355
            logging.warning(f"Could not generate valid chart for {var}: {repr(e)}")


def create_importance(endpoint):
    """Create variable importance graphs"""
    x, y = endpoint.get_input_and_output_for_profiling(full_x=True)
    func = endpoint.series_func

    logging.info("Explanations - Calculating variable importance")
    if endpoint.KIND.value == "regression":
        chart, varlist = varimp(func, x, y, endpoint.profile_columns, metric="Rmse")
    elif endpoint.KIND.value == "binary":
        chart, varlist = varimp(func, x, y, endpoint.profile_columns, metric="AUC")
    else:
        raise NotImplementedError("Unknown endpoint kind:" + endpoint.KIND.value)

    # Save to disk
    folder = mkdir(endpoint=endpoint, spec_path="anatomy")

    fname = "varimp.json"
    fpath = os.path.join(folder, fname)
    chart.save(fpath, format="json")

    fname = "varlist.json"
    fpath = os.path.join(folder, fname)
    with open(fpath, "w") as f:
        json.dump(varlist, f)


def create_summary(endpoint, explain_only=False):
    endpoint_name = endpoint.series_func.__name__
    logging.info(f"Summary - creating endpoint summary for endpoint: {endpoint_name}")
    if explain_only:
        endpoint_input_names = endpoint.explain_input_names
    else:
        endpoint_input_names = endpoint.input_names
    as_json = {
        "name": endpoint_name,
        "kind": endpoint.KIND.value,
        "inputs": endpoint_input_names,
        "output": endpoint.output_names,
    }
    # Save to disk
    folder = mkdir(endpoint=endpoint)
    with open(os.path.join(folder, "summary.json"), "w") as summary:
        json.dump(as_json, summary)
