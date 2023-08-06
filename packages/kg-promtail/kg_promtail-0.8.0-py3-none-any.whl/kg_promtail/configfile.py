from typing import Optional, Any, Sequence, Mapping

from kubragen.configfile import ConfigFileOutput, ConfigFileOutput_Dict, ConfigFile_Extend, \
    ConfigFileExtension, ConfigFileExtensionData
from kubragen.merger import Merger
from kubragen.option import OptionDef
from kubragen.options import Options, option_root_get, OptionGetter


class PromtailConfigFileOptions(Options):
    """
    Options for Promtail config file.

    .. list-table::
        :header-rows: 1

        * - option
          - description
          - allowed types
          - default value
        * - config |rarr| merge_config
          - Mapping to merge into final config
          - Mapping
          -
    """
    def define_options(self) -> Optional[Any]:
        """
        Declare the options for the Promtail config file.

        :return: The supported options
        """
        return {
            'config': {
                'merge_config': OptionDef(allowed_types=[Mapping]),
            },
        }


class PromtailConfigFile(ConfigFile_Extend):
    """
    Promtail main configuration file in Yaml format.
    """
    options: PromtailConfigFileOptions

    def __init__(self, options: Optional[PromtailConfigFileOptions] = None,
                 extensions: Optional[Sequence[ConfigFileExtension]] = None):
        super().__init__(extensions)
        if options is None:
            options = PromtailConfigFileOptions()
        self.options = options

    def option_get(self, name: str):
        return option_root_get(self.options, name)

    def init_value(self, options: OptionGetter) -> ConfigFileExtensionData:
        ret = ConfigFileExtensionData({
            'client': {
                'backoff_config': {
                    'max_period': '5m',
                    'max_retries': 10,
                    'min_period': '500ms'
                },
                'batchsize': 1048576,
                'batchwait': '1s',
                'external_labels': {},
                'timeout': '10s'
            },
            'positions': {
                'filename': '/run/promtail/positions.yaml'
            },
            'server': {
                'http_listen_port': 3101
            },
            'target_config': {
                'sync_period': '10s'
            },
            'scrape_configs': []
        })

        return ret

    def finish_value(self, options: OptionGetter, data: ConfigFileExtensionData) -> ConfigFileOutput:
        if self.option_get('config.merge_config') is not None:
            Merger.merge(data.data, self.option_get('config.merge_config'))
        return ConfigFileOutput_Dict(data.data)
