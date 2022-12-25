default: help

.PHONY: help 
help: ## print this help message: see https://stackoverflow.com/a/64996042
	@echo 'Usage:'
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-22s\033[0m %s\n", $$1, $$2}'

.PHONY: confirm 
confirm: ## confirm y or N
	@echo -n 'Are you sure? [y/N] ' && read ans && [ $${ans:-N} = y ]

.PHONY: run
run: ## run src/main.py
	python src/main.py