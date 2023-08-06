FROM python:3.7-slim

COPY ./docker/prod/python/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

WORKDIR /{{params['project_name']}}

COPY ./{{params['project_name']}}/requirements /{{params['project_name']}}/requirements

COPY ./{{params['project_name']}} /{{params['project_name']}}

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r requirements/prod_requirements.txt

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
