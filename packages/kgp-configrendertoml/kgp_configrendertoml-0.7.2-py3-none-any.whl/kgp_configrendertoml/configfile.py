from typing import Any

import toml
from kubragen.configfile import ConfigFileRender, ConfigFileOutput, ConfigFileOutput_DictSingleLevel, \
    ConfigFileOutput_DictDualLevel, ConfigFileOutput_Dict


class ConfigFileRender_TOML(ConfigFileRender):
    """
    Renderer that outputs a TOML file.
    """
    def render_toml(self, value: Any) -> str:
        return toml.dumps(value)

    def supports(self, value: ConfigFileOutput) -> bool:
        if isinstance(value, ConfigFileOutput_DictSingleLevel) or \
           isinstance(value, ConfigFileOutput_DictDualLevel) or \
           isinstance(value, ConfigFileOutput_Dict):
            return True
        return super().supports(value)

    def render(self, value: ConfigFileOutput) -> str:
        if self.supports(value):
            return self.render_toml(value.value)
        super().render(value)
