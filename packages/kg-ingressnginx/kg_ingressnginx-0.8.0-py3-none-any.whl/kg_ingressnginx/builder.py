from typing import List, Optional, Dict, Any

import requests
import yaml
from kubragen import KubraGen
from kubragen.builder import Builder
from kubragen.consts import PROVIDER_KIND, PROVIDER_DIGITALOCEAN, PROVIDER_AMAZON
from kubragen.exception import InvalidNameError
from kubragen.object import ObjectItem
from kubragen.types import TBuild, TBuildItem
from kubragen.util import urljoin

from .option import IngressNGINXOptions


class IngressNGINXBuilder(Builder):
    """
    Ingress NGINX builder.

    Based on `ingress-nginx deploy <https://kubernetes.github.io/ingress-nginx/deploy/>`_.

    Based on `kubernetes/ingress-nginx <https://github.com/kubernetes/ingress-nginx>`_.

    .. list-table::
        :header-rows: 1

        * - build
          - description
        * - BUILD_INGRESS
          - creates ingress

    .. list-table::
        :header-rows: 1

        * - build item
          - description
        * - BUILDITEM_INGRESS
          - Ingress

    """
    options: IngressNGINXOptions
    # _namespace: str
    _downloadedfiles: Optional[Dict[str, Any]]
    _use_provider: str

    SOURCE_NAME = 'kg_ingressnginx'

    BUILD_INGRESS = TBuild('ingress')

    BUILDITEM_INGRESS = TBuildItem('ingress')

    def __init__(self, kubragen: KubraGen, options: Optional[IngressNGINXOptions] = None):
        super().__init__(kubragen)
        if options is None:
            options = IngressNGINXOptions()
        self.options = options

        self._downloadedfiles = None
        # self._namespace = self.option_get('namespace')
        self._parse_provider()

    def option_get(self, name: str):
        return self.kubragen.option_root_get(self.options, name)

    def _parse_provider(self):
        config_provider = self.option_get('config.provider_override')
        if config_provider is not None:
            self._use_provider = config_provider
            return
        if self.kubragen.provider.provider == PROVIDER_KIND:
            self._use_provider = 'kind'
        elif self.kubragen.provider.provider == PROVIDER_DIGITALOCEAN:
            self._use_provider = 'do'
        elif self.kubragen.provider.provider == PROVIDER_AMAZON:
            self._use_provider = 'aws'
        else:
            self._use_provider = 'cloud'

    def _checkdownloaded(self):
        if self._downloadedfiles is None:
            dflist = {}
            for df in ['deploy.yaml']:
                r = requests.get(urljoin('https://raw.githubusercontent.com/kubernetes/ingress-nginx',
                                         self.option_get('config.github_commit'), 'deploy', 'static', 'provider',
                                         self._use_provider, df))
                r.raise_for_status()
                dflist[df] = [item for item in yaml.load_all(r.text, Loader=yaml.SafeLoader)]
            self._downloadedfiles = dflist

    def basename(self, suffix: str = ''):
        return '{}{}'.format(self.option_get('basename'), suffix)

    # def namespace(self):
    #     return self._namespace

    def build_names(self) -> List[TBuild]:
        return [self.BUILD_INGRESS]

    def build_names_required(self) -> List[TBuild]:
        return [self.BUILD_INGRESS]

    def builditem_names(self) -> List[TBuildItem]:
        return [
            self.BUILDITEM_INGRESS,
        ]

    def internal_build(self, buildname: TBuild) -> List[ObjectItem]:
        if buildname == self.BUILD_INGRESS:
            return self.internal_build_ingress()
        else:
            raise InvalidNameError('Invalid build name: "{}"'.format(buildname))

    def internal_build_ingress(self) -> List[ObjectItem]:
        self._checkdownloaded()
        ret = []
        if self._downloadedfiles is not None:
            # TODO: patch names and namespaces
            ret = self._downloadedfiles['deploy.yaml']
        return ret
