ARG branch=latest
FROM cccs/assemblyline-v4-service-base:latest

ENV SERVICE_PATH joesandbox.JoeSandbox

USER assemblyline

WORKDIR /opt/al_service
COPY . .

USER root
ARG version=4.5.1.dev1
RUN sed -i -e "s/\$SERVICE_TAG/$version/g" service_manifest.yml

USER assemblyline
