import io
from unittest import TestCase
from unittest.mock import Mock

from botocore.response import StreamingBody
from botocore.stub import Stubber

from app.s3_service import S3Service


def get_response(content_file):

    return {
        'ContentLength': 500,
        'Body': StreamingBody(
            raw_stream=io.BytesIO(content_file),
            content_length=len(content_file)
        )
    }


class TestS3Service(TestCase):

    def setUp(self) -> None:
        self.s3_service = S3Service()

    def test_get_client(self):

        client = self.s3_service.get_client()
        assert client is not None

    def test_execute_get_object_success(self):

        s3_client = self.s3_service.get_client()
        assert s3_client is not None

        # prepara um stubber
        with Stubber(s3_client) as stubber:
            # simula um conteudo qualquer
            content_file = b'sfsd-sdfgfd dgd fgdf-g dgdfgdfgd-d gdfgdfgd'
            bucket_test = 'bucket_name'
            key_test = 'key_file_name'
            # recupera a resposta esperada da execucao do metodo s3_client.get_object()
            response = get_response(content_file)
            # esses sao os parametros enviados ao metodo s3_client.get_object()
            expected_params = {'Bucket': bucket_test, 'Key': key_test}
            stubber.add_response('get_object', response, expected_params)
            stubber.activate()
            # recebe a resposta do metodo contendo o conteudo e o tamanho do arquivo
            service_response = self.s3_service.execute_get_object(client=s3_client,
                                                                  bucket=bucket_test,
                                                                  key=key_test)
            assert service_response == content_file

    def test_execute_get_object_success_file_not_found(self):

        s3_client = self.s3_service.get_client()
        s3_client.get_object = Mock(return_value=None)
        bucket_test = 'bucket_name'
        key_test = 'key_file_name'

        with self.assertRaises(FileNotFoundError):
            # recebe a resposta do metodo contendo o conteudo e o tamanho do arquivo
            self.s3_service.execute_get_object(client=s3_client,
                                               bucket=bucket_test,
                                               key=key_test)
