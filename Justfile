package := 'tamahagane'
default_test_suite := 'tests/unittests'

install:
    uv sync --group dev --group docs

update:
    uv sync --group dev --group docs

upgrade:
    uv sync --group dev --group docs --upgrade

doc:
    cd docs && uv run make html
    xdg-open docs/build/html/index.html

cleandoc:
    cd docs && uv run make clean

test: lint typecheck unittest

lf:
    uv run pytest -sxvvv --lf

unittest test_suite=default_test_suite:
    uv run pytest -sxv {{test_suite}}

lint:
    uv run ruff check .

typecheck:
    uv run mypy src/ tests/

fmt:
    uv run ruff check --fix .
    uv run ruff format src tests

cov test_suite=default_test_suite:
    rm -f .coverage
    rm -rf htmlcov
    uv run pytest --cov-report=html --cov={{package}} {{test_suite}}
    xdg-open htmlcov/index.html

release major_minor_patch: test && changelog
    uvx --with=pdm,pdm-bump --python-preference system pdm bump {{major_minor_patch}}

changelog:
    uv run python scripts/write_changelog.py
    cat CHANGELOG.md >> CHANGELOG.md.new
    rm CHANGELOG.md
    mv CHANGELOG.md.new CHANGELOG.md
    $EDITOR CHANGELOG.md

publish:
    git commit -am "Release $(uv version --short)"
    git tag "v$(uv version --short)"
    git push origin "v$(uv version --short)"
    git push origin main
