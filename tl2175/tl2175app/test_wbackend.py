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
import os.path
from os import path

class SetUp(TestCase):
    @classmethod
    def setUpTestData(self):
        call_command('loaddata', 'db.json', verbosity=0)

class ResetPasses(TestCase):
    def do_command(self, *args, **options):
        with StringIO() as f:
            call_command(*args, stdout = f)
            return f.getvalue()

    def test_resetpasses_db(self):
        text = self.do_command('resetpasses')
        self.assertEqual(Passes.DoesNotExist, True)
        self.assertEqual(Station.Exists, True)
        self.assertEqual(Provider.Exists, True)
        self.assertEqual(Vehicle.Exists, True)
