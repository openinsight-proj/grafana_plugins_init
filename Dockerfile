FROM busybox:1.35

WORKDIR /app

COPY /plugins /app/plugins
COPY /dashboards /app/dashboards

CMD unzip -o /app/plugins/marcusolsson-json-datasource-1.3.10.zip -d /opt/plugins && cp -r /app/dashboards /opt/plugins