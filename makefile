ifeq ($(OS),Windows_NT)
    detected_OS := Windows
	python_command := python
else
    detected_OS := Unix
	python_command := python3
endif

doc:
	$(python_command) -m pdoc ./client.py ./globals.py ./logger.py ./math_utils.pu ./nl2fetch.py ./packet.py ./wrapper.py -o ./docs