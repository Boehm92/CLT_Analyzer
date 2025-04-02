# Basis-Image mit Python 3.8
FROM python:3.8.14-bullseye

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Kopiere das Requirements-File und installiere die Abhängigkeiten
COPY requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir -r /app/requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

# Kopiere den gesamten Code in das Container-Verzeichnis
COPY scripts/ /app/scripts/

# Setze die Umgebungsvariablen für das Training
ENV PYTHONPATH=/app/scripts
ENV DATA_FOLDER=${DATA_FOLDER}
ENV TRAINING_DATASET_SOURCE=${TRAINING_DATASET_SOURCE}

# Setze den Einstiegspunkt auf das __main__.py Script
CMD ["python", "scripts/__main__.py"]
