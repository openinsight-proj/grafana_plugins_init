FROM quay.io/grafana-operator/grafana_plugins_init:0.0.6

WORKDIR /app

COPY /plugins /app/plugins

CMD [ "unzip", "/app/plugins/marcusolsson-json-datasource-1.3.10.zip", "-d", "/opt/plugins" ]
