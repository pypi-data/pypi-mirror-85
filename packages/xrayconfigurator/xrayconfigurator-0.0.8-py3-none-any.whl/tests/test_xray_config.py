import configparser
import logging
import unittest
from unittest import TestCase

import os
from unittest.mock import Mock, patch

from aws_xray_sdk import global_sdk_config
from aws_xray_sdk.core import xray_recorder

from xray_configurator.xray_configurator import XRayConfigurator


class ConfigTestCase(TestCase):
    @patch("xray_configurator.xray_configurator.patch_all")
    @patch("xray_configurator.xray_configurator.XRayMiddleware")
    @patch("xray_configurator.xray_configurator.XRayFlaskSqlAlchemy")
    def test_no_xray_section(self, mock_alchemy, mock_middleware, mock_patch_all):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), "config.ini"))
        XRayConfigurator(config, Mock())
        self.assertFalse(global_sdk_config.sdk_enabled())
        mock_alchemy.assert_not_called()
        mock_middleware.assert_not_called()
        mock_patch_all.assert_not_called()

    @patch("xray_configurator.xray_configurator.xray_recorder.configure")
    @patch("xray_configurator.xray_configurator.patch_all")
    @patch("xray_configurator.xray_configurator.XRayMiddleware")
    @patch("xray_configurator.xray_configurator.XRayFlaskSqlAlchemy")
    def test_xray_defaults(self, mock_alchemy, mock_middleware, mock_patch_all, mock_configure):
        config = configparser.ConfigParser()
        config.read(
            os.path.join(os.path.dirname(__file__), "config_xray_defaults.ini")
        )
        app_mock = Mock()

        XRayConfigurator(config, app_mock)
        self.assertTrue(global_sdk_config.sdk_enabled())
        mock_configure.assert_called_once_with(daemon_address='xray-daemon:2000', plugins=('ECSPlugin', 'EC2Plugin'), sampling=False, service='test-service-name', stream_sql=True)
        self.assertEqual(logging.getLogger("aws_xray_sdk").level, logging.NOTSET)

        mock_alchemy.assert_called_once_with(app_mock)
        mock_middleware.assert_called_once_with(app_mock, xray_recorder)
        mock_patch_all.assert_called_once_with()

    @patch("xray_configurator.xray_configurator.xray_recorder.configure")
    @patch("xray_configurator.xray_configurator.patch_all")
    @patch("xray_configurator.xray_configurator.XRayMiddleware")
    @patch("xray_configurator.xray_configurator.XRayFlaskSqlAlchemy")
    def test_xray(self, mock_alchemy, mock_middleware, mock_patch_all, mock_configure):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), "config_xray.ini"))
        app_mock = Mock()

        XRayConfigurator(config, app_mock)
        self.assertTrue(global_sdk_config.sdk_enabled())
        mock_configure.assert_called_once_with(daemon_address='129.0.0.0:5000', plugins=('ECSPlugin', 'EC2Plugin', 'ElasticBeanstalkPlugin'), sampling=True, service='test-service-name', stream_sql=False)
        self.assertEqual(logging.getLogger("aws_xray_sdk").level, logging.DEBUG)

        mock_alchemy.assert_not_called()
        mock_middleware.assert_called_once_with(app_mock, xray_recorder)
        mock_patch_all.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
