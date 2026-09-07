.PHONY: test clean install help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

test: ## Run all tests
	python tests/test_easylang.py
	python tests/test_hardlang.py
	python tests/test_hardwarelang.py

test-easylang: ## Run EasyLang tests
	python tests/test_easylang.py

test-hardlang: ## Run HardLang tests
	python tests/test_hardlang.py

test-hardwarelang: ## Run HardwareLang tests
	python tests/test_hardwarelang.py

run-easylang: ## Run EasyLang example
	python easylang/easylang.py easylang/examples/hello.el

run-hardlang: ## Run HardLang example
	python hardlang/hardlang.py hardlang/examples/hello.hl

run-hardwarelang: ## Run HardwareLang example
	python hardwarelang/hardwarelang.py hardwarelang/examples/blink.hw

compile-hardwarelang: ## Compile HardwareLang to C
	python hardwarelang/hardwarelang.py --compile-c hardwarelang/examples/blink.hw

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.o" -delete
	find . -type f -name "*.out" -delete

install: ## Install dependencies
	pip install -r requirements.txt
