
.PHONY: remove-dashbaords
remove-dashbaords:
	rm -rf ../dashboards/

.PHONY: remove-dashbaords
gen-dashboards: remove-dashbaords
	docker run --rm -v $$(pwd)/dashboards:/dashboards -v $$(pwd)/hack:/hack -it python:3.11.9 /bin/sh -c \
	'cd hack && pip install -r requirements.txt && python sync_grafana_dashboards.py'

build-image-darwin:
	docker buildx build --platform linux/amd64 -t release-ci.daocloud.io/insight/grafana_plugins_init:dev .

build-image-liunx:
	docker buildx build --platform linux/amd64 -t release-ci.daocloud.io/insight/grafana_plugins_init:dev .