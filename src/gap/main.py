import typer
from gap.commands import check, scribe, gate, migrate

app = typer.Typer(
    name="gap",
    help="The Sovereign Gated Agent Protocol Engine.",
    no_args_is_help=True
)

app.add_typer(check.app, name="check")
app.add_typer(scribe.app, name="scribe")
app.add_typer(gate.app, name="gate")
app.add_typer(migrate.app, name="migrate")

if __name__ == "__main__":
    app()
