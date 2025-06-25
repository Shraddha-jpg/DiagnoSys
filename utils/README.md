# Utils Module

This folder contains core utility modules used throughout the project. Each module is designed to encapsulate reusable logic and keep the main application code clean and modular.

## Contents

- `storage.py` — Storage management logic and data persistence.
- `models.py` — Data models and schema definitions.
- `logger.py` — Logging utilities for local and global logs.
- `clear.py` — Utility for cleaning up generated files and folders.

## Usage

Import utilities in your code as follows:
```python
from utils.storage import StorageManager
from utils.models import System, Volume
from utils.logger import Logger
```

## Contribution

- Keep utility functions generic and reusable.
- Document all public functions and classes.
- Add tests for new utilities if possible. 