install:
	poetry install

run:
	poetry run toc-md

build:
	rm -f dist/*
	poetry build

package-install:
	python3 -m pip install dist/*.whl --force-reinstall

lint-fix:
	poetry run ruff check . --fix

lint:
	poetry run ruff check .

breaking-install:
	python3 -m pip install dist/*.whl --force-reinstall --break-system-packages
