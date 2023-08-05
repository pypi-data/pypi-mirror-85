from typing import Optional, Any, Mapping

from kubragen.configfile import ConfigFile
from kubragen.data import Data
from kubragen.option import OptionDef
from kubragen.options import Options


class PromtailOptions(Options):
    """
    Options for the Promtail builder.

    .. list-table::
        :header-rows: 1

        * - option
          - description
          - allowed types
          - default value
        * - basename
          - object names prefix
          - str
          - ```promtail```
        * - namespace
          - namespace
          - str
          - ```monitoring```
        * - config |rarr| prometheus_annotation
          - add prometheus annotations
          - bool
          - ```False```
        * - config |rarr| promtail_config
          - Promtail config file
          - str, ConfigFile
          - :class:`kg_promtail.PromtailConfigFile`
        * - config |rarr| loki_url
          - Loki url (with http://)
          - str
          -
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
        * - container |rarr| promtail
          - promtail container image
          - str
          - ```grafana/promtail:<version>```
        * - kubernetes |rarr| resources |rarr| daemonset
          - Kubernetes StatefulSet resources
          - dict
          -
    """
    def define_options(self) -> Optional[Any]:
        """
        Declare the options for the Promtail builder.

        :return: The supported options
        """
        return {
            'basename': OptionDef(required=True, default_value='promtail', allowed_types=[str]),
            'namespace': OptionDef(required=True, default_value='monitoring', allowed_types=[str]),
            'config': {
                'prometheus_annotation': OptionDef(required=True, default_value=False, allowed_types=[bool]),
                'promtail_config': OptionDef(allowed_types=[str, ConfigFile]),
                'loki_url': OptionDef(allowed_types=[str]),
                'authorization': {
                    'serviceaccount_create': OptionDef(required=True, default_value=True, allowed_types=[bool]),
                    'serviceaccount_use': OptionDef(allowed_types=[str]),
                    'roles_create': OptionDef(required=True, default_value=True, allowed_types=[bool]),
                    'roles_bind': OptionDef(required=True, default_value=True, allowed_types=[bool]),
                },
            },
            'container': {
                'promtail': OptionDef(required=True, default_value='grafana/promtail:2.0.0', allowed_types=[str]),
            },
            'kubernetes': {
                'resources': {
                    'daemonset': OptionDef(allowed_types=[Mapping]),
                }
            },
        }


class PromtailOptions_Default_Resources_DaemonSet(Data):
    """
    Default option value for:

    ```kubernetes.resources.daemonset```
    """
    def is_enabled(self) -> bool:
        return True

    def get_value(self) -> Any:
        return {
            'requests': {
                'cpu': '100m',
                'memory': '128Mi'
            },
            'limits': {
                'cpu': '200m',
                'memory': '128Mi'
            },
        }