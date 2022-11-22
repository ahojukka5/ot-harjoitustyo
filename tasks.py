from invoke import task


@task
def start(ctx):
    ctx.run("python3 src/start_gui.py", pty=True)
