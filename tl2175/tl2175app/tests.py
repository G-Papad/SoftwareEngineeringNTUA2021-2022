from io import StringIO
from django.core.management import call_command
from django.test import TestCase

# Create your tests here.

class PassesCostTest (TestCase):
    @classmethod
    def setUpTestData(self):
        call_command('loaddata', 'db.json', verbosity=0)

    def test_command_output(self):
        out =StringIO()
        call_command('passescost', '--op1=OO', '--op2=KO','--datefrom=20201001', '--dateto=20201031', '--format=json', stdout=out)
        self.assertIn('13.8', out.getvalue())
