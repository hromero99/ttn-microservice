FROM python:3.9.6
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80","--reload-include","*.py"]