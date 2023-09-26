# Makefile for ScholarlyRecommender
PYTHON=$(shell command -v python3)
PIP = $(shell command -v pip3)

ifeq (, $(PYTHON))
    $(error "PYTHON=$(PYTHON) not found in $(PATH)")
endif

ifeq (, $(PIP))
	$(error "PIP=$(PIP) not found in $(PATH)")
endif

PYTHON_VERSION_MIN=3.9
PYTHON_VERSION_CUR=$(shell $(PYTHON) -c 'import sys; print("%d.%d"% sys.version_info[0:2])')
PYTHON_VERSION_OK=$(shell $(PYTHON) -c 'import sys; cur_ver = sys.version_info[0:2]; min_ver = tuple(map(int, "$(PYTHON_VERSION_MIN)".split("."))); print(int(cur_ver >= min_ver))')
ifeq ($(PYTHON_VERSION_OK), 0)
    $(error "Need python version >= $(PYTHON_VERSION_MIN). Current version is $(PYTHON_VERSION_CUR)")
endif

ENV_DIR = env
PIP_VERSION = pip3

# Phony targets
.PHONY: all build setup install run clean

# Default target
all: setup install run

# Setup the virtual environment if it doesn't exist
setup:
	if [ ! -d "$(ENV_DIR)" ]; then \
		$(PYTHON) -m venv $(ENV_DIR); \
	fi

# Activate the virtual environment and install dependencies
install:
	if [ -d "$(ENV_DIR)/bin" ]; then \
		source $(ENV_DIR)/bin/activate && \
		$(PIP_VERSION) install -r requirements.txt; \
	elif [ -d "$(ENV_DIR)/Scripts" ]; then \
		source $(ENV_DIR)/Scripts/activate && \
		$(PIP_VERSION) install -r requirements.txt; \
	fi

build: setup install

## Run Streamlit App (virtual env already activated)
run:
	streamlit run webapp.py

# Clean the environment
clean:
	rm -rf $(ENV_DIR)