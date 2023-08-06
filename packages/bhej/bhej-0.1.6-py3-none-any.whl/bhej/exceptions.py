import typer


def handleNetworkError():
    typer.echo("Error in making network request. Check your network connection.")
    raise typer.Exit(code=74)


def handleServerError():
    typer.echo("An unexpected error occurred with the server.")
    raise typer.Exit(code=75)
