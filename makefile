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
	pyinstaller --onefile --name bloCS \
		--add-data 'assets:assets' \
		--add-data 'assets/graphics/background/background.png:assets/graphics/background' \
		main.py

# Clean up generated files
.PHONY: clean
clean:
	rm -rf build dist *.spec

.PHONY: rebuild
rebuild:
	make clean
	make build