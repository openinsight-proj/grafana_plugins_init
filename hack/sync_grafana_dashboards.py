#!/usr/bin/env python3
"""Fetch dashboards from provided urls into this chart."""
import re
import json
import textwrap
from os import makedirs, path

import requests
import yaml
from yaml.representer import SafeRepresenter


# https://stackoverflow.com/a/20863889/961092
class LiteralStr(str):
    pass


# def change_style(style, representer):
#     def new_representer(dumper, data):
#         scalar = representer(dumper, data)
#         scalar.style = style
#         return scalar
#
#     return new_representer


# Source files list
charts = [
    {
        'name': 'fluent-bit',
        'source': './resources/insight-system/insight_agent_fluentbit.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True,
    },
    {
        'name': 'otel-collector',
        'source': './resources/insight-system/insight_otel_collector.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True,
    },
    {
        'name': 'jaeger-collector',
        'source': 'https://raw.githubusercontent.com/jaegertracing/jaeger/main/monitoring/jaeger-mixin/dashboard-for-grafana.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True,
    },
    {
        'name': 'tracing-debug',
        'source': './resources/insight-system/insight_tracing_debug.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True,
    },
    {
        'name': 'agent-otel-collector',
        'source': './resources/insight-system/insight_agent_otel_collector.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
    },
    {
        'name': 'logging-usage',
        'source': './resources/insight-system/insight_es_usage.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True,
    },
    {
        'name': 'victoriametrics-cluster',
        'source': './resources/insight-system/victoriametrics-cluster.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
    },

    {
        'source': 'https://raw.githubusercontent.com/prometheus-operator/kube-prometheus/main/manifests/grafana-dashboardDefinitions.yaml',
        'destination': '../dashboards/insight-system',
        'type': 'yaml',
    },
    {
        'source': 'https://etcd.io/docs/v3.4/op-guide/grafana.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
    },
    {
        'source': 'https://raw.githubusercontent.com/VictoriaMetrics/VictoriaMetrics/master/dashboards/victoriametrics.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
    },
    {
        'source': 'https://raw.githubusercontent.com/VictoriaMetrics/VictoriaMetrics/master/dashboards/vmalert.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
    },
    {
        'source': 'https://raw.githubusercontent.com/dotdc/grafana-dashboards-kubernetes/master/dashboards/k8s-system-coredns.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
    },
    {
        'name': 'insight-overview-en',
        'source': './resources/insight-system/insight_overview_en.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
    },
    {
        'name': 'insight-overview-zh',
        'source': './resources/insight-system/insight_overview_zh.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
    },
    {
        'name': 'namespace-overview-en',
        'source': './resources/insight-system/namespace_overview_en.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
    },
    {
        'name': 'namespace-overview-zh',
        'source': './resources/insight-system/namespace_overview_zh.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
    },
    {
        'name': 'probe-overview-en',
        'source': './resources/insight-system/probe_overview_en.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
    },
    {
        'name': 'probe-overview-zh',
        'source': './resources/insight-system/probe_overview_zh.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
    },
    {
        'name': 'gpu-cluster',
        'source': './resources/insight-system/gpu-cluster.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True
    },
    {
        'name': 'gpu-node',
        'source': './resources/insight-system/gpu-node.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True
    },
    {
        'name': 'gpu-pod',
        'source': './resources/insight-system/gpu-pod.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True
    },
    {
        'name': 'ascend',
        'source': './resources/insight-system/ascend.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True
    },
    {
        'name': 'calico',
        'source': './resources/insight-system/calico.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True
    },
    {
        'name': 'contour',
        'source': './resources/insight-system/contour.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True
    },
    {
        'name': 'egress',
        'source': './resources/insight-system/egress.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True
    },
    {
        'name': 'hwamei',
        'source': './resources/insight-system/hwamei.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True
    },
    {
        'name': 'ingress',
        'source': './resources/insight-system/ingress.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True
    },
    {
        'name': 'jvm-monitoring-exporter-en',
        'source': './resources/insight-system/jvm-monitoring-exporter-en.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True
    },
    {
        'name': 'jvm-monitoring-exporter-zh',
        'source': './resources/insight-system/jvm-monitoring-exporter-zh.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True
    },
    {
        'name': 'jvm-monitoring-otel-en',
        'source': './resources/insight-system/jvm-monitoring-otel-en.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True
    },
    {
        'name': 'jvm-monitoring-otel-zh',
        'source': './resources/insight-system/jvm-monitoring-otel-zh.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True
    },
    {
        'name': 'metallb',
        'source': './resources/insight-system/metallb.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True
    },
    {
        'name': 'spiderpool',
        'source': './resources/insight-system/spiderpool.json',
        'destination': '../dashboards/insight-system',
        'type': 'json',
        'ignore_patch': True
    },

]

