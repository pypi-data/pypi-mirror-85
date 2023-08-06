version: '3'
services:
  {{ params['project_name'] }}_python: &{{ params['project_name'] }}_python
    build:
      context: .
      dockerfile: docker/prod/python/Dockerfile
    environment:
      - DJANGO_SETTINGS_MODULE={{ params['project_name'] }}.settings.prod
    volumes:
    - ./{{ params['project_name'] }}:/{{params['project_name']}}
     - ~/.aws/:/root/.aws
    ports:
    - 8000:8000
    command: gunicorn -w 4 {{ params['project_name'] }}.wsgi -b 0.0.0.0:8000
    depends_on:
      - {{params['project_name'] }}_rabbitmq
      - {{params['project_name'] }}_celery_worker_default
  {{ params['project_name'] }}_rabbitmq:
    image: rabbitmq:3.7-alpine
  {{params['project_name'] }}_celery_worker_default:
    <<: *{{ params['project_name'] }}_python # up to copy of instance
    command: celery -A {{params['project_name'] }} worker --loglevel=info
    ports: []
    depends_on:
      - {{ params['project_name'] }}_rabbitmq
  {{params['project_name'] }}_celery_beat:
    <<: *{{params['project_name'] }}_python # up to copy of instance
    command: celery -A {{params['project_name'] }} beat --loglevel=info
    ports: []
    depends_on:
      - {{params['project_name'] }}_rabbitmq
      - {{params['project_name'] }}_celery_worker_default
