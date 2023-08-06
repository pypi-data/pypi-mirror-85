from extras.plugins import PluginConfig


class AnnouncementConfig(PluginConfig):
    """
    This class defines attributes for the NetBox Announcement plugin.
    """
    # Plugin package name
    name = 'netbox_announcement'

    # Human-friendly name and description
    verbose_name = 'Announcement'
    description = 'A plugin to render and edit announcements'

    # Plugin version
    version = '1.0.6'
    # Plugin author
    author = 'Vasilatos Vitaliy'
    author_email = 'vasilatos80@gmail.com'

    # Configuration parameters that MUST be defined by the user (if any)
    required_settings = []

    # Default configuration parameter values, if not set by the user
    # default_settings = {
    #     'loud': True
    # }

    # Base URL path. If not set, the plugin name will be used.
    base_url = 'announcement'

    # Caching config
    # caching_config = {}


config = AnnouncementConfig
