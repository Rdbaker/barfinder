# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import os

from apiai import ApiAI
from flask import Flask, render_template, url_for, redirect
from flask_sslify import SSLify
from flask_admin import Admin
from flask_login import current_user

from barfinder import commands, public, user, api
from barfinder.assets import assets
from barfinder.extensions import (bcrypt, cache, csrf_protect, db,
                                  debug_toolbar, login_manager, migrate)
from barfinder.models.business import Business, Tag, BusinessTag
from barfinder.settings import ProdConfig


def create_app(config_object=ProdConfig):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)

    @app.before_first_request
    def initialize_apiai_service():
        app.api_ai = ApiAI(client_access_token=os.environ.get('API_AI_TOKEN'))

    return app


def register_extensions(app):
    """Register Flask extensions."""
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    admin = Admin(app, name='Barfinder', template_mode='bootstrap3')
    register_admin_routes(admin)

    # only use SSL if we're on heroku
    if 'DYNO' in os.environ:
        SSLify(app)

    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(api.chat.mod)
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': user.models.User}

    app.shell_context_processor(shell_context)


def register_admin_routes(admin):
    from flask_admin.contrib.sqla import ModelView

    class BarfinderAdminView(ModelView):
        def is_accessible(self):
            return current_user.is_authenticated

        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for('public.home'))

    admin.add_view(BarfinderAdminView(Business, db.session))
    admin.add_view(BarfinderAdminView(Tag, db.session))
    admin.add_view(BarfinderAdminView(BusinessTag, db.session))


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
