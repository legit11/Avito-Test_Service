## Запуск проекта с Docker

Для запуска проекта с использованием Docker выполните следующую команду:

```docker-compose up --build```

После успешной сборки проект будет доступен по адресу: http://localhost:8080.

##Важная информация:
**Если вы используете Windows, возможно, у вас возникнут проблемы с выполнением скриптов из-за различий в стиле окончаний строк между Windows (CRLF) и Linux (LF). Docker требует, чтобы файлы использовали LF-формат.**
**Это особенно важно для следующих файлов:**

Dockerfile
```docker/start.sh```
```docker-compose.yml```

Конвертация стиля строк в LF
**Убедитесь, что указанные файлы используют стиль строк LF. Для этого вы можете конвертировать файлы из CRLF в LF с помощью текстового редактора, такого как:**

Visual Studio Code (VS Code)
PyCharm
Шаги для конвертации в VS Code:

Откройте файл в Visual Studio Code.
Нажмите на индикатор стиля окончаний строк в правом нижнем углу.
Выберите "LF" (или "Convert to LF").
Шаги для конвертации в PyCharm:

Откройте файл в PyCharm.
Перейдите в меню "File" -> "Line Separators".
Выберите "Unix and OS X (\n)".
**Правильный стиль окончаний строк необходим для корректной работы контейнера Docker.**
