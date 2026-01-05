install:
	poetry install

run:
	poetry run toc-md

build:
	poetry build

package-install:
	python3 -m pip install dist/*.whl

lint-fix:
	poetry run ruff check . --fix

lint:
	poetry run ruff check .

breaking-install:
	python3 -m pip install dist/*.whl --break-system-packages
