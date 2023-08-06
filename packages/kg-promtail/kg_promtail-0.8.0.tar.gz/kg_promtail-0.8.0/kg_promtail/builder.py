from typing import Optional, Sequence

from kubragen import KubraGen
from kubragen.builder import Builder
from kubragen.configfile import ConfigFileRenderMulti, ConfigFileRender_Yaml, ConfigFileRender_RawStr
from kubragen.data import ValueData
from kubragen.exception import InvalidParamError, InvalidNameError
from kubragen.helper import LiteralStr, QuotedStr
from kubragen.object import ObjectItem, Object
from kubragen.types import TBuild, TBuildItem

from .configfile import PromtailConfigFile
from .option import PromtailOptions


class PromtailBuilder(Builder):
    """
    Promtail builder.

    Based on `Install Loki with Helm <https://grafana.com/docs/loki/latest/installation/helm/>`_.

    .. list-table::
        :header-rows: 1

        * - build
          - description
        * - BUILD_ACCESSCONTROL
          - creates service account, roles, and roles bindings
        * - BUILD_CONFIG
          - creates ConfigMap and Secret
        * - BUILD_SERVICE
          - creates deployments and services

    .. list-table::
        :header-rows: 1

        * - build item
          - description
        * - BUILDITEM_CONFIG
          - ConfigMap
        * - BUILDITEM_SERVICE_ACCOUNT
          - ServiceAccount
        * - BUILDITEM_CLUSTER_ROLE
          - ClusterRole
        * - BUILDITEM_CLUSTER_ROLE_BINDING
          - ClusterRoleBinding
        * - BUILDITEM_DAEMONSET
          - Daemonset

    .. list-table::
        :header-rows: 1

        * - object name
          - description
          - default value
        * - config
          - ConfigMap
          - ```<basename>-config```
        * - service-account
          - ServiceAccount
          - ```<basename>```
        * - cluster-role
          - cluster role
          - ```<basename>```
        * - cluster-role-binding
          - cluster role binding
          - ```<basename>```
        * - daemonset
          - DaemonSet
          - ```<basename>```
        * - pod-label-app
          - label *app* to be used by selection
          - ```<basename>```
    """
    options: PromtailOptions
    configfile: Optional[str]
    _namespace: str

    SOURCE_NAME = 'kg_promtail'

    BUILD_ACCESSCONTROL = TBuild('accesscontrol')
    BUILD_CONFIG = TBuild('config')
    BUILD_SERVICE = TBuild('service')

    BUILDITEM_CONFIG = TBuildItem('config')
    BUILDITEM_SERVICE_ACCOUNT = TBuildItem('service-account')
    BUILDITEM_CLUSTER_ROLE = TBuildItem('cluster-role')
    BUILDITEM_CLUSTER_ROLE_BINDING = TBuildItem('cluster-role-binding')
    BUILDITEM_DAEMONSET = TBuildItem('daemonset')

    def __init__(self, kubragen: KubraGen, options: Optional[PromtailOptions] = None):
        super().__init__(kubragen)
        if options is None:
            options = PromtailOptions()
        self.options = options
        self.configfile = None

        self._namespace = self.option_get('namespace')

        if self.option_get('config.authorization.serviceaccount_create') is not False:
            serviceaccount_name = self.basename()
        else:
            serviceaccount_name = self.option_get('config.authorization.serviceaccount_use')
            if serviceaccount_name == '':
                serviceaccount_name = None

        if self.option_get('config.authorization.roles_bind') is not False:
            if serviceaccount_name is None:
                raise InvalidParamError('To bind roles a service account is required')

        self.object_names_init({
            'config': self.basename('-config'),
            'service-account': serviceaccount_name,
            'cluster-role': self.basename(),
            'cluster-role-binding': self.basename(),
            'daemonset': self.basename(),
            'pod-label-app': self.basename(),
        })

    def option_get(self, name: str):
        return self.kubragen.option_root_get(self.options, name)

    def basename(self, suffix: str = ''):
        return '{}{}'.format(self.option_get('basename'), suffix)

    def namespace(self):
        return self._namespace

    def build_names(self) -> Sequence[TBuild]:
        return [self.BUILD_ACCESSCONTROL, self.BUILD_CONFIG, self.BUILD_SERVICE]

    def build_names_required(self) -> Sequence[TBuild]:
        ret = [self.BUILD_CONFIG, self.BUILD_SERVICE]
        if self.option_get('config.authorization.serviceaccount_create') is not False or \
                self.option_get('config.authorization.roles_create') is not False:
            ret.append(self.BUILD_ACCESSCONTROL)
        return ret

    def builditem_names(self) -> Sequence[TBuildItem]:
        return [
            self.BUILDITEM_CONFIG,
            self.BUILDITEM_SERVICE_ACCOUNT,
            self.BUILDITEM_CLUSTER_ROLE,
            self.BUILDITEM_CLUSTER_ROLE_BINDING,
            self.BUILDITEM_DAEMONSET,
        ]

    def internal_build(self, buildname: TBuild) -> Sequence[ObjectItem]:
        if buildname == self.BUILD_ACCESSCONTROL:
            return self.internal_build_accesscontrol()
        elif buildname == self.BUILD_CONFIG:
            return self.internal_build_config()
        elif buildname == self.BUILD_SERVICE:
            return self.internal_build_service()
        else:
            raise InvalidNameError('Invalid build name: "{}"'.format(buildname))

    def internal_build_accesscontrol(self) -> Sequence[ObjectItem]:
        ret = []

        if self.option_get('config.authorization.serviceaccount_create') is not False:
            ret.extend([
                Object({
                    'apiVersion': 'v1',
                    'kind': 'ServiceAccount',
                    'metadata': {
                        'name': self.object_name('service-account'),
                        'namespace': self.namespace(),
                    }
                }, name=self.BUILDITEM_SERVICE_ACCOUNT, source=self.SOURCE_NAME, instance=self.basename()),
            ])

        if self.option_get('config.authorization.roles_create') is not False:
            ret.extend([
                Object({
                    'kind': 'ClusterRole',
                    'apiVersion': 'rbac.authorization.k8s.io/v1',
                    'metadata': {
                        'name': self.object_name('cluster-role'),
                    },
                    'rules': [{
                        'apiGroups': [''],
                        'resources': ['nodes',
                                      'nodes/proxy',
                                      'services',
                                      'endpoints',
                                      'pods'],
                        'verbs': ['get', 'watch', 'list']
                    }]
                }, name=self.BUILDITEM_CLUSTER_ROLE, source=self.SOURCE_NAME, instance=self.basename()),
            ])

        if self.option_get('config.authorization.roles_bind') is not False:
            ret.extend([
                Object({
                    'kind': 'ClusterRoleBinding',
                    'apiVersion': 'rbac.authorization.k8s.io/v1beta1',
                    'metadata': {
                        'name': self.object_name('cluster-role-binding'),
                    },
                    'subjects': [{
                        'kind': 'ServiceAccount',
                        'name': self.object_name('service-account'),
                        'namespace': self.namespace(),
                    }],
                    'roleRef': {
                        'apiGroup': 'rbac.authorization.k8s.io',
                        'kind': 'ClusterRole',
                        'name': self.object_name('cluster-role'),
                    }
                }, name=self.BUILDITEM_CLUSTER_ROLE_BINDING, source=self.SOURCE_NAME, instance=self.basename())
            ])

        return ret

    def internal_build_config(self) -> Sequence[ObjectItem]:
        ret = []

        ret.append(Object({
            'apiVersion': 'v1',
            'kind': 'ConfigMap',
            'metadata': {
                'name': self.object_name('config'),
                'namespace': self.namespace(),
            },
            'data': {
                'promtail.yaml': LiteralStr(self.promtail_configfile_get()),
            }
        }, name=self.BUILDITEM_CONFIG, source=self.SOURCE_NAME, instance=self.basename()))

        return ret

    def internal_build_service(self) -> Sequence[ObjectItem]:
        ret = []

        ret.extend([
            Object({
                'apiVersion': 'apps/v1',
                'kind': 'DaemonSet',
                'metadata': {
                    'name': self.object_name('daemonset'),
                    'namespace': self.namespace(),
                    'labels': {
                        'app': self.object_name('pod-label-app'),
                    },
                },
                'spec': {
                    'selector': {
                        'matchLabels': {
                            'app': self.object_name('pod-label-app'),
                        }
                    },
                    'template': {
                        'metadata': {
                            'labels': {
                                'app': self.object_name('pod-label-app'),
                            },
                            'annotations': ValueData({
                                'prometheus.io/scrape': QuotedStr('true'),
                                'prometheus.io/port': QuotedStr('http-metrics'),
                            }, enabled=self.option_get('config.prometheus_annotation') is not False),
                        },
                        'spec': {
                            'serviceAccountName': self.object_name('service-account'),
                            'containers': [{
                                'name': 'promtail',
                                'image': self.option_get('container.promtail'),
                                'args': [
                                    '-config.file=/etc/promtail/promtail.yaml',
                                    ValueData('-client.url={}/loki/api/v1/push'.format(self.option_get('config.loki_url')),
                                              enabled=self.option_get('config.loki_url') is not None),
                                ],
                                'volumeMounts': [{
                                    'name': 'config',
                                    'mountPath': '/etc/promtail'
                                },
                                {
                                    'name': 'run',
                                    'mountPath': '/run/promtail'
                                },
                                {
                                    'mountPath': '/var/lib/docker/containers',
                                    'name': 'docker',
                                    'readOnly': True
                                },
                                {
                                    'mountPath': '/var/log/pods',
                                    'name': 'pods',
                                    'readOnly': True
                                }],
                                'env': [{
                                    'name': 'HOSTNAME',
                                    'valueFrom': {
                                        'fieldRef': {
                                            'fieldPath': 'spec.nodeName'
                                        }
                                    },
                                }],
                                'ports': [{
                                    'containerPort': 3101,
                                    'name': 'http-metrics'
                                }],
                                'securityContext': {
                                    'readOnlyRootFilesystem': True,
                                    'runAsGroup': 0,
                                    'runAsUser': 0
                                },
                                'readinessProbe': {
                                    'failureThreshold': 5,
                                    'httpGet': {
                                        'path': '/ready',
                                        'port': 'http-metrics'
                                    },
                                    'initialDelaySeconds': 10,
                                    'periodSeconds': 10,
                                    'successThreshold': 1,
                                    'timeoutSeconds': 1
                                },
                                'resources': ValueData(
                                    value=self.option_get('kubernetes.resources.daemonset'),
                                    disabled_if_none=True),
                            }],
                            'tolerations': [{
                                'effect': 'NoSchedule',
                                'key': 'node-role.kubernetes.io/master',
                                'operator': 'Exists'
                            }],
                            'volumes': [{
                                'name': 'config',
                                'configMap': {
                                    'name': self.object_name('config'),
                                    'items': [{
                                        'key': 'promtail.yaml',
                                        'path': 'promtail.yaml',
                                    }]
                                }
                            },
                            {
                                'name': 'run',
                                'hostPath': {
                                    'path': '/run/promtail'
                                }
                            },
                            {
                                'hostPath': {
                                    'path': '/var/lib/docker/containers'
                                },
                                'name': 'docker'
                            },
                            {
                                'hostPath': {
                                    'path': '/var/log/pods'
                                },
                                'name': 'pods'
                            }]
                        }
                    }
                }
            }, name=self.BUILDITEM_DAEMONSET, source=self.SOURCE_NAME, instance=self.basename()),
        ])

        return ret

    def promtail_configfile_get(self) -> str:
        if self.configfile is None:
            configfile = self.option_get('config.promtail_config')
            if configfile is None:
                configfile = PromtailConfigFile()
            if isinstance(configfile, str):
                self.configfile = configfile
            else:
                configfilerender = ConfigFileRenderMulti([
                    ConfigFileRender_Yaml(),
                    ConfigFileRender_RawStr()
                ])
                self.configfile = configfilerender.render(configfile.get_value(self))
        return self.configfile
