import click
from .models import Vehicle, Passes, Station, Provider
from datetime import date

@click.group()
def cli():
    pass

@cli.command()
@click.option('--station', default="1", help='operator', type=str)
@click.option('--from', default="2005-01-01 2000:00:00", help='operator', type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option('--to', default="2021-01-01 2000:00:00", help='operator', type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option('--format', default="1", help='operator', type=str)

def passesperstation(station, from, to, format):
    dict = {}
    passes = Passes.objects.filter(passes_fk1__stationid=station).exclude(timestamp__gte=to).filter(timestamp__gte=from)
    serializer = PassesSerializer(passes, many=True)
    for data in serializer.data:
        print(data)

if __name__=="__main__":
    cli()
