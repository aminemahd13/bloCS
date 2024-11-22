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
	pyinstaller --onefile --add-data "assets:assets" --name bloCS --icon=assets/graphics/bloc_2048.png main.py
# Clean up generated files
.PHONY: clean
clean:
	sudo rm -rf build dist __pycache__ *.spec

# Run the project locally
.PHONY: run
run:
	python main.py


help:
	@echo "Available targets:"
	@echo "  build    - Build the executable"
	@echo "  run      - Run the built executable"
	@echo "  clean    - Remove build artifacts"
	@echo "  help     - Display this help message"
	@echo "  init     - install dependencies"