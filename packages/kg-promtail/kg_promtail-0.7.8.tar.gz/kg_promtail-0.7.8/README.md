# KubraGen Builder: Promtail

[![PyPI version](https://img.shields.io/pypi/v/kg_promtail.svg)](https://pypi.python.org/pypi/kg_promtail/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/kg_promtail.svg)](https://pypi.python.org/pypi/kg_promtail/)

kg_promtail is a builder for [KubraGen](https://github.com/RangelReale/kubragen) that deploys 
a [Promtail](https://grafana.com/docs/loki/latest/clients/promtail/) service in Kubernetes.

Promtail is commonly used with [Loki](https://grafana.com/oss/loki/).

[KubraGen](https://github.com/RangelReale/kubragen) is a Kubernetes YAML generator library that makes it possible to generate
configurations using the full power of the Python programming language.

* Website: https://github.com/RangelReale/kg_promtail
* Repository: https://github.com/RangelReale/kg_promtail.git
* Documentation: https://kg_promtail.readthedocs.org/
* PyPI: https://pypi.python.org/pypi/kg_promtail

## Example

```python
from kubragen import KubraGen
from kubragen.consts import PROVIDER_GOOGLE, PROVIDERSVC_GOOGLE_GKE
from kubragen.object import Object
from kubragen.option import OptionRoot
from kubragen.options import Options
from kubragen.output import OutputProject, OD_FileTemplate, OutputFile_ShellScript, OutputFile_Kubernetes, \
    OutputDriver_Print
from kubragen.provider import Provider

from kg_promtail import PromtailBuilder, PromtailOptions, PromtailConfigFile, PromtailConfigFileOptions, \
    PromtailConfigFileExt_Kubernetes

kg = KubraGen(provider=Provider(PROVIDER_GOOGLE, PROVIDERSVC_GOOGLE_GKE), options=Options({
    'namespaces': {
        'mon': 'app-monitoring',
    },
}))

out = OutputProject(kg)

shell_script = OutputFile_ShellScript('create_gke.sh')
out.append(shell_script)

shell_script.append('set -e')

#
# OUTPUTFILE: app-namespace.yaml
#
file = OutputFile_Kubernetes('app-namespace.yaml')

file.append([
    Object({
        'apiVersion': 'v1',
        'kind': 'Namespace',
        'metadata': {
            'name': 'app-monitoring',
        },
    }, name='ns-monitoring', source='app', instance='app')
])

out.append(file)
shell_script.append(OD_FileTemplate(f'kubectl apply -f ${{FILE_{file.fileid}}}'))

shell_script.append(f'kubectl config set-context --current --namespace=app-monitoring')

#
# SETUP: promtail
#
promtailconfigfile = PromtailConfigFile(options=PromtailConfigFileOptions({
}), extensions=[PromtailConfigFileExt_Kubernetes()])

promtail_config = PromtailBuilder(kubragen=kg, options=PromtailOptions({
    'namespace': OptionRoot('namespaces.mon'),
    'basename': 'mypromtail',
    'config': {
        'promtail_config': promtailconfigfile,
        'loki_url': 'http://loki:3100',
    },
    'kubernetes': {
        'resources': {
            'daemonset': {
                'requests': {
                    'cpu': '150m',
                    'memory': '300Mi'
                },
                'limits': {
                    'cpu': '300m',
                    'memory': '450Mi'
                },
            },
        },
    }
}))

promtail_config.ensure_build_names(promtail_config.BUILD_ACCESSCONTROL, promtail_config.BUILD_CONFIG,
                                   promtail_config.BUILD_SERVICE)

#
# OUTPUTFILE: promtail-config.yaml
#
file = OutputFile_Kubernetes('promtail-config.yaml')
out.append(file)

file.append(promtail_config.build(promtail_config.BUILD_ACCESSCONTROL, promtail_config.BUILD_CONFIG))

shell_script.append(OD_FileTemplate(f'kubectl apply -f ${{FILE_{file.fileid}}}'))

#
# OUTPUTFILE: promtail.yaml
#
file = OutputFile_Kubernetes('promtail.yaml')
out.append(file)

file.append(promtail_config.build(promtail_config.BUILD_SERVICE))

shell_script.append(OD_FileTemplate(f'kubectl apply -f ${{FILE_{file.fileid}}}'))

#
# Write files
#
out.output(OutputDriver_Print())
# out.output(OutputDriver_Directory('/tmp/build-gke'))
```

Output:

```text
****** BEGIN FILE: 001-app-namespace.yaml ********
apiVersion: v1
kind: Namespace
metadata:
  name: app-monitoring

****** END FILE: 001-app-namespace.yaml ********
****** BEGIN FILE: 002-promtail-config.yaml ********
apiVersion: v1
kind: ServiceAccount
metadata:
  name: mypromtail
  namespace: app-monitoring
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: mypromtail
rules:
- apiGroups: ['']
  resources: [nodes, nodes/proxy, services, endpoints, pods]
  verbs: [get, watch, list]
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: mypromtail
<...more...>
****** END FILE: 002-promtail-config.yaml ********
****** BEGIN FILE: 003-promtail.yaml ********
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: mypromtail
  namespace: app-monitoring
  labels:
    app: mypromtail
spec:
  selector:
    matchLabels:
      app: mypromtail
  template:
    metadata:
      labels:
        app: mypromtail
    spec:
      serviceAccountName: mypromtail
<...more...>
****** END FILE: 003-promtail.yaml ********
****** BEGIN FILE: create_gke.sh ********
#!/bin/bash

set -e
kubectl apply -f 001-app-namespace.yaml
kubectl config set-context --current --namespace=app-monitoring
kubectl apply -f 002-promtail-config.yaml
kubectl apply -f 003-promtail.yaml

****** END FILE: create_gke.sh ********
```

## Credits

based on

[Install Loki with Helm](https://grafana.com/docs/loki/latest/installation/helm/)

## Author

Rangel Reale (rangelspam@gmail.com)
