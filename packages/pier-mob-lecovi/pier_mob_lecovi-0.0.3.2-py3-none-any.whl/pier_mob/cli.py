import typer

__version__ = "0.0.3.2"


app = typer.Typer()


@app.command()
def info():
    typer.secho("Pier Mob built with Typer and ♥️.", fg=typer.colors.WHITE, bold=True)


@app.command()
def version():
    typer.echo(f"Pier Mob v{__version__}")
