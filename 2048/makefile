# Default target
.PHONY: all
all: init build

# Initialize the environment
.PHONY: init
init:
	pip install -r requirements.txt
	pip install -e .

# Build the project into a binary using PyInstaller
.PHONY: build
build:
	pyinstaller --onefile --name cw2048 main.py

# Clean up generated files
.PHONY: clean
clean:
	rm -rf build dist __pycache__ *.spec

# Run the project locally
.PHONY: run
run:
	python main.py
