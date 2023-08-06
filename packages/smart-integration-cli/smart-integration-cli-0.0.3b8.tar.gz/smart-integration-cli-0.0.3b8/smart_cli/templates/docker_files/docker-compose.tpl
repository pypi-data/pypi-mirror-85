version: '3'
volumes:
  pgdata:
services:
  {{params['project_name'] }}_python: &{{params['project_name'] }}_python # link to instance
    build:
      context: .
      dockerfile: docker/local/python/Dockerfile
    volumes:
    - ./{{params['project_name'] }}:/{{ params['project_name'] }}
    - ~/.aws/:/root/.aws
    ports:
    - 8000:8000
    environment:
      DJANGO_SETTINGS_MODULE: '{{params['project_name'] }}.settings.dev'
      # # You can change which AWS CLI Profile is used
      AWS_PROFILE: "default"
    command: python manage.py runserver 0.0.0.0:8000
    depends_on:
      - postgres
      - {{params['project_name'] }}_rabbitmq
      - {{params['project_name'] }}_celery_worker_default
  postgres:
    image: postgres:10.3-alpine
    restart: always
    environment:
      POSTGRES_USER: test
      POSTGRES_DB: test
      POSTGRES_PASSWORD: test
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - 5434:5432
  {{params['project_name'] }}_rabbitmq:
    image: rabbitmq:3.7-alpine
  {{params['project_name'] }}_celery_worker_default:
    <<: *{{params['project_name'] }}_python # up to copy of instance
    command: celery -A {{params['project_name'] }} worker --loglevel=info
    ports: []
    depends_on:
      - postgres
      - {{params['project_name'] }}_rabbitmq
  {{params['project_name'] }}_celery_beat:
    <<: *{{params['project_name'] }}_python # up to copy of instance
    command: celery -A {{params['project_name'] }} beat --loglevel=info
    ports: []
    depends_on:
      - {{params['project_name'] }}_rabbitmq
      - {{params['project_name'] }}_celery_worker_default
