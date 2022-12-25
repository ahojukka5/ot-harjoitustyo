from invoke import task


@task
def start(ctx):
    ctx.run("python3 src/saehaekkae.py gui", pty=True)


@task
def start_tui(ctx):
    ctx.run("python3 src/saehaekkae.py tui", pty=True)


@task
def test(ctx):
    ctx.run("pytest src", pty=True)


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)


@task
def lint(ctx):
    ctx.run("pylint --ignore=tests src", pty=True)
