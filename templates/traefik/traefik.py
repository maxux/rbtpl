from zerorobot.template.base import TemplateBase

CONTAINER_TEMPLATE_UID = 'github.com/threefoldtech/0-templates/container/0.0.1'

class Traefik(TemplateBase):
    # define the verion of this template
    version = '0.0.1'
    template_name = "traefik"

    def __init__(self, name=None, guid=None, data=None):
        super().__init__(name=name, guid=guid, data=data)

    @property
    def _node_sal(self):
        return j.clients.zos.get(self.data['node'])

    @property
    def _container_sal(self):
        return self._node_sal.containers.get(self._container_name)

    @property
    def _container_name(self):
        return "container-%s" % self.guid

    def install(self):
        """
        Creating traefik container with the provided config file
        """
        self.logger.info("installing traefik: %s", self.name)
        container = self._get_container()

        # ensure container is installed and running
        for action in ['install', 'start']:
            try:
                container.state.check('actions', action, 'ok')

            except StateCheckError:
                container.schedule_action(action).wait(die=True)

        self._node_sal.client.nft.open_port(80)
        print(self._container_sal.client.system('traefik --version').get())

        self.state.set('status', 'running', 'ok')
        self.state.set('actions', 'install', 'ok')
