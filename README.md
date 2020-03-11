>> 
API REST com Flask, Flask-Restful, SQLAlchemy e PostgreSQL
===================
Necessário ter o virtualenv e o pip instalados!

1. Instale todas as dependências:
```shell
$ pip install -r requirements.txt
```
2. Crie a tabela:
```shell
$ ./models.py
```
3. Execute a aplicação:
```
$ FLASK_APP=app.py flask run
```
4. Execute os comandos:
```shell
>> import requests, json
>> data_post = { 'first_name': 'User', 'email': 'user@gmail.com' }
>> data_put = { 'first_name': 'User', 'email': 'usertest@gmail.com' }
>> headers = { 'Content-Type': 'application/json' }
>> id = 1

>> requests.post('http://localhost:5000/users/', headers=headers, data=json.dumps(data_post)).json()
>> requests.get('http://localhost:5000/users/').json()
>> requests.put('http://localhost:5000/users/{}'.format(id), headers=headers, data=json.dumps(data_put)).json()
>> requests.delete('http://localhost:5000/users/{}'.format(id))