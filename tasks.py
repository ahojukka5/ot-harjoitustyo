from invoke import task


@task
def start(ctx):
    ctx.run("python3 src/start_gui.py", pty=True)


@task
def test(ctx):
    ctx.run("pytest src", pty=True)
