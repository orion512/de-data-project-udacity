from __future__ import division, absolute_import, print_function

from airflow.plugins_manager import AirflowPlugin

import operators
import utils

# Defining the plugin class
class CustomPlugin(AirflowPlugin):
    name = "custom_plugin"
    operators = [
        operators.StageToPostgresOperator,
        # operators.LoadFactOperator,
        # operators.LoadDimensionOperator,
        # operators.DataQualityOperator
    ]
    helpers = [
        utils.SqlQueries
    ]