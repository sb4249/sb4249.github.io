SHELL := /bin/bash

#Compiler and flag settings
CC=gcc			#GCC Compiler is the default
CFLAGS=-g		#Build with debugging enabled by default

#HELP
.PHONY: help
help:
	@echo "Usage make <TARGET>"
	@echo ""
	@echo "  Targets:"
	@echo "	   build				Build the server executable"
	@echo "	   run					Run the server"
	@echo "	   clean				Remove the server executable"

.PHONY: build
build: server.c
	$(CC) $(CFLAGS) -o server server.c 

.PHONY: run
run: server
	./server

.PHONY: clean
clean:
	rm -f server