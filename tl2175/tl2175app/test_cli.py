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


#class PassesCostTest (TestCase):
    #@classmethod
    #def setUpTestData(self):
        #call_command('loaddata', 'db.json', verbosity=0)
    #def test_command_output(self):
        #out =StringIO()
        #call_command('passescost', op1='OO', op2='KO', datefrom='20201001', dateto='20201031', format='json', stdout=out)
        #self.assertIn('13.8', out.getvalue())

class PassesAnalysisTest(TestCase):
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
    """
    def test_passesanalysis_wrong_ops(self):
        text = self.do_command('passesanalysis', op1 = 'AJ', op2 = 'AO', datefrom = '20190404', dateto = '20200404')
        self.assertEqual('Invalid arguments: Provider does not exist\n\n', text)
    """
    def test_passesanalysis_savejson(self):
        self.do_command('passesanalysis', op1 = 'KO', op2 = 'AO', datefrom = '20200320', dateto = '20200404', savejson = "yes")
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

class PassesPerStationTest(TestCase):
    def do_command(self, *args, **options):
        with StringIO() as f:
            call_command(*args, **options, stdout = f)
            return f.getvalue()
    def test_passesperstation_wrong_dates(self):
        text = self.do_command('passesperstation', station = 'KO01', datefrom = '20200404', dateto = '20190404')
        self.assertEqual('Invalid arguments: date_from > date_to\n\n', text)

    def test_passesperstation_wrong_dateformat(self):
        text = self.do_command('passesperstation', station = 'KO01', datefrom = '2020/04/04', dateto = '20350404')
        self.assertEqual('Wrong DateTime Format\n\n', text)

        """
    def test_passesperstation_wrong_ops(self):
        text = self.do_command('passesperstation', station = 'AJ', datefrom = '20190404', dateto = '20200404')
        self.assertEqual('Invalid arguments: Provider does not exist\n\n', text)
        """
    def test_passesperstation_savejson(self):
        text = self.do_command('passesperstation', station = 'KO01', datefrom = '20200320', dateto = '20200404', savejson = "yes")
        if (not path.exists("tl2175app/management/commands/results/json/PassesPerStation_KO01_20200320_20200404.json")):
            self.assertEqual(0,1)

    def test_passesperstation_csv(self):
        text = self.do_command('passesperstation', station = 'KO01', datefrom = '20200320', dateto = '20200404', format = 'yes')
        if (not path.exists("tl2175app/management/commands/results/csv/PassesPerStation_KO01_20200320_20200404.csv")):
            self.assertEqual(0,1)

    def test_passesperstation_test01(self):
        text = self.do_command('passesperstation', station = 'KO01', datefrom = '20200320', dateto = '20200404')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual("""{'Station': 'KO01', 'StationOperator': 'kentriki_odos', 'RequestTimeStamp': '""" + timestamp + """', 'PeriodFrom': '2020-03-20 00:00:00', 'PeriodTo': '2020-04-04 00:00:00', 'NumberOfPasses': 6, 'PassesList': [{'passid': 'CLJ2137833', 'timestamp': '2020-03-20T21:53:00', 'charge': '2.50', 'vehicleRef': 'IX01MVL33676', 'pass_type': 'home', 'PassIndex': 1, 'TagProvider': 'kentriki_odos'}, {'passid': 'CII8631766', 'timestamp': '2020-03-27T07:51:00', 'charge': '2.80', 'vehicleRef': 'UO75YNW62238', 'pass_type': 'home', 'PassIndex': 2, 'TagProvider': 'kentriki_odos'}, {'passid': 'CHO0835399', 'timestamp': '2020-03-28T09:40:00', 'charge': '2.80', 'vehicleRef': 'ED51EWW52190', 'pass_type': 'home', 'PassIndex': 3, 'TagProvider': 'kentriki_odos'}, {'passid': 'MLU6406429', 'timestamp': '2020-03-30T16:04:00', 'charge': '2.20', 'vehicleRef': 'HW75BKT77773', 'pass_type': 'home', 'PassIndex': 4, 'TagProvider': 'kentriki_odos'}, {'passid': 'CDC9700930', 'timestamp': '2020-04-02T02:50:00', 'charge': '2.80', 'vehicleRef': 'YH66OKD41942', 'pass_type': 'home', 'PassIndex': 5, 'TagProvider': 'kentriki_odos'}, {'passid': 'POV0246876', 'timestamp': '2020-04-02T08:50:00', 'charge': '1.00', 'vehicleRef': 'WY00MLL63827', 'pass_type': 'home', 'PassIndex': 6, 'TagProvider': 'kentriki_odos'}]}\n\n""", text)

        #add more tests for other instances

class PassesCostTest(TestCase):
    def do_command(self, *args, **options):
        with StringIO() as f:
            call_command(*args, **options, stdout = f)
            return f.getvalue()
    def test_passescost_wrong_dates(self):
        text = self.do_command('passescost', op1 = 'KO', op2 = 'AO', datefrom = '20200404', dateto = '20190404')
        self.assertEqual('Invalid arguments: date_from > date_to\n\n', text)

    def test_passescost_wrong_dateformat(self):
        text = self.do_command('passescost', op1 = 'KO', op2 = 'AO', datefrom = '2020/04/04', dateto = '20350404')
        self.assertEqual('Wrong DateTime Format\n\n', text)
    """
    def test_passescost_wrong_ops(self):
        text = self.do_command('passescost', op1 = 'AJ', op2 = 'AO', datefrom = '20190404', dateto = '20200404')
        self.assertEqual('Invalid arguments: Provider does not exist\n\n', text)
    """
    def test_passescost_savejson(self):
        self.do_command('passescost', op1 = 'KO', op2 = 'AO', datefrom = '20200320', dateto = '20200404', savejson = "yes")
        if (not path.exists("tl2175app/management/commands/results/json/PassesCost_KO_AO_20200320_20200404.json")):
            self.assertEqual(0,1)

    def test_passescost_csv(self):
        text = self.do_command('passescost', op1 = 'KO', op2 = 'AO', datefrom = '20200320', dateto = '20200404', format = 'yes')
        if (not path.exists("tl2175app/management/commands/results/csv/PassesCost_KO_AO_20200320_20200404.csv")):
            self.assertEqual(0,1)

    def test_passescost_test01(self):
        text = self.do_command('passescost', op1 = 'KO', op2 = 'AO', datefrom = '20200320', dateto = '20200404')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual("""{'Operator1': 'KO', 'Operator2': 'AO', 'RequestTimestamp': '""" + timestamp + """', 'PeriodFrom': '2020-03-20 00:00:00', 'PeriodTo': '2020-04-04 00:00:00', 'NumberOfPasses': 2, 'PassesCost': 3.0}\n\n""", text)


class ChargesByTest(TestCase):
    def do_command(self, *args, **options):
        with StringIO() as f:
            call_command(*args, **options, stdout = f)
            return f.getvalue()
    def test_chargesby_wrong_dates(self):
        text = self.do_command('chargesby', op1 = 'KO', datefrom = '20200404', dateto = '20190404')
        self.assertEqual('Invalid arguments: date_from > date_to\n\n', text)

    def test_chargesby_wrong_dateformat(self):
        text = self.do_command('chargesby', op1 = 'KO', datefrom = '2020/04/04', dateto = '20350404')
        self.assertEqual('Wrong DateTime Format\n\n', text)

        """
    def test_chargesby_wrong_ops(self):
        text = self.do_command('chargesby', op1 = 'AJ', datefrom = '20190404', dateto = '20200404')
        self.assertEqual('Invalid arguments: Provider does not exist\n\n', text)
        """
    def test_chargesby_savejson(self):
        text = self.do_command('chargesby', op1 = 'KO', datefrom = '20200320', dateto = '20200404', savejson = "yes")
        if (not path.exists("tl2175app/management/commands/results/json/ChargesBy_KO_20200320_20200404.json")):
            self.assertEqual(0,1)

    def test_chargesby_csv(self):
        text = self.do_command('chargesby', op1 = 'KO', datefrom = '20200320', dateto = '20200404', format = 'yes')
        if (not path.exists("tl2175app/management/commands/results/csv/ChargesBy_KO_20200320_20200404.csv")):
            self.assertEqual(0,1)

    def test_chargesby_test01(self):
        text = self.do_command('chargesby', op1 = 'KO', datefrom = '20200320', dateto = '20200404')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual("""{'opID': 'KO', 'RequestTimeStamp': '""" + timestamp + """', 'PeriodFrom': '2020-03-20 00:00:00', 'PeriodTo': '2020-04-04 00:00:00', 'PPOList': [{'VisitingOperator': 'AO', 'NumberOfPasses': 2, 'PassesCost': 3.0}, {'VisitingOperator': 'GF', 'NumberOfPasses': 2, 'PassesCost': 4.3}, {'VisitingOperator': 'EG', 'NumberOfPasses': 0, 'PassesCost': 0}, {'VisitingOperator': 'MR', 'NumberOfPasses': 3, 'PassesCost': 6.0}, {'VisitingOperator': 'NE', 'NumberOfPasses': 3, 'PassesCost': 6.3}, {'VisitingOperator': 'OO', 'NumberOfPasses': 2, 'PassesCost': 5.1}]}\n\n""", text)

class HealthCheckTest(TestCase):
    def do_command(self, *args, **options):
        with StringIO() as f:
            call_command(*args, stdout = f)
            return f.getvalue()
    def test_healthcheck(self):
        text = self.do_command('healthcheck')
        self.assertEqual("[{'status': 'OK', 'dbconnection': 'Connected'}]\n\n", text)

class ConfigurePaymentsTest(TestCase):
    def do_command(self, *args, **options):
        with StringIO() as f:
            call_command(*args, **options, stdout = f)
            return f.getvalue()
    def test_configurepayments_wrong_dates(self):
        text = self.do_command('configurepayments', op1 = 'KO', op2 = 'AO', datefrom = '20200404', dateto = '20190404')
        self.assertEqual('Invalid arguments: date_from > date_to\n\n', text)

    def test_configurepayments_wrong_dateformat(self):
        text = self.do_command('configurepayments', op1 = 'KO', op2 = 'AO', datefrom = '2020/04/04', dateto = '20350404')
        self.assertEqual('Wrong DateTime Format\n\n', text)
    """
    def test_configurepayments_wrong_ops(self):
        text = self.do_command('configurepayments', op1 = 'AJ', op2 = 'AO', datefrom = '20190404', dateto = '20200404')
        self.assertEqual('Invalid arguments: Provider does not exist\n\n', text)
    """
    def test_configurepayments_savejson(self):
        self.do_command('configurepayments', op1 = 'KO', op2 = 'AO', datefrom = '20200320', dateto = '20200404', savejson = "yes")
        if (not path.exists("tl2175app/management/commands/results/json/ConfigurePayments_KO_AO_20200320_20200404.json")):
            self.assertEqual(0,1)
    def test_configurepayments_csv(self):
        text = self.do_command('configurepayments', op1 = 'KO', op2 = 'AO', datefrom = '20200320', dateto = '20200404', format = 'yes')
        if (not path.exists("tl2175app/management/commands/results/csv/ConfigurePayments_KO_AO_20200320_20200404.csv")):
            self.assertEqual(0,1)
    def test_configurepayments_test01(self):
        text = self.do_command('configurepayments', op1 = 'KO', op2 = 'AO', datefrom = '20200320', dateto = '20200404')
        self.assertEqual("""{'operators': 'KO AO', 'cost': -13.8}\n\n""", text)
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
