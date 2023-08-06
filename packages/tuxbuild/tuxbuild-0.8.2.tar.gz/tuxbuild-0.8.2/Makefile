.PHONY:all flake8 check-black black test lint-dockerfile lint-markdown
all: test test-integration flake8 check-black lint-dockerfile lint-markdown
	@echo "🚀😀👌😍🚀"

flake8:
	flake8 .

check-black:
	black --check .

black:
	black .

test:
	python3 -m pytest --cov=tuxbuild --cov-report term-missing .

test-integration:
	run-parts --report test/integration

lint-dockerfile:
	docker run --rm -i hadolint/hadolint < Dockerfile

lint-markdown:
	docker run --rm -i pipelinecomponents/markdownlint -r MD001,MD002,MD003,MD004,MD005,MD006,MD007,MD009,MD010,MD011,MD012,MD014,MD018,MD019,MD020,MD021,MD022,MD023,MD024,MD025,MD026,MD027,MD028,MD029,MD030,MD031,MD032,MD034,MD035,MD036,MD037,MD038,MD039,MD046 < README.md
