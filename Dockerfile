FROM python:latest
RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install -r package.txt
EXPOSE 5000
CMD ["python", "main.py"]