from io import StringIO
from django.core.management import call_command
from django.test import TestCase

# Create your tests here.

class PassesCostTest (TestCase):
    def test_command_output(self):
        out =StringIO()
        call_command('passescost', '--op1=KO', '--op2=OO','--datefrom=20201001', '--dateto=20201031', '--format=json', stdout=out)
        print("out: " + out.getvalue() + " here")
        self.assertIn('13,80', out.getvalue())
