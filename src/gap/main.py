import typer
from gap.commands import check, scribe, gate

app = typer.Typer(
    name="gap",
    help="The Gated Agent Protocol Engine.",
    no_args_is_help=True
)

app.add_typer(check.app, name="check")
app.add_typer(scribe.app, name="scribe")
app.add_typer(gate.app, name="gate")

# New
from gap.commands import checkpoint
app.add_typer(checkpoint.app, name="checkpoint")

if __name__ == "__main__":
    app()
