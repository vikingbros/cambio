.PHONY: build # Place build first so a blank `make` will run it
build:
	isort src/ tests/
	black src/ tests/
	flake8 src/
	mypy src/
	pytest tests/
