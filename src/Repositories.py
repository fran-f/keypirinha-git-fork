#
# Git-Fork Repositories plugin
# More info at https://github.com/fran-f/keypirinha-git-fork
#

import keypirinha as kp

from .lib.ForkWrapper import ForkWrapper

class Repositories(kp.Plugin):
    """
    Add catalog items for all the repositories known to Git Fork.
    """

    fork = None
    default_icon = None
    repository_prefix = None

    def on_start(self):
        self._load_settings()
        self._set_up()

    def on_events(self, flags):
        if flags & kp.Events.PACKCONFIG:
            self._clean_up()
            self._load_settings()
            self._set_up()

    def on_catalog(self):
        if not self.fork:
            return

        self.set_catalog([
            self._item_for_repository(r) for r in self.fork.repositories()
        ])

    def on_execute(self, item, action):
        self.fork.openrepository(item.target())

    def on_suggest(self, user_input, items_chain):
        pass

    def _load_settings(self):
        """
        Load the configuration file and extract settings to local variables.
        """
        settings = PluginSettings(self.load_settings())
        self.fork = ForkWrapper(settings.forkdir())
        self.repository_prefix = settings.repositoryprefix()

    def _set_up(self):
        """
        Initialise the plugin based on the extracted configuration.
        """
        self.default_icon = self.load_icon(self.fork.icon())
        self.set_default_icon(self.default_icon)

    def _clean_up(self):
        """
        Clean up any resources, to start anew with fresh configuration.
        """
        if self.default_icon:
            self.default_icon.free()
            self.default_icon = None

    def _item_for_repository(self, repository):
        """
        Return a catalog item for a repository.
        """
        return self.create_item(
                category = kp.ItemCategory.REFERENCE,
                label = self.repository_prefix + repository.get("Name"),
                short_desc = "Open repository in %s" % repository.get("Path"),
                target = repository.get("Path"),
                args_hint = kp.ItemArgsHint.FORBIDDEN,
                hit_hint = kp.ItemHitHint.IGNORE
        )


class PluginSettings:

    def __init__(self, settings):
        self._settings = settings

    def forkdir(self):
        return self._settings.get(
                key = "install_dir",
                section = "fork",
                fallback = ForkWrapper.defaultdir(),
                unquote = True
        )

    def repositoryprefix(self):
        return self._settings.get(
                key = "repository_prefix",
                section = "items",
                fallback = "Fork: ",
                unquote = True
        )

