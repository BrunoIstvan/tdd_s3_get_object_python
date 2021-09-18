import boto3


class S3Service:

    def __init__(self):
        pass

    def get_client(self):
        """
        Método que retorna um client do S3
        :return: Client do S3
        """
        return boto3.client('s3')

    def execute_get_object(self, client, bucket, key):
        """
        Método que retorna o conteúdo de um arquivo dentro do S3
        :param client: Client do S3
        :param bucket: Nome do bucket
        :param key: Nome do arquivo
        :return: Conteúdo do arquivo
        """
        result = client.get_object(Bucket=bucket, Key=key)

        if result is None:
            raise FileNotFoundError('Arquivo não encontrado')

        # retorna o conteudo e o tamanho do arquivo
        return result['Body'].read()
