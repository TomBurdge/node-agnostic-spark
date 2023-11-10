GLOBAL_PYTHON = $(shell which python3.10)
LOCAL_PYTHON = ./.venv/bin/python
LOCAL_PRE_COMMIT = ./.venv/lib/python*/site-packages/pre_commit

setup: data venv install pre-commit

data:
	mkdir -p data
	curl https://us-prd-motherduck-open-datasets.s3.amazonaws.com/hacker_news/parquet/hacker_news_2021_2022.parquet -o data/hacker_news_2021_2022.parquet

java:
	sudo apt update
	sudo apt install default-jdk


venv: $(GLOBAL_PYTHON)
	@echo "Creating .venv..."
	python3 -m venv .venv
	@echo "Activating .venv..."
	@echo "Run 'deactivate' command to exit virtual environment."
	@echo "For more info, see https://docs.python.org/3/library/venv.html."
	. ./.venv/bin/activate

install: ${LOCAL_PYTHON}
	@echo "Installing dependencies..."
	pip install -e ".[dev]"

#currently - this doesn't work with the setup file - seems to not activate the environment properly
pre-commit: ${LOCAL_PYTHON} ${LOCAL_PRE_COMMIT}
	@echo "Setting up pre-commit..."
	@if [ -f ${LOCAL_PRE_COMMIT} ]; then \
		./.venv/bin/pre-commit install; \
	else \
		echo "pre-commit not found in ${LOCAL_PRE_COMMIT}"; \
		echo "Trying to reinstall pre-commit..."; \
		./.venv/bin/pip install pre-commit; \
		./.venv/bin/pre-commit install; \
	fi
	./.venv/bin/pre-commit autoupdate

metaflow: ${LOCAL_PYTHON}
	@echo "Configuring metaflow for aws services"
	aws configure

clean:
	rm -rf .git/hooks
	rm -rf .venv
	rm -f poetry.lock
