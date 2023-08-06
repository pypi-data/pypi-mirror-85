from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices
from .. import config
import inflection

def plugin_item(name):
    return PluginMenuItem(
        permissions = [f"{config.name}.view_{name.lower()}"],
        link=f"plugins:{config.name}:{inflection.tableize(name)}_list",
        link_text=f"{inflection.titleize(inflection.pluralize(name))}",
    )
