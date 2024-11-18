# 2048 Game

This project is a Python implementation of the popular 2048 game, featuring modular design and easy-to-use commands for setup and execution.

## Features
- Random tile generation with scoring logic.
- Intuitive controls for grid-based moves.
- Modular structure for easier development and testing.

## Requirements
Ensure Python is installed on your system, and then set up the required dependencies.

## Setup and Build Commands

### Using the Makefile
The project includes a `Makefile` to simplify common tasks:

1. **Initialize the Environment**:
   Installs dependencies and sets up the project for development:
   ```bash
   make init
   ```

2. **Build the Game**:
   Compiles the project into a standalone binary using PyInstaller:
   ```bash
   make build
   ```
   The resulting binary will be located in the `dist/` directory as `cw2048`.

3. **Run the Game**:
   To run the project locally:
   ```bash
   make run
   ```

4. **Clean the Project**:
   Removes generated files and directories:
   ```bash
   make clean
   ```

## Running Tests
To verify the functionality:
```bash
python -m unittest discover tests
```

## License
This project is licensed. See the `LICENSE` file for details.
```
