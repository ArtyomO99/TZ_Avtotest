# TZ_Avtotest
HTTP-сервер для предоставления информации по географическим объектам.

Запуск:
python script.py

Используется адрес 127.0.0.1 и порт 8000

Описание:
1. /getfile/<geonameid> - принимает идентификатор geonameid и возвращает информацию о городе.
Пример: http://127.0.0.1:8000/getfile/451828

2. /getpage - принимает в параметры страницу page и количество отображаемых на странице городов perPage и возвращает список городов с их информацией.
Пример: http://127.0.0.1:8000/getpage?page=2&perPage=10

3. /getcity - принимает в параметры названия двух городов: city_1, city_2 (на русском языке), и получает информацию о найденных городах. Дополнительно сравнивает какой из городов севернее и одинаковая ли у них временная зона.
Пример: http://127.0.0.1:8000/getcity?city_1=Ступнево&city_2=Стукшино
