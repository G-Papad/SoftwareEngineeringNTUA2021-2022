from io import StringIO
from django.core.management import call_command
from tl2175app.management.commands.healthcheck import Command
from django.core import management
from django.test import TestCase, SimpleTestCase
from django.core.management.base import BaseCommand
from tl2175app.models import Vehicle, Passes, Station, Provider
from django.db.models import Sum
from datetime import datetime
from tl2175app.serializers import *
import csv, json, os
import requests

"""
class HealthCheck(TestCase):
    def call_command(self, *args, **options):
        out = StringIO()
        call_command("healthcheck", *args, stdout = out, stderr = StringIO(), **options,)
        return out.getvalue()

    def test_health(self):
        out = self.call_command()
        self.assertEqual(out, "[{'status': 'OK', 'dbconnection': 'Connected'}]")
"""
class PassesAnalysisTest(TestCase):
    def do_command(self, *args, **options):
        with StringIO() as f:
            call_command(*args, stdout = f)
            return f.getvalue()
    def test_passes_analysis(self):
        options = {'op1':"KO", 'op2': "AO", 'datefrom':'20200402', 'dateto':'20190403'}
        text = self.do_command('passesanalysis', options)
        self.assertEqual('Invalid arguments: datefrom > date_to', text)

class HealthCheckTest(TestCase):
    def do_command(self, *args, **options):
        with StringIO() as f:
            call_command(*args, stdout = f)
            return f.getvalue()
    def test_01(self):
        text = self.do_command('healthcheck')
        self.assertEqual("[{'status': 'OK', 'dbconnection': 'Connected'}]\n\n", text)
