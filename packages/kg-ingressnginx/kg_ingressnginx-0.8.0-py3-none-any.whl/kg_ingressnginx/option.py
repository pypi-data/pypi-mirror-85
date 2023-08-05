from kubragen.option import OptionDef
from kubragen.options import Options


class IngressNGINXOptions(Options):
    """
    Options for the Ingress NGINX builder.

    .. list-table::
        :header-rows: 1

        * - option
          - description
          - allowed types
          - default value
        * - config |rarr| github_commit
          - github commit
          - str
          - ```ingress-nginx-<version>```
        * - config |rarr| provider_override
          - force provider, otherwise detect using the current :class:`kubragen.provider.Provider`
          - str
          -
    """
    def define_options(self):
        """
        Declare the options for the Ingress NGINX builder.

        :return: The supported options
        """
        return {
            # 'basename': OptionDef(),
            # 'namespace': OptionDef(),
            'config': {
                'github_commit': OptionDef(required=True, default_value='ingress-nginx-3.7.1', allowed_types=[str]),
                'provider_override': OptionDef(allowed_types=[str]),
            },
        }
