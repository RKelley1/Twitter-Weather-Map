import hug

from api.methods import default_response

def singleton(cls):
    return cls()


@singleton
class Bootstrap(object):
    PATH_SEPARATOR = '/'
    RESOURCES = 'resources'
    ROUTES = 'routes'
    MIDDLEWARE = 'middleware'

    @classmethod
    def configure(cls, api_root: str, config: dict):
        assert isinstance(config, dict)
        assert isinstance(api_root, str)

        cls._configure_middleware(api_root, config)
        cls._configure_resources(api_root, config)

    @classmethod
    def _configure_resources(cls, api_root: str, config: dict):
        resources = config.get(cls.RESOURCES, None)

        assert resources and len(resources) > 0

        _route = hug.route.API(api_root)

        for _name, _class in resources.items():
            _root_path = cls.PATH_SEPARATOR + _name
            _route.object(_root_path, output=default_response)(_class())

    @classmethod
    def _configure_middleware(cls, api_root: str, config: dict):
        middleware = config.get(cls.MIDDLEWARE, None)

        if not middleware or len(middleware) < 1:
            return

        _interface = hug.API(api_root).http

        for _, _class in middleware.items():
            _interface.add_middleware(_class())
