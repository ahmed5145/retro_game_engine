# Installation Guide

## Prerequisites

Before installing the Retro Game Engine, ensure you have:

- Python 3.11 or higher
- pip (Python package installer)
- Poetry (optional, for development)

## Installation Methods

### Using pip (Recommended)

```bash
pip install retro-game-engine
```

### Using Poetry (For Development)

1. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone the repository:
```bash
git clone https://github.com/ahmed5145/retro_game_engine.git
cd retro_game_engine
```

3. Install dependencies:
```bash
poetry install
```

## Platform-Specific Instructions

### Windows

1. Install Python from [python.org](https://python.org)
2. Ensure Python is added to PATH during installation
3. Open Command Prompt and run:
```bash
pip install retro-game-engine
```

### macOS

1. Install Python using Homebrew:
```bash
brew install python@3.11
```

2. Install the engine:
```bash
pip3 install retro-game-engine
```

### Linux

1. Install Python and dependencies:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3-pip python3-venv

# Fedora
sudo dnf install python3.11 python3-pip
```

2. Install the engine:
```bash
pip3 install retro-game-engine
```

## Verifying Installation

Test your installation by running:

```python
from retro_game_engine import Game

print(Game.__version__)
```

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'pygame'**
   - Solution: `pip install pygame`

2. **Version conflicts**
   - Solution: Use a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     pip install retro-game-engine
     ```

3. **Permission errors**
   - Solution: Use `--user` flag:
     ```bash
     pip install --user retro-game-engine
     ```

## Next Steps

- Check out our [Quick Start Guide](getting-started.md)
- Try the [Tutorials](tutorials/README.md)
- Explore [Examples](examples/README.md)
