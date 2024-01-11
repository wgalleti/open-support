# Sistema para Suporte

> Requisitos

* Python 3.8
* Node 12+

Clonar projeto `git clone https://github.com/wgalleti/open-suporte`

> API

1. Entre na pasta api `cd api`
1. Ative o ambiente virtual `pipenv shell`
1. Instale as dependencias `pipenv install -d`
1. Copie o arquivo de exemplo do .env `cp env_sample .env`
1. Configure o .env de acordo com seu ambiente
1. Crie as migrações `python manage.py makemigrations`
1. Aplique as migrações `python manage.py migrate`
1. Crie o usuario `python manage.py createsuperuser`
1. Suba o servidor `python manage.py runserver`

> Frontend

1. Entre na pasta web `cd ../web`
2. Instale as dependencias `npm i`
3. Suba o servidor `npm run serve`