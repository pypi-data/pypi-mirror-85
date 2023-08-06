# coding: utf-8

__author__ = "Ondrej Jurcak"

import logging
from configparser import ConfigParser

from aws_xray_sdk import global_sdk_config
from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
from aws_xray_sdk.ext.flask_sqlalchemy.query import XRayFlaskSqlAlchemy


class XRayConfigurator:
    def __init__(self, config: ConfigParser, application) -> None:
        if "XRAY" in config:
            xray = config["XRAY"]
            global_sdk_config.set_sdk_enabled(True)
            xray_recorder.configure(service=xray.get("SERVICE_NAME"),
                plugins=eval(xray.get("PLUGINS", "'ECSPlugin', 'EC2Plugin'")),
                sampling=xray.getboolean("SAMPLING", False),
                stream_sql=xray.getboolean("STREAM_SQL", True),
                daemon_address=xray.get("DAEMON", "xray-daemon:2000"))
            patch_all()

            if xray.getboolean("SQLALCHEMY", True):
                XRayFlaskSqlAlchemy(application)

            XRayMiddleware(application, xray_recorder)

            if xray.get("LOGGING_ENABLED", False):
                logging.getLogger("aws_xray_sdk").setLevel(logging.DEBUG)
            else:
                logging.getLogger("aws_xray_sdk").setLevel(logging.NOTSET)
        else:
            global_sdk_config.set_sdk_enabled(False)
