# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bq_airflow_dag_generator']

package_data = \
{'': ['*']}

install_requires = \
['apache-airflow>=1.10.9,<2.0.0',
 'google-cloud-bigquery>=2.3.1,<3.0.0',
 'networkx>=2.5,<3.0',
 'pydot>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'bq-airflow-dag-generator',
    'version': '0.1.4',
    'description': 'Generate Airflow DAG from DOT language to execute BigQuery efficiently mainly for AlphaSQL',
    'long_description': '# bq-airflow-dag-generator\n\nUtility package to generate Airflow DAG from DOT language to execute BigQuery efficiently mainly for [AlphaSQL](https://github.com/Matts966/alphasql).\n\n## Install\n\n```bash\npip install bq-airflow-dag-generator\n```\n\n## Usage\n\n```python\n# You can set SQL_ROOT if your SQL file paths in dag.dot are not on current directory.\nos.environ["SQL_ROOT"] = "/path/to/sql/root"\ndagpath = "/path/to/dag.dot"\ndag = generate_airflow_dag_by_dot_path(dagpath)\n```\n\nYou can add tasks to existing DAG like\n\n```python\ndagpath = "/path/to/dag.dot"\nexisting_airflow_dag\ngenerate_airflow_dag_by_dot_path(dagpath, dag=existing_airflow_dag)\n```\n\nYou can pass how to create Aiflow tasks like\n\n```python\ndef gen_task(sql_file_path, dag):\n    sql_root = os.environ.get("SQL_ROOT")\n    sql_file_path = os.path.join(sql_root, sql_file_path) if sql_root else sql_file_path\n    with open(sql_file_path, "r") as f:\n        query = f.read()\n        task = PythonOperator(\n            task_id=sql_file_path.replace("/", ""),\n            python_callable=get_bigquery_callable(query),\n            dag=dag,\n        )\n        task.doc = f"""\\\n# BigQuery Task Documentation: {sql_file_path}\nThis is automatically generated.\nQuery:\n{query}\n"""\n    return task\n\ndagpath = "/path/to/dag.dot"\ngenerate_airflow_dag_by_dot_path(dagpath, get_task_by_sql_path_and_dag=gen_task)\n```\n\n## Test\n\n```bash\npython -m unittest tests.test_dags\n```\n',
    'author': 'Matts966',
    'author_email': 'Matts966@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