skip_list = [
    "prometheus.json",
    "prometheus-remote-write.json"
]

# Additional conditions map
# condition_map = {
#     'grafana-coredns-k8s': '(index .Values "dashboards" "coreDns")',
#     'etcd': '(index .Values "dashboards" "kubeEtcd")',
#     'apiserver': '(index .Values "dashboards" "kubeApiServer")',
#     'controller-manager': '(index .Values "dashboards" "kubeControllerManager")',
#     'kubelet': '(index .Values "dashboards" "kubelet")',
#     'proxy': '(index .Values "dashboards" "kubeProxy")',
#     'scheduler': '(index .Values "dashboards" "kubeScheduler")',
#     'node-rsrc-use': '(index .Values "dashboards" "prometheus-node-exporter")',
#     'node-cluster-rsrc-use': '(index .Values "dashboards" "prometheus-node-exporter")',
#     'victoriametrics-cluster': '(index .Values "dashboards" "vmcluster")',
#     'victoriametrics': '(index .Values "dashboards" "vmsingle")',
#     'vmalert': '(index .Values "dashboards" "vmalert")',
#     'vmagent': '(index .Values "dashboards" "vmagent")',
#     'fluent-bit': '(index .Values "dashboards" "fluentBit")',
#     'agent-otel-collector': '(index .Values "dashboards" "agentOtelCollector")',
#     'otel-collector': '(index .Values "dashboards" "otelCollector")',
#     'nodes-darwin': '(index .Values "dashboards" "nodes-darwin")',
#     'jaeger-collector': '(index .Values "dashboards" "jaegerCollector")',
#     'tracing-debug': '(index .Values "dashboards" "tracingDebug")',
#     'insight-logging': '(index .Values "dashboards" "insightLogging")'
# }

# standard header
# header = '''{{- /*
# Generated from '%(name)s' from %(url)s
# Do not change in-place! In order to change this file first read following link:
# https://gitlab.daocloud.cn/ndx/engineering/insight/insight/-/tree/main/hack
# */ -}}
# {{- %(condition)s }}
# apiVersion: integreatly.org/v1alpha1
# kind: GrafanaDashboard
# metadata:
#   namespace: {{ .Release.Namespace }}
#   name: {{ printf "%%s-%%s" (include "dashboard.fullname" $) "%(name)s" | trunc 63 | trimSuffix "-" | trimSuffix "." }}
#   labels:
# {{ include "dashboard.common.labels" $ | indent 4 }}
#     {{- if (index $ "Values" "dashboards" "label") }}
#     {{ (index $ "Values" "dashboards" "label") }}: "1"
#     {{- end }}
#     {{- if (index $ "Values" "dashboards" "additionalDashboardLabels") }}
#     {{- range $key, $val := (index .Values "dashboards" "additionalDashboardLabels") }}
#     {{ $key }}: {{ $val | quote }}
#     {{- end }}
#     {{- end }}
#     app: {{ include "dashboard.name" $ }}-grafana-operator
#     {{- if (index $ "Values" "dashboards" "additionalDashboardAnnotations") }}
#   annotations:
#     {{- range $key, $val := (index .Values "dashboards" "additionalDashboardAnnotations") }}
#     {{ $key }}: {{ $val | quote }}
#     {{- end }}
#     {{- end }}
# spec:
# '''

