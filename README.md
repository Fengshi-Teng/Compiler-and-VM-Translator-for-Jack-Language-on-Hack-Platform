# README

Compiler and VM Translator for Jack Language on Hack Platform

Project Overview

	This project implements two essential components for the Hack platform:

	1.	Jack Compiler: Translates Jack source code (.jack) into intermediate
	Virtual Machine (VM) language (.vm).
	2.	VM Translator: Converts VM language into Hack assembly language (.asm)
	for execution on the Hack computer.

	What is Jack Language?

	Jack is a simple, high-level programming language used in the Nand2Tetris
	course. It is designed for educational purposes, enabling students to learn
	compilation and computer architecture. Jack is a simplified version of Java
	which can be compiled and run on the Hack machine.

File Descriptions

	•	Jack Compiler: Located in src/compiler.py, responsible for parsing,
		tokenizing, and generating VM code from Jack source files.
	•	VM Translator: Located in src/VM2.py, designed to process VM code and
		output Hack assembly files.
	•	Additional project folders (project0-6, project9) contain related
		exercises and example implementations.

Requirements

	Before running the project, ensure the following requirements are met:

	Python
		This project requires the latest version of Python. It is recommended
		to use Python 3.10 or higher.

Usage
	Follow insturctions in README file in each directory.

Features

	1.	Automatic Code Cleanup:
	•	Removes comments (inline // and block-style) and blank lines.
	•	Trims leading whitespace for clean processing.
	2.	Jack Compiler:
	•	Tokenizes and parses Jack source code into structured XML.
	•	Generates VM commands based on the parsed representation.
	3.	VM Translator:
	•	Converts VM commands into Hack assembly instructions.
	•	Handles arithmetic, logical, and memory commands, including static segment management.

Author & License
	Author: Fengshi Teng
	© 2025 All Rights Reserved
