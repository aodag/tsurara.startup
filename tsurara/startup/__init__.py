import functools


class AppBuilder(object):
    def __init__(self, app_factory, settings):
        self.app_factory = app_factory
        self.settings = settings
        self.middlewares = []

    def use(self, middleware, **settings):
        self.middlewares.append((middleware, settings))

    def make_app(self):
        app = self.app_factory(**self.settings)
        for middleware, settings in self.middlewares:
            app = middleware(app, **settings)
        return app


def startup(app, settings):
    app_builder = AppBuilder(app, settings)
    def dec(func):
        @functools.wraps(func)
        def startup_func():
            func(app_builder)
            return app_builder.make_app()
        return startup_func
    return dec
