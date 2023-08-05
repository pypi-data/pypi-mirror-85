from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_announcement:announcement_list',
        link_text='Announcements',
        buttons=(
            PluginMenuButton('plugins:netbox_announcement:announcement_add', 'Add', 'fa fa-plus',
                             ButtonColorChoices.GREEN),
        )
    ),
)
