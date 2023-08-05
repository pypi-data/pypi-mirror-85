# KubraGen Builder: Ingress NGINX

[![PyPI version](https://img.shields.io/pypi/v/kg_ingressnginx.svg)](https://pypi.python.org/pypi/kg_ingressnginx/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/kg_ingressnginx.svg)](https://pypi.python.org/pypi/kg_ingressnginx/)

kg_ingressnginx is a builder for [KubraGen](https://github.com/RangelReale/kubragen) that deploys 
a [Ingress NGINX](https://github.com/kubernetes/ingress-nginx) server in Kubernetes.

[KubraGen](https://github.com/RangelReale/kubragen) is a Kubernetes YAML generator library that makes it possible to generate
configurations using the full power of the Python programming language.

* Website: https://github.com/RangelReale/kg_ingressnginx
* Repository: https://github.com/RangelReale/kg_ingressnginx.git
* Documentation: https://kg_ingressnginx.readthedocs.org/
* PyPI: https://pypi.python.org/pypi/kg_ingressnginx

## Example

```python
from kubragen import KubraGen
from kubragen.consts import PROVIDER_GOOGLE, PROVIDERSVC_GOOGLE_GKE
from kubragen.object import Object
from kubragen.options import Options
from kubragen.output import OutputProject, OD_FileTemplate, OutputFile_ShellScript, OutputFile_Kubernetes, \
    OutputDriver_Print
from kubragen.provider import Provider

from kg_ingressnginx import IngressNGINXBuilder, IngressNGINXOptions

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
# SETUP: ingressnginx
#
ingressnginx_config = IngressNGINXBuilder(kubragen=kg, options=IngressNGINXOptions({
}))

ingressnginx_config.ensure_build_names(ingressnginx_config.BUILD_INGRESS)

#
# OUTPUTFILE: ingressnginx.yaml
#
file = OutputFile_Kubernetes('ingressnginx.yaml')
out.append(file)

file.append(ingressnginx_config.build(ingressnginx_config.BUILD_INGRESS))

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
****** BEGIN FILE: 002-ingressnginx.yaml ********
apiVersion: v1
kind: Namespace
metadata:
  name: ingress-nginx
  labels:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
---
apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    helm.sh/chart: ingress-nginx-3.6.0
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 0.40.2
    app.kubernetes.io/managed-by: Helm
<...more...>
****** END FILE: 002-ingressnginx.yaml ********
****** BEGIN FILE: create_gke.sh ********
#!/bin/bash

set -e
kubectl apply -f 001-app-namespace.yaml
kubectl config set-context --current --namespace=app-monitoring
kubectl apply -f 002-ingressnginx.yaml

****** END FILE: create_gke.sh ********
```

### Credits

Based on

[ingress-nginx deploy](https://kubernetes.github.io/ingress-nginx/deploy/)

[kubernetes/ingress-nginx](https://github.com/kubernetes/ingress-nginx)

## Author

Rangel Reale (rangelreale@gmail.com)
