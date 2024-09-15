Запуск проекта с Docker

Чтобы запустить проект с использованием Docker, выполните следующую команду:

```docker-compose up --build ```

После сборки проект будет доступен по адресу http://localhost:8080

Важная информация для пользователей Windows
Если вы используете Windows, возможно, у вас возникнут проблемы с выполнением скриптов из-за различий в стиле окончания строк между Windows (CRLF) и Linux (LF). Docker требует, чтобы файлы использовали LF-формат. Особенно это важно для следующих файлов:

Dockerfile
docker/start.sh
docker-compose.yml

Убедитесь, что указанные файлы используют стиль строк LF. Для этого вы можете конвертировать файлы из CRLF в LF с помощью текстового редактора, такого как:

Pycharm или VS Code

Откройте файл в VS Code или Pycharm.
Нажмите на индикатор стиля окончания строк в правом нижнем углу.
Выберите "LF" (или "Convert to LF").

Это необходимо для правильной работы контейнера Docker.
