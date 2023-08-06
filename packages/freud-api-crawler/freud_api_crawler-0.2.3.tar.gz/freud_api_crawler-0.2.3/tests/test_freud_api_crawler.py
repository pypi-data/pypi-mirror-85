#!/usr/bin/env python

"""Tests for `freud_api_crawler` package."""

import os
import unittest
from click.testing import CliRunner

from freud_api_crawler import freud_api_crawler as frd
from freud_api_crawler import cli


class TestFreud_api_crawler(unittest.TestCase):
    """Tests for `freud_api_crawler` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_not_authenticated(self):
        """Test if os-envs are set"""
        frd_obj = frd.FrdClient()
        if frd.FRD_PW and frd.FRD_PW:
            self.assertTrue(frd_obj.authenticated)
        else:
            self.assertFalse(frd_obj.authenticated)

    def test_001_endpoints_no_auth(self):
        """Test of endpoints-method"""
        frd_obj = frd.FrdClient(user=False, pw=False)
        endpoints = frd_obj.list_endpoints()
        self.assertFalse(endpoints)

    # def test_002_endpoints_with_auth(self):
    #     """Test of endpoints-method"""
    #     frd_obj = frd.FrdClient()
    #     endpoints = frd_obj.list_endpoints()
    #     self.assertTrue(endpoints)
    #     print(endpoints.keys())
    #     self.assertTrue('node' in endpoints.keys())

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'freud_api_crawler.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
