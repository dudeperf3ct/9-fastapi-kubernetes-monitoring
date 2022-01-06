FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements-tests.txt /app/requirements-tests.txt

RUN pip3 install --no-cache-dir -r requirements-tests.txt

COPY setup.py /app/setup.py

RUN pip install .

COPY . .

EXPOSE 8000

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app.app:app"]