PYTHON := $(shell command -v python3 || command -v python)

doc:
	$(PYTHON) -m pdoc ./client.py ./globals.py ./logger.py ./math_utils.py ./nl2fetch.py ./packet.py ./wrapper.py -o ./docs
