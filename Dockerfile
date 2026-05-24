FROM python:3.11

WORKDIR /code

COPY code/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY code/ .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]