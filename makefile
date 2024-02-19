doc:
	python -m pdoc ./client.py ./globals.py ./logger.py ./math_utils.pu ./nl2fetch.py ./packet.py ./wrapper.py -o ./docs

doc-mac:
	python3 -m pdoc ./client.py ./globals.py ./logger.py ./math_utils.pu ./nl2fetch.py ./packet.py ./wrapper.py -o ./docs