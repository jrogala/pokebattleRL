from invoke.tasks import task


@task
def docker(c, build=False, up=False, upd=False, down=False, logs=False, rm=False):
    """
    Build and run the docker container.
    """
    if build:
        c.run("docker compose build")
    if up:
        c.run("docker compose up")
    if upd:
        c.run("docker compose up -d")
    if down:
        c.run("docker compose down")
    if logs:
        c.run("docker compose logs -f")
    if rm:
        c.run("docker compose rm -f")
