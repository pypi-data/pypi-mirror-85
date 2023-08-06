from formatter import DockingFormatter
import click 

@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--outputfile', help="Name of the output file you want to give, default is input filename with xlsx extension.")
def run(filename, outputfile):
    """This is an docking log to xmls formatter script"""
    df = DockingFormatter()
    if outputfile:
        try:
            df.findAffinityForCompound(click.format_filename(filename),output=outputfile)
            if '.xlsx' in outputfile:
                click.echo("Docker log formatted to xlsx file with name {0}".format(outputfile))
            else:
                click.echo("Docker log formatted to xlsx file with name {0}".format(f"{outputfile}.xlsx"))
        except:
            click.echo("An unexpected problem occured")
    else:
        try:
            df.findAffinityForCompound(click.format_filename(filename))
            click.echo("Docker log formatted to xlsx file")
        except:
            click.echo("An unexpected problem occured")
    