templating_cluster_name = '''{
  "allValue": null,
  "current": {
    "text": "",
    "value": ""
  },
  "datasource": {
    "type": "prometheus",
    "uid": ""
  },
  "definition": "query_result(count(global_cluster_info) by (cluster_name))",
  "hide": ":multicluster:",
  "includeAll": false,
  "label": "Cluster",
  "multi": false,
  "name": "cluster_name",
  "options": [],
  "query": {
    "query": "query_result(count(global_cluster_info) by (cluster_name))",
    "refId": "Prometheus-cluster_name-Variable-Query"
  },
  "refresh": 2,
  "regex": "/\\"([^\\"]+)\\"/",
  "sort": 1,
  "tagValuesQuery": "",
  "tags": [],
  "tagsQuery": "",
  "type": "query",
  "useTags": false
}'''


# def init_yaml_styles():
#     represent_literal_str = change_style('|', SafeRepresenter.represent_str)
#     yaml.add_representer(LiteralStr, represent_literal_str)


# def escape(s):
#     return s.replace("{{", "{{`{{").replace("}}", "}}`}}").replace("{{`{{", "{{`{{`}}").replace("}}`}}", "{{`}}`}}")
#
#
# def unescape(s):
#     return s.replace("\{\{", "{{").replace("\}\}", "}}")


# def yaml_str_repr(struct, indent=2):
#     """represent yaml as a string"""
#     text = yaml.dump(
#         struct,
#         width=1000,  # to disable line wrapping
#         default_flow_style=False  # to disable multiple items on single line
#     )
#     text = escape(text)  # escape {{ and }} for helm
#     text = unescape(text)  # unescape \{\{ and \}\} for templating
#     text = textwrap.indent(text, ' ' * indent)
#     return text


def convert_cluster_name_to_linkUrl(key, content_struct):
    try:
        if key == 'rows':
            rows = content_struct[key]
            for row in rows:
                convert_cluster_name_to_linkUrl('panels', row)
        if key == 'panels':
            panels = content_struct.get(key)
            for panel in panels:
                styles = panel.get('styles', '')
                if styles:
                    for style in styles:
                        url = style.get('linkUrl', '')
                        if url:
                            style['linkUrl'] = url + "&var-cluster_name=$cluster_name"
    except Exception as e:
        print("[Error] ", e)


def convert_cluster_to_cluster_name(content_struct):
    """dirty change"""
    tpl_list = content_struct['templating']['list']
    cluster_idx, cluster_name_idx = -1, -1
    try:
        for idx, var in enumerate(tpl_list):
            if var['name'] == 'cluster':
                cluster_idx = idx;
            elif var['name'] == 'cluster_name':
                cluster_name_idx = idx;

        if cluster_idx != -1:
            var = tpl_list[cluster_idx]
            # use our cluster define and hide it
            var['hide'] = 2  # hide this
            var['query'] = {
                "query": "query_result(count(global_cluster_info{cluster_name=\"$cluster_name\"}) by (cluster))",
                "refId": "Prometheus-cluster-Variable-Query"
            }
            var['definition'] = "query_result(count(global_cluster_info{cluster_name=\"$cluster_name\"}) by (cluster))"
            var['regex'] = "/\"([^\"]+)\"/"

            # add cluster_name var into rows[0].panels[0].styles[0].linkUrl
            if content_struct.get('rows'):
                convert_cluster_name_to_linkUrl('rows', content_struct)

            # add cluster_name var into panels[0].styles[0].linkUrl
            if content_struct.get('panels'):
                convert_cluster_name_to_linkUrl('panels', content_struct)

            tpl_cluster_name = json.loads(templating_cluster_name)
            if cluster_name_idx != -1:
                # cluster_name already exists, replace it
                tpl_list[cluster_name_idx] = tpl_cluster_name
            else:
                # cluster_name not exists, append it after cluster
                tpl_list.insert(cluster_idx + 1, tpl_cluster_name)


    except Exception as e:
        print("[Error] ", e)


def convert_hide_datasource_select(content_struct):
    """dirty change"""
    tpl_list = content_struct['templating']['list']
    try:
        for var in tpl_list:
            if var['name'] == 'datasource' or var['name'] == 'ds':
                # hide all datasource select
                var['hide'] = 2  # hide this
    except Exception as e:
        print("[Error] ", e)


