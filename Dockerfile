FROM python:3.7.3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 0

RUN pip install --no-cache-dir coverage
RUN pip install --no-cache-dir codecov
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash"]