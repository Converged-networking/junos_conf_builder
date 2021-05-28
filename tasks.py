from invoke import task

@task
def test(c):
    c.run("pipenv run yamllint --strict defaults tasks templates tests vars", pty=True)
    c.run("pipenv run ansible-playbook tests/test.yml -i tests/inventory --check", pty=True)

@task
def build(c):
    c.run("pipenv run ansible-playbook tests/test.yml -i tests/inventory", pty=True)
