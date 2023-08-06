from extras.plugins import PluginConfig

class awsConfig(PluginConfig):
    name = "netbox_aws_accounts"
    verbose_name = "Netbox AWS Accounts"
    description = "Extension for AWS functionality"

    version = "0.1"

    # Plugin author
    author = 'Tiago Sousa'
    author_email = 'tiagosousa@me.com'

    # Configuration parameters that MUST be defined by the user (if any)
    required_settings = []

    # Default configuration parameter values, if not set by the user
    default_settings = {
    }

    # Base URL path. If not set, the plugin name will be used.
    base_url = 'aws'

    # Caching config
    caching_config = {}


config = awsConfig

