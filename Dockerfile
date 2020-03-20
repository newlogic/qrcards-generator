FROM python:3.8

RUN apt-get update
RUN apt-get install -fy librsvg2-bin mupdf-tools

COPY requirements.txt .
RUN pip install -U pip && \
    pip install -r requirements.txt

WORKDIR /app

COPY . /app

ENTRYPOINT ["python", "generate_qr_cards.py"]
