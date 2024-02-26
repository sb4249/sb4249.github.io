ifeq ($(OS),Windows_NT)
    detected_OS := Windows
    python_command := python
else
    detected_OS := Unix
    python_command := python3
endif

doc:
	$(python_command) -m pdoc ./client.py ./globals.py ./logger.py ./math_utils.py ./nl2fetch.py ./packet.py ./wrapper.py -o ./docs --logo "https://media.discordapp.net/attachments/1120127851354652725/1171201942203142234/DALLE_Motion_Simulator_Logo.png?ex=65e63f4e&is=65d3ca4e&hm=2a1693ae1370d834bc084fee25e1b18df0de53813e6615aef2cde3a540d3babf&=&format=webp&quality=lossless&width=910&height=910"
