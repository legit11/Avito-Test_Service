FROM python:3.12-slim

RUN mkdir /avito

WORKDIR /avito

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

EXPOSE 8080

CMD ["sh", "/avito/docker/start.sh"]