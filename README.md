## Запуск проекта осуществляется с помощью Docker

1. Чтобы запустить проект с помощью Docker, выполните команду:

```bash
docker-compose up --build
```
**Но для тестирования всей функциональности нужно будет вставить в Базу Данных тестовые данные(см. пункт 2)**


После сборки проект будет доступен по адресу `localhost:8080`.

### Важная информация:

В проект добавлен файл `.gitattributes` который принудительно устанавливает формат LF но в некоторых случаях это не срабатывает поэтому ->

Если вы работаете на Windows, возможно, у вас возникнут проблемы с выполнением скриптов из-за различий в стилях окончания строк между Windows (CRLF) и Linux (LF). Docker требует, чтобы файлы были в LF-формате. Это особенно важно для следующих файлов:


- `Dockerfile`
- `docker/start.sh`
- `docker-compose.yml`


Убедитесь, что указанные файлы имеют стиль строк LF. Вы можете конвертировать файлы из CRLF в LF с помощью любой текстовой редакции, например:
#### Pycharm:

1. Откройте файл в PyCharm.
2. Перейдите в меню "File" -> "Line Separators".
3. Выберите "Unix and OS X (\n)".
4. **Правильный стиль окончаний строк необходим для корректной работы контейнера Docker.**


#### Visual Studio Code:

1. Откройте файл в VS Code.
2. Нажмите на индикатор стиля окончания строк в правом нижнем углу.
3. Выберите "LF" (или "Convert to LF").
4. **Правильный стиль окончаний строк необходим для корректной работы контейнера Docker.





Откройте файл в PyCharm.
Перейдите в меню "File" -> "Line Separators".
Выберите "Unix and OS X (\n)".
**Правильный стиль окончаний строк необходим для корректной работы контейнера Docker.**

2. ## Проект содержит набор тестовых данных для проверки функциональности

При необходимости вы можете вставить данные из файла `test_data.sql` в контейнер PostgreSQL с помощью команды:

```sh
   docker cp ./test_data.sql db_app:/test_data.sql
```


```sh
   docker exec -it db_app psql -U postgres -d postgres -f /test_data.sql
```

## Осуществите проверку данных:

1. Проверьте наличие данных в таблице Employee:
   

 ```sh
   docker exec -it db_app psql -U postgres -d postgres -c "SELECT * FROM employee;"
```


2. Проверьте наличие данных в таблице Organization:

   
  ```sh
   docker exec -it db_app psql -U postgres -d postgres -c "SELECT * FROM organization;"
```


3. Проверьте наличие данных в таблице Responsible_Organizations:

   
   ```sh
   docker exec -it db_app psql -U postgres -d postgres -c "SELECT * FROM organization_responsible;"
   ```


5. Проверьте налчие данных в таблице Tenders:


 ```sh
   docker exec -it db_app psql -U postgres -d postgres -c "SELECT * FROM tenders;"
```

После этого проект  будет полностью готов к тестированию функциональности.


Большое спасибо!