def patch_dashboards_json(content, ignore_patch=False):
    try:
        content_struct = json.loads(content)

        if not ignore_patch:
            # hide datasource select
            convert_hide_datasource_select(content_struct)

            # make single-cluster to multi-cluster
            convert_cluster_to_cluster_name(content_struct)

        # make dashboards readonly
        content_struct['editable'] = False

        # add common tag
        content_struct['tags'].append('vm-k8s-stack')

        # fix drilldown links. see https://github.com/kubernetes-monitoring/kubernetes-mixin/issues/659
        # print(type(content_struct['rows']))
        if content_struct.get('rows'):
            for row in content_struct['rows']:
                for panel in row['panels']:
                    for style in panel.get('styles', []):
                        if 'linkUrl' in style and style['linkUrl'].startswith('./d'):
                            style['linkUrl'] = style['linkUrl'].replace(
                                './d', '/d')

        # grafana's json to helm yaml template
        content_array = []
        original_content_lines = content.split('\n')
        for i, line in enumerate(json.dumps(content_struct, indent=4).split('\n')):
            if '[]' not in line and '{}' not in line:
                content_array.append(line)
                continue

            append = ''
            if line.endswith(','):
                line = line[:-1]
                append = ','

            if line.endswith('{}') or line.endswith('[]'):
                content_array.append(line[:-1])
                content_array.append('')
                content_array.append(
                    ' ' * (len(line) - len(line.lstrip())) + line[-1] + append)

        content = '\n'.join(content_array)

        multicluster = content.find(':multicluster:')
        if multicluster != -1:
            content = ''.join((content[:multicluster - 1], "0", content[multicluster + 15:]))

        timezone = content.find('"timezone": "UTC",')
        if timezone == -1:
            timezone = content.find('"timezone": "utc",')

        if timezone != -1:
            content = ''.join((
                content[:timezone],
                '"timezone": "",',
                content[timezone + 18:]
            ))
    except (ValueError, KeyError) as e:
        print("[Error] ", e)

    return content


def write_dashboard_to_file(resource_name, content, destination, ignore_patch=False):
    content = patch_dashboards_json(content, ignore_patch)

    new_filename = "%s/%s" % (destination,  resource_name + '.json')

    # make sure directories to store the file exist
    makedirs(destination, exist_ok=True)

    # recreate the file
    with open(new_filename, 'w') as f:
        f.write(content)

    print("Generated %s" % new_filename)


def is_local_file(path):
    return not re.match(r'http(s)+:\/\/', path)




def main():
    # init_yaml_styles()
    # read the rules, create a new template file per group
    for chart in charts:
        print("Generating dashboards from %s" % chart['source'])
        if is_local_file(chart['source']):
            file = open(chart['source'], mode='r')
            raw_text = file.read()
            file.close()
        else:
            response = requests.get(chart['source'])
            if response.status_code != 200:
                print('Skipping the file, response code %s not equals 200' %
                      response.status_code)
                continue
            raw_text = response.text

        resource_name = chart.get('name', path.basename(chart['source']).replace('.json', ''))
        destination = chart.get('destination')
        ignore_patch = chart.get('ignore_patch')

        if chart['type'] == 'yaml':
            yaml_text = yaml.full_load(raw_text)
            groups = yaml_text['items']
            for group in groups:
                for resource, content in group['data'].items():
                    if resource in skip_list:
                        continue
                    write_dashboard_to_file(resource.replace('.json', ''), content, destination, ignore_patch)
        elif chart['type'] == 'json':
            json_text = json.loads(raw_text)
            # is it already a dashboard structure or is it nested (etcd case)?
            flat_structure = bool(json_text.get('annotations'))
            if flat_structure:
                write_dashboard_to_file(resource_name, json.dumps(json_text, indent=4), destination, ignore_patch)
            else:
                for resource, content in json_text.items():
                    write_dashboard_to_file(resource.replace('.json', ''), json.dumps(content, indent=4), destination, ignore_patch)
    print("Finished")


if __name__ == '__main__':
    main()
