.ONESHELL:
.PHONY: create_pip_env, install_pip_req, pip_env, create_conda_env, conda_env, \
	local, activate, clean

#-------------------------------------------------------------------------
# Pip Commands
#-------------------------------------------------------------------------

# Assumes Python 3 installed as 'python' in conda on Windows, or as 'python3' on Linux

create_pip_env:
ifeq ($(OS), Windows_NT)
	python -m venv utilities-env
else
	python3 -m venv utilities-env
endif

install_pip_req:
ifeq ($(OS), Windows_NT)
	utilities-env\Scripts\python -m pip install -r requirements.txt
else
	utilities-env/bin/python3 -m pip install -r requirements.txt
endif

local_pip:
ifeq ($(OS), Windows_NT)
	utilities-env\Scripts\python -m pip install -e .
else
	utilities-env/bin/python3 -m pip install -e .
endif

pip_env: create_pip_env install_pip_req local_pip ## Create pip virtual environment and install package locally


#-------------------------------------------------------------------------
# Conda Commands
#-------------------------------------------------------------------------

# Assumes conda is on PATH env variable and using cmd if on Windows

create_conda_env:
	conda env create -f environment.yml --force 

local_conda:
ifeq ($(OS), Windows_NT)
	conda init cmd.exe
else
	conda init bash
endif
	conda activate utilities_env; pip install -e .

conda_env: create_conda_env ## Create conda virtual environment and install package locally


#-------------------------------------------------------------------------
# Self-documenting Commands
#-------------------------------------------------------------------------

.DEFAULT_GOAL := help
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'