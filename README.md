# Artina
### Пример работы сайта
![Главная страница сайта](/media_for_readme/mainpage_artina.png)

![Страница художников](/media_for_readme/artists_artina.png)

![Картины Третьяковской Галереи](/media_for_readme/paintings_artina.png)

### Запуск кода программы
#### 1) Клонируйте репозиторий
```commandline
git clone https://github.com/TWoWsCreator/Artina.git
```
#### 2) Создайте виртуальную среду
For Windows:
```commandline
python -m venv venv
.\venv\Scripts\activate
```
For Mac OS/Linux:
```commandline
python3 -m venv venv
source venv/bin/activate
```
#### 3) Установите зависимости
```commandline
pip install -r requirements.txt
```
#### 4) Сделайте миграции
```commandline
python manage.py migrate
```
#### 5) Загрузите фикстуры
```commandline
python manage.py loaddata fixtures/data.json
```
#### 6) Запустите сайт
```commandline
python manage.py runserver
```
##### 7) перейдите по адресу http://127.0.0.1:8000

### Структура базы данных