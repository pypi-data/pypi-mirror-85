# KubraGen Builder: Kube Resource Report

[![PyPI version](https://img.shields.io/pypi/v/kg_kuberesourcereport.svg)](https://pypi.python.org/pypi/kg_kuberesourcereport/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/kg_kuberesourcereport.svg)](https://pypi.python.org/pypi/kg_kuberesourcereport/)

kg_kuberesourcereport is a builder for [KubraGen](https://github.com/RangelReale/kubragen) that deploys 
a [Kube Resource Report](https://codeberg.org/hjacobs/kube-resource-report) service in Kubernetes.

[KubraGen](https://github.com/RangelReale/kubragen) is a Kubernetes YAML generator library that makes it possible to generate
configurations using the full power of the Python programming language.

* Website: https://github.com/RangelReale/kg_kuberesourcereport
* Repository: https://github.com/RangelReale/kg_kuberesourcereport.git
* Documentation: https://kg_kuberesourcereport.readthedocs.org/
* PyPI: https://pypi.python.org/pypi/kg_kuberesourcereport

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

from kg_kuberesourcereport import KubeResourceReportBuilder, KubeResourceReportOptions, \
    KubeResourceReportOptions_Default_Resources_Deployment, KubeResourceReportOptions_Default_Resources_DeploymentNGINX

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
# SETUP: kube-resource-report
#
ksm_config = KubeResourceReportBuilder(kubragen=kg, options=KubeResourceReportOptions({
    'namespace': OptionRoot('namespaces.mon'),
    'basename': 'myksm',
    'config': {
    },
    'kubernetes': {
        'resources': {
            'deployment': KubeResourceReportOptions_Default_Resources_Deployment(),
            'deployment-nginx': KubeResourceReportOptions_Default_Resources_DeploymentNGINX(),
        },
    }
}))

ksm_config.ensure_build_names(ksm_config.BUILD_ACCESSCONTROL, ksm_config.BUILD_SERVICE)

#
# OUTPUTFILE: KubeResourceReport-config.yaml
#
file = OutputFile_Kubernetes('kuberesourcereport-config.yaml')
out.append(file)

file.append(ksm_config.build(ksm_config.BUILD_ACCESSCONTROL))

shell_script.append(OD_FileTemplate(f'kubectl apply -f ${{FILE_{file.fileid}}}'))

#
# OUTPUTFILE: KubeResourceReport.yaml
#
file = OutputFile_Kubernetes('KubeResourceReport.yaml')
out.append(file)

file.append(ksm_config.build(ksm_config.BUILD_SERVICE))

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
****** BEGIN FILE: 002-kuberesourcereport-config.yaml ********
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myksm
  namespace: app-monitoring
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: myksm
rules:
- apiGroups: ['']
  resources: [nodes, pods, namespaces, services]
  verbs: [get, list]
<...more...>
****** END FILE: 002-kuberesourcereport-config.yaml ********
****** BEGIN FILE: 003-KubeResourceReport.yaml ********
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myksm
  namespace: app-monitoring
  labels:
    app: myksm
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myksm
  template:
    metadata:
      labels:
        app: myksm
    spec:
      serviceAccountName: myksm
      containers:
      - name: kube-resource-report
        image: hjacobs/kube-resource-report:20.10.0
        args: [--update-interval-minutes=1, --additional-cost-per-cluster=30.0, /output]
<...more...>
****** END FILE: 003-KubeResourceReport.yaml ********
****** BEGIN FILE: create_gke.sh ********
#!/bin/bash

set -e
kubectl apply -f 001-app-namespace.yaml
kubectl config set-context --current --namespace=app-monitoring
kubectl apply -f 002-kuberesourcereport-config.yaml
kubectl apply -f 003-KubeResourceReport.yaml

****** END FILE: create_gke.sh ********
```

### Credits

based on

[codeberg.org/hjacobs/kube-resource-report](https://codeberg.org/hjacobs/kube-resource-report)

## Author

Rangel Reale (rangelreale@gmail.com)
