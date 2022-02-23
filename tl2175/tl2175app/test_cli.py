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

class PassesCostTest (TestCase):
    @classmethod
    def setUpTestData(self):
        call_command('loaddata', 'db.json', verbosity=0)
    def test_command_output(self):
        out =StringIO()
        call_command('passescost', op1='OO', op2='KO', datefrom='20201001', dateto='20201031', format='json', stdout=out)
        self.assertIn('13.8', out.getvalue())

# class PassesAnalysisTest(TestCase):
    def do_command(self, *args, **options):
        with StringIO() as f:
            call_command(*args, **options, stdout = f)
            return f.getvalue()
    def test_passesanalysis_wrong_dates(self):
        text = self.do_command('passesanalysis', op1 = 'KO', op2 = 'AO', datefrom = '20200404', dateto = '20190404')
        self.assertEqual('Invalid arguments: date_from > date_to\n\n', text)

    def test_passesanalysis_wrong_dateformat(self):
        text = self.do_command('passesanalysis', op1 = 'KO', op2 = 'AO', datefrom = '2020/04/04', dateto = '20350404')
        self.assertEqual('Wrong DateTime Format\n\n', text)

        #fix this when connect to db

        """
    def test_passesanalysis_wrong_ops(self):
        text = self.do_command('passesanalysis', op1 = 'AJ', op2 = 'AO', datefrom = '20190404', dateto = '20200404')
        self.assertEqual('Invalid arguments: Provider does not exist\n\n', text)
        """

    def test_passesanalysis_savejson(self):
        text = self.do_command('passesanalysis', op1 = 'KO', op2 = 'AO', datefrom = '20200320', dateto = '20200404', savejson = "yes")
        if (not path.exists("tl2175app/management/commands/results/json/PassesAnalysis_KO_AO_20200320_20200404.json")):
            self.assertEqual(0,1)

    def test_passesanalysis_csv(self):
        text = self.do_command('passesanalysis', op1 = 'KO', op2 = 'AO', datefrom = '20200320', dateto = '20200404', format = 'yes')
        if (not path.exists("tl2175app/management/commands/results/csv/PassesAnalysis_KO_AO_20200320_20200404.csv")):
            self.assertEqual(0,1)

    def test_passesanalysis_test01(self):
        text = self.do_command('passesanalysis', op1 = 'KO', op2 = 'AO', datefrom = '20200320', dateto = '20200404')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual("""{'op1_ID': 'KO', 'op2_ID': 'AO', 'RequestTimeStamp': '"""+timestamp+"""', 'PeriodFrom': '2020-03-20 00:00:00', 'PeriodTo': '2020-04-04 00:00:00', 'NumberOfPasses': 2, 'PassesList': [{'passid': 'CNQ8711527', 'timestamp': '2020-03-26T20:59:00', 'charge': '2.00', 'stationRef': 'kentriki_odos tolls station 03', 'vehicleRef': 'OC94ASJ72024', 'PassIndex': 1}, {'passid': 'NCF9224902', 'timestamp': '2020-03-24T17:25:00', 'charge': '1.00', 'stationRef': 'kentriki_odos tolls station 09', 'vehicleRef': 'HT62RDI04611', 'PassIndex': 2}]}\n\n""", text)

        #add more tests for other instances

# class HealthCheckTest(TestCase):
#     def do_command(self, *args, **options):
#         with StringIO() as f:
#             call_command(*args, stdout = f)
#             return f.getvalue()
    def test_healthcheck(self):
        text = self.do_command('healthcheck')
        self.assertEqual("[{'status': 'OK', 'dbconnection': 'Connected'}]\n\n", text)
"""
class ResetPasses(TestCase):
    def do_command(self, *args, **options):
        with StringIO() as f:
            call_command(*args, stdout = f)
            return f.getvalue()
    def test_resetpasses(self):
        text = self.do_command('resetpasses')
        self.assertEqual("[{'status': 'OK'}]\n\n", text)

class ResetStations(TestCase):
    def do_command(self, *args, **options):
        with StringIO() as f:
            call_command(*args, stdout = f)
            return f.getvalue()
    def test_resetpasses(self):
        text = self.do_command('resetstations')
        self.assertEqual("[{'status': 'OK'}]\n\n", text)

class ResetVehicles(TestCase):
    def do_command(self, *args, **options):
        with StringIO() as f:
            call_command(*args, stdout = f)
            return f.getvalue()
    def test_resetpasses(self):
        text = self.do_command('resetvehicles')
        self.assertEqual("[{'status': 'OK'}]\n\n", text)
"""
