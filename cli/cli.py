import click

from .utils import APP_DIR, PROJECT_ROOT, run_command


@click.group()
def cli():
    "CLI for executing and developing the querido-diario-backend app."


@cli.command()
@click.option("-d", "--django-port", default="8000", help="Set exposed Django port.")
@click.option(
    "--workdir", default="/opt/app", help="Set app workdir (same as Dockerfile)."
)
@click.option(
    "--pod-name",
    default="querido-diario-backend",
    help="Set pod name (also containers names prefix).",
)
@click.option(
    "--image-namespace", default="querido-diario", help="Set built image namespace."
)
@click.option("--image-tag", default="latest", help="Set built image tag.")
@click.option("--superuser", is_flag=True, help="Also setup superuser.")
@click.option("--collectstatic", is_flag=True, help="Also setup static files.")
@click.option("--makemigrations", is_flag=True, help="Also make migrations.")
@click.option("--migrate", is_flag=True, help="Also execute pending migrations.")
@click.option("--force-recreate", is_flag=True, help="Rebuild entire architecture.")
@click.option(
    "--live-arch-pod",
    is_flag=True,
    help="Assumes that a pod already exists with other services running (such as Postgres).",
)
def setup(
    django_port,
    pod_name,
    workdir,
    image_namespace,
    image_tag,
    superuser,
    collectstatic,
    makemigrations,
    migrate,
    force_recreate,
    live_arch_pod,
):
    "Sets up containers and installs tools for developing (temporary command that does everything)."

    replace_flag = "--replace" if force_recreate else ""

    run_command("pre-commit install")

    run_command(f"cp --no-clobber {APP_DIR}/.example.env {APP_DIR}/.env")
    run_command(
        f"cp --no-clobber {APP_DIR}/.example.postgres.env {APP_DIR}/.postgres.env"
    )

    run_command(
        f"podman build --format docker --tag {image_namespace}/{pod_name}:{image_tag} -f {APP_DIR}/Dockerfile {APP_DIR}"
    )

    if not live_arch_pod:
        run_command(
            f"podman pod create {replace_flag} --publish {django_port}:8000 --name {pod_name}"
        )
        run_command(
            f"podman run -d --rm -ti --name {pod_name}-postgres --pod {pod_name} --volume {pod_name}-postgres-volume:/var/lib/postgresql/data/ --env-file {APP_DIR}/.postgres.env docker.io/postgres:latest -p 5432"
        )

    run_command(
        f"podman run -d --rm -ti --name {pod_name}-redis --pod {pod_name} docker.io/redis:latest --port 6378"
    )
    run_command(
        f"podman run --replace --rm -ti --name {pod_name}-django --pod {pod_name} --volume {APP_DIR}:{workdir}:rw {image_namespace}/{pod_name}:{image_tag} wait-for-it --timeout=30 localhost:5432"
    )
    run_command(
        f"podman run --replace --rm -ti --name {pod_name}-django --pod {pod_name} --volume {APP_DIR}:{workdir}:rw {image_namespace}/{pod_name}:{image_tag} wait-for-it --timeout=30 localhost:6378"
    )

    run_command(
        f"podman run --replace -d -ti --restart always --name {pod_name}-django --pod {pod_name} --volume {APP_DIR}:{workdir}:rw --volume {pod_name}-web-static-volume:{workdir}/static --env-file {APP_DIR}/.env {image_namespace}/{pod_name}:{image_tag} gunicorn config.wsgi:application -w 2 -b :8000 --log-level debug --reload"
    )
    run_command(
        f"podman run -d -ti --restart always --name {pod_name}-celery-beat --pod {pod_name} --volume {APP_DIR}:{workdir}:rw {image_namespace}/{pod_name}:{image_tag} celery -A config beat -l INFO"
    )
    run_command(
        f"podman run -d -ti --restart always --name {pod_name}-celery-worker --pod {pod_name} --volume {APP_DIR}:{workdir}:rw {image_namespace}/{pod_name}:{image_tag} celery -A config worker -l INFO"
    )

    run_command(f"podman exec -ti {pod_name}-django python create_database.py")

    if makemigrations:
        run_command(
            f"podman exec -ti {pod_name}-django python manage.py makemigrations"
        )

    if migrate:
        run_command(f"podman exec -ti {pod_name}-django python manage.py migrate")

    if collectstatic:
        run_command(f"podman exec -ti {pod_name}-django python manage.py collectstatic")

    if superuser:
        click.echo("\nCreate a superuser\n")
        run_command(
            f"podman exec -ti {pod_name}-django python manage.py createsuperuser"
        )


@cli.command()
@click.option("--check", is_flag=True, help="Just checking (doesn't apply formatting).")
def format(check):
    "Project's style formatting."

    if check:
        run_command(f"python -m isort --check --diff {APP_DIR} {PROJECT_ROOT}/cli")
        run_command(f"python -m black --check {APP_DIR} {PROJECT_ROOT}/cli")
        run_command(f"flake8 {APP_DIR} {PROJECT_ROOT}/cli")
    else:
        run_command(f"python -m isort --apply {APP_DIR} {PROJECT_ROOT}/cli")
        run_command(f"python -m black {APP_DIR} {PROJECT_ROOT}/cli")


@cli.command()
@click.option("--dev", is_flag=True, help="Updates requirements-dev.txt instead.")
def update_requirements(dev):
    "Updates requirements.txt file."

    workdir, suffix = (PROJECT_ROOT, "-dev") if dev else (APP_DIR, "")
    run_command(
        f"pip-compile {workdir}/requirements{suffix}.in > {workdir}/requirements{suffix}.txt",
        shell=True,
    )
