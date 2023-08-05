from typing import Mapping, Any

from kubragen.data import Data
from kubragen.option import OptionDef
from kubragen.options import Options


class KubeResourceReportOptions(Options):
    """
    Options for the Kube Resource Report builder.

    .. list-table::
        :header-rows: 1

        * - option
          - description
          - allowed types
          - default value
        * - basename
          - object names prefix
          - str
          - ```kube-resource-report```
        * - namespace
          - namespace
          - str
          - ```monitoring```
        * - config |rarr| service_port
          - service port
          - int
          - 80
        * - config |rarr| authorization |rarr| serviceaccount_create
          - whether to create a service account
          - bool
          - ```True```
        * - config |rarr| authorization |rarr| serviceaccount_use
          - service account to use if not creating
          - str
          -
        * - config |rarr| authorization |rarr| roles_create
          - whether create roles
          - bool
          - ```True```
        * - config |rarr| authorization |rarr| roles_bind
          - whether to bind roles to service account
          - bool
          - ```True```
        * - container |rarr| kube-resource-report
          - kube-resource-report container image
          - str
          - ```quay.io/coreos/kube-resource-report:<version>```
        * - container |rarr| nginx
          - nginx container image
          - str
          - ```nginx:<version>```
        * - kubernetes |rarr| resources |rarr| deployment
          - Kubernetes Deployment resources
          - Mapping
          -
        * - kubernetes |rarr| resources |rarr| deployment-nginx
          - Kubernetes NGINX Deployment resources
          - Mapping
          -
    """
    def define_options(self):
        """
        Declare the options for the Kube Rsource Report builder.

        :return: The supported options
        """
        return {
            'basename': OptionDef(required=True, default_value='kube-resource-report', allowed_types=[str]),
            'namespace': OptionDef(required=True, default_value='monitoring', allowed_types=[str]),
            'config': {
                'service_port': OptionDef(required=True, default_value=80, allowed_types=[int]),
                'authorization': {
                    'serviceaccount_create': OptionDef(required=True, default_value=True, allowed_types=[bool]),
                    'serviceaccount_use': OptionDef(allowed_types=[str]),
                    'roles_create': OptionDef(required=True, default_value=True, allowed_types=[bool]),
                    'roles_bind': OptionDef(required=True, default_value=True, allowed_types=[bool]),
                },
            },
            'container': {
                'kube-resource-report': OptionDef(required=True,
                                                  default_value='hjacobs/kube-resource-report:20.10.0',
                                                  allowed_types=[str]),
                'nginx': OptionDef(required=True,
                                   default_value='nginx:1.19.4-alpine',
                                   allowed_types=[str]),
            },
            'kubernetes': {
                'resources': {
                    'deployment': OptionDef(allowed_types=[Mapping]),
                    'deployment-nginx': OptionDef(allowed_types=[Mapping]),
                }
            },
        }


class KubeResourceReportOptions_Default_Resources_Deployment(Data):
    """
    Default option value for:

    ```kubernetes.resources.deployment```
    """
    def is_enabled(self) -> bool:
        return True

    def get_value(self) -> Any:
        return {
            'requests': {
                'cpu': '5m',
                'memory': '50Mi'
            },
            'limits': {
                'cpu': '10m',
                'memory': '100Mi'
            },
        }


class KubeResourceReportOptions_Default_Resources_DeploymentNGINX(Data):
    """
    Default option value for:

    ```kubernetes.resources.deployment-nginx```
    """
    def is_enabled(self) -> bool:
        return True

    def get_value(self) -> Any:
        return {
            'requests': {
                'cpu': '5m',
                'memory': '20Mi'
            },
            'limits': {
                'cpu': '10m',
                'memory': '50Mi'
            },
        }
