import base64
import json
import unittest
from unittest.mock import MagicMock, Mock

from app.exceptions.custom_exceptions import InvalidQueryParametersException, InvalidS3ParametersException
from app.process import Process

event = {
    'queryStringParameters': {
        'bucket': 'bucket_name',
        'key': 'key_file_name'
    }
}


class TestProcess(unittest.TestCase):

    def setUp(self) -> None:
        self.process = Process()

    def test_execute(self):
        expected_get_object_response = b'Data file'
        expected_response = self.process.build_response(expected_get_object_response)
        self.process.validate_query_string_param = Mock(return_value=event['queryStringParameters'])
        self.process.validate_param_values = Mock(return_value=('bucket_name', 'key_file_name'))
        self.process.s3_service = MagicMock()
        self.process.s3_service.get_client = MagicMock()
        self.process.s3_service.execute_get_object = MagicMock(return_value=expected_get_object_response)

        content = self.process.execute(event)

        assert content == expected_response
        self.process.validate_query_string_param.assert_called_with(event)
        self.process.validate_param_values.assert_called_with(event['queryStringParameters'])
        self.process.s3_service.get_client.assert_called_once()
        self.process.s3_service.execute_get_object.assert_called_with(self.process.s3_service.get_client(),
                                                                      'bucket_name',
                                                                      'key_file_name')

    def test_validate_param_values_success(self):
        bucket, key = self.process.validate_param_values(event['queryStringParameters'])

        assert bucket is not None, 'Parametro bucket esta vazio'
        assert key is not None, 'Parametro key esta vazio'
        assert bucket == 'bucket_name', 'Valor do parametro bucket esta diferente do esperado'
        assert key == 'key_file_name', 'Valor do parametro key esta diferente do esperado'

    def test_validate_param_values_fail(self):
        with self.assertRaises(InvalidS3ParametersException):
            self.process.validate_param_values({})

    def test_validate_query_string_param_success(self):
        params = self.process.validate_query_string_param(event)

        assert params is not None, 'Parametro event esta nulo'
        assert 'bucket' in params, 'Parametro bucket nao informado dentro de queryStringParameters'
        assert 'key' in params, 'Parametro key nao informado dentro de queryStringParameters'
        assert params['bucket'] == 'bucket_name', 'Valor do parametro bucket diferente do esperado'
        assert params['key'] == 'key_file_name', 'Valor do parametro key diferente do esperado'

    def test_validate_query_string_param_fail(self):
        with self.assertRaises(InvalidQueryParametersException):
            self.process.validate_query_string_param({})

    def test_build_response_success(self):
        content = b'file content'
        success_response = {
            'headers': {'Content-Type': 'text/plan; charset=utf-8'},
            'statusCode': 200,
            'body': base64.b64encode(content).decode('utf-8'),
            'isBase64Encoded': True
        }
        response = self.process.build_response(content)

        assert response is not None
        assert response == success_response

    def test_build_response_file_not_found(self):
        file_not_found_response = {'statusCode': 404, 'body': json.dumps('Arquivo não encontrado')}
        response = self.process.build_response(None)

        assert response is not None
        assert response == file_not_found_response


if __name__ == '__main__':
    unittest.main()
