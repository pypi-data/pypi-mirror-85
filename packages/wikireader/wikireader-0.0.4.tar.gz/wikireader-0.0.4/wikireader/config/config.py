from pathlib import Path
import json
import importlib.resources as pkg_resources
from . import data


class Config:
    """
    Holds config data
    """
    def __init__(self):
        self._configdir = Path.home() / ".config" / "wikireader"
        if not self._configdir.exists():
            self._configdir.mkdir()
        configfile = self._configdir / "config.json"
        if  not configfile.exists():
            configfile.write_text(
                pkg_resources.read_text(data, "config.json"))
        self._readconfig(
            json.loads(
                configfile.read_text()))
    
    def _readconfig(self, config):
        """
        Reads configfile
        """
        self.theme = config.get("theme", "dark")
        self.language = config.get("language", "eng")
    
    def _copy_css(self):
        css_path = self._configdir / "css"
        if not css_path.exists():
            css_path.mkdir()
        for r in pkg_resources.contents(data):
            if r.endswith(".css"):
                (css_path / r).write_text(
                    pkg_resources.read_text(data, r))

    @property
    def css(self):
        data = self._configdir / "css" / f"{self.theme}.css"
        if not data.exists():
            self._copy_css()
        css = data.read_text()
        return css
        




