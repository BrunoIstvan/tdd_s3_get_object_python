# tdd_s3_get_object_python

Criar virtualenv:

    pip install virtualenv
    virtualenv venv
    
Ativar virtualenv

    source venv/bin/activate

Desativar virtualenv

    deactivate

Instalar dependências:

    pip install -r requirements.txt

Rodar os testes unitários:

    pytest --cov=app tests/   

Criar arquivo zip para subir no lambda:

    zip s3_get_object_python.zip lambda_function.py app/ 

Atualizar código do lambda:

    aws lambda update-function-code --function-name <lambda-function-name> --zip-file fileb://s3_get_object_python.zip

    