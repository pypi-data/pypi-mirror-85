import json
from pprint import pprint
from typing import Any, Dict

from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow_grpc.grpc_operator import GrpcOperator
from google.protobuf import json_format

from .score_pb2_grpc import ScoreServiceStub
from .score_pb2 import ScoreRequest


def test_operator(dag):
    def app_score_response(response: Any, context: Dict):
        print(response)
        print(context)
        # context['ti'].xcom_push(key='app_score_response', value=response)
        return response

    app_score_op = GrpcOperator(
        task_id='get_app_score',
        dag=dag,
        grpc_conn_id='user_grpc_default',
        stub_class=ScoreServiceStub,
        call_func='AppScore',
        request_data_func=ScoreRequest,
        # data={'request': GetAppRequest(channel='com.idr.dokuin')},
        response_callback=app_score_response,
        log_response=True,
        xcom_push=True,
        xcom_task_id=Variable.get('APP_SCORE_TASK_ID')
    )



    return app_score_op
