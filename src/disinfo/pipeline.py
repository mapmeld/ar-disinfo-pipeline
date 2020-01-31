"""Pipeline construction."""

from typing import Dict

from kedro.pipeline import Pipeline
from disinfo.pipelines import data_engineering as de
from disinfo.pipelines import data_science as ds



# Here you can define your data-driven pipeline by importing your functions
# and adding them to the pipeline as follows:
#
# from nodes.data_wrangling import clean_data, compute_features
#
# pipeline = Pipeline([
#     node(clean_data, 'customers', 'prepared_customers'),
#     node(compute_features, 'prepared_customers', ['X_train', 'Y_train'])
# ])
#
# Once you have your pipeline defined, you can run it from the root of your
# project by calling:
#
# $ kedro run


def create_pipelines(**kwargs) -> Dict[str, Pipeline]:
    """Create the project's pipeline.

    Args:
        kwargs: Ignore any additional arguments added in the future.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.

    """
    data_engineering_pipeline = de.create_pipeline()
    #data_science_pipeline = ds.create_pipeline()

    return {
        "de": data_engineering_pipeline,
        "__default__": data_engineering_pipeline # + data_science_pipeline,
    }
