import boto3
import pytest
import os
from os import path
import yaml

from moto import mock_dynamodb2


@pytest.fixture(autouse=True)
def set_envs(monkeypatch):
    with open(path.join(path.dirname(path.abspath(__file__)), 'test_data.yml'), 'r', encoding='utf-8') as fp:
        envs = yaml.safe_load(fp)['environment']

    for k, v in envs.items():
        monkeypatch.setenv(k, str(v))


@pytest.fixture()
def table():
    with mock_dynamodb2():
        with open(path.join(path.dirname(path.abspath(__file__)), 'test_data.yml'), 'r', encoding='utf-8') as fp:
            test_data = yaml.safe_load(fp)['DynamoDB']

        table_config = test_data['Table']
        dynamodb = boto3.resource('dynamodb')
        # テスト用テーブルの作成
        dynamodb.create_table(
            TableName=os.environ['TABLE_NAME'],
            AttributeDefinitions=table_config['AttributeDefinitions'],
            KeySchema=table_config['KeySchema']
        )
        # テスト用データの格納
        table = dynamodb.Table(os.environ['TABLE_NAME'])
        with table.batch_writer() as batch:
            for item in test_data['Items']:
                batch.put_item(Item=item)

        yield table


@pytest.mark.parametrize(
    "event, expected",
    [
        (
            {'body': {'id': '0001'}},
            [
                {
                    'id': '0001',
                    'name': 'Tanaka',
                    'age': 100,
                    'profile': 'human'
                }
            ]
        ),
        (
            {'body': {'id': '0005'}},
            []
        )
    ]
)
def test_handler(table, event, expected):
    from hello_world.app import handler
    assert expected == handler(event, context=None)
