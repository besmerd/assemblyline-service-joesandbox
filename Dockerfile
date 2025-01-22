FROM cccs/assemblyline-v4-service-base:latest

ENV SERVICE_PATH joesandbox.JoeSandbox

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --user --requirement requirements.txt && rm -rf ~/.cache/pip

ARG version=4.5.1.dev1
RUN sed -i -e "s/\$SERVICE_TAG/$version/g" service_manifest.yml

USER assemblyline

WORKDIR /opt/al_service
COPY joesandbox.py .
