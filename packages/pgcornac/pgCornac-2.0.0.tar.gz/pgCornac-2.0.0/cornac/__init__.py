import os.path
from pathlib import Path
from pkg_resources import get_distribution
from urllib.parse import urlparse
from warnings import filterwarnings

from flask import Flask

from cornac.utils import patch_dict

# psycopg2 and psycopg2-binary is a mess. You can't define OR dependency in
# Python. Just globally ignore this for now.
filterwarnings("ignore", message="The psycopg2 wheel package will be renamed")  # noqa


try:
    dist = get_distribution('pgCornac')
    __version__ = dist.version
except Exception:
    __version__ = 'unknown'


FILESDIR = Path(__file__).parent / 'files'


class Cornac(Flask):
    _canonical_url_adapter = None

    @property
    def app_version(self):
        return f'Cornac/{__version__}'

    @property
    def canonical_url_adapter(self):
        # Instanciate a dedicated url_adapter to build canonical URL based on
        # CANONICAL_URL instead of SERVER_NAME.
        if self._canonical_url_adapter is None:
            canonical = urlparse(self.config['CANONICAL_URL'])
            with patch_dict(
                    self.config,
                    PREFERRED_URL_SCHEME=canonical.scheme,
                    SERVER_NAME=canonical.netloc,
                    APPLICATION_ROOT=canonical.path,
            ):
                self._canonical_url_adapter = self.create_url_adapter(None)
        return self._canonical_url_adapter

    @property
    def has_etcd(self):
        return bool(self.config['ETCD'])

    @property
    def has_snapshots(self):
        return bool(self.config['BACKUPS_LOCATION'])

    @property
    def has_temboard(self):
        return bool(self.config['TEMBOARD'])


def create_app(environ=os.environ):

    app = Cornac(
        __name__,
        instance_path=str(Path.home()),
        static_folder=None,
    )

    from .core.config import configure
    configure(app, environ=environ)

    from .core.model import db
    db.init_app(app)

    from .web import cornacbp, iam, rds, root, sts, fallback, set_server_header
    app.register_blueprint(root)
    app.register_blueprint(cornacbp, url_prefix='/cornac')
    app.register_blueprint(iam, url_prefix='/iam')
    app.register_blueprint(rds, url_prefix='/rds')
    app.register_blueprint(sts, url_prefix='/sts')
    app.errorhandler(404)(fallback)
    app.after_request(set_server_header)

    from .web.auth import TrustedProxyFix
    app.wsgi_app = TrustedProxyFix(
        app.wsgi_app, app.config['TRUSTED_PROXIES_ADDRESSES'])

    from flask_cors import CORS
    CORS(app)

    from flask_mailman import Mail
    app.mail = Mail(app)

    from .worker import dramatiq, maintainance

    # Dynamic setup of periodicity.
    from periodiq import cron, PeriodiqMiddleware
    dramatiq.middleware.append(PeriodiqMiddleware(skip_delay=30 * 60))
    maintainance.kw['periodic'] = cron(app.config['MAINTAINANCE_WINDOW'])

    dramatiq.init_app(app)

    return app
