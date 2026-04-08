# AGENTS.md -- CLT_Analyzer

## Project Overview

Cross-Laminated Timber (CLT) Analyzer: a microservices application that detects machining
features (doors, windows, power outlets, etc.) in 3D STL models using graph neural networks,
localizes them, and estimates manufacturing time.

**Languages:** Python (Flask + PyTorch backend), TypeScript (Next.js + React frontend)

## Architecture

```
user_interface (Next.js :5000)
   |         |         |
   v         v         v
 MFS:5001  MFR:5002  MTE:5003
 Localizer Recognizer TimeEstimator
 (Flask+GNN each, NVIDIA CUDA required)
```

- `data_generator/` -- Synthetic CAD data generation (Python 3.8, pymadcad)
- `machining_feature_localizer/` -- GNN node classification (PyTorch Geometric, Flask)
- `machining_feature_recognizer/` -- GNN graph classification (PyTorch Geometric, Flask)
- `machining_time_estimator/` -- GNN regression (PyTorch Geometric, Flask)
- `user_interface/` -- Next.js 15 / React 19 frontend with Three.js 3D viewer

Each service has its own `Dockerfile`, `docker-compose.yml`, and `requirements.txt` (or
`package.json`). There is no root-level orchestration file or unified build system.

## Build & Run Commands

### Frontend (user_interface/)

```bash
cd user_interface
npm install            # install dependencies
npm run dev            # dev server on port 5000
npm run build          # production build
npm run start          # production server on port 5000
npm run lint           # ESLint (next/core-web-vitals + next/typescript)
```

### Python ML Services

Each Python service runs via Docker (GPU required: nvidia/cuda:12.8.0):

```bash
cd machining_feature_localizer   # or _recognizer or _time_estimator
docker compose up --build
```

To run a service locally without Docker (from its `scripts/` directory):

```bash
pip install -r requirements.txt
python __main__.py --application_mode test     # inference mode (starts Flask API)
python __main__.py --application_mode training # training mode
```

### Data Generator

```bash
cd data_generator
docker compose up --build
# or locally:
pip install -r requirements.txt
python scripts/__main__.py --number_of_models 100
```

## Testing

No test framework is currently configured for any service. If adding tests:

- **Python:** Use `pytest`. Place tests in a `tests/` directory per service. Run a single
  test with `pytest tests/test_file.py::test_function_name -v`.
- **TypeScript:** Use Jest or Vitest. Run a single test with
  `npx jest --testPathPattern="ComponentName"` or `npx vitest run src/path/to/test.ts`.

## Linting & Formatting

- **TypeScript:** ESLint is configured via `user_interface/eslint.config.mjs` (flat config
  extending `next/core-web-vitals` and `next/typescript`). Run with `npm run lint`.
- **Python:** No linter or formatter is configured. If adding one, use `ruff` for both
  linting and formatting.
- **No** `.prettierrc`, `.editorconfig`, `mypy.ini`, or pre-commit hooks exist.

## Code Style Guidelines

### Python

**File naming:** PascalCase for modules (`DataImporter.py`, `RestService.py`). This is
non-standard but consistent across the entire codebase. Follow it.

**Class naming:** PascalCase. One class per file, file name matches class name.

**Method naming:** snake_case (`training()`, `test()`, `setup_routes()`).

**Local variables:** Prefix with underscore (`_best_f1`, `_network_model`, `_test_dataset`).
This is a distinctive convention in this codebase -- all function-scoped variables use a
leading underscore. Instance attributes (`self.device`, `self.max_epoch`) do NOT use it.

**Type hints:** Largely absent. Not required by convention, but welcome for new code.

**Imports:** Group as stdlib, then third-party + local (merged), separated by a blank line.
Use `from X import Y` style. Common aliases: `import numpy as np`,
`import torch.nn.functional as f`, `import madcad as mdc`.

```python
import argparse
import os

import torch
from ManufacturingTimeRegression import ManufacturingTimeRegression
from network_models.DgcnNetwork import DgcnNetwork
from utils.DataImporter import DataImporter
from utils.RestService import RestService
```

**No `__init__.py` files.** Services rely on flat `scripts/` directories with PYTHONPATH
set in Dockerfiles.

**Docstrings:** Virtually absent. Comments are a mix of English and German.

### TypeScript

**Component files:** PascalCase (`WireframeViewer.tsx`), one per folder matching the name.
All use `"use client";` directive (Next.js App Router). Export as
`export default function ComponentName(...)`.

**Utility files:** camelCase (`restService.ts`, `fileService.ts`). Use named exports.

**Types:** TypeScript strict mode is enabled. Define `interface` for component props.
Functions should have typed parameters and return types.

**Imports:** Framework first (react, next), libraries second (@mui, three), local last
(@/components/..., @/utils/...).

```tsx
import React, { useState } from "react";
import { Container, Dialog } from "@mui/material";
import WireframeViewer from "@/components/WireframeViewer/WireframeViewer";
import { handleFileUpload, STLFile } from "@/utils/fileService";
```

### Error Handling

**Python:** Use `try/except` with `print()` for errors. Return sensible defaults on
failure. No custom exception classes exist; `ValueError` is raised for invalid config.

```python
try:
    os.remove(file_path)
except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print(f"Could not delete file: {e}")
```

**TypeScript:** Use `try/catch` with `console.error()`. Return `null` or `[]` on failure,
never re-throw.

```typescript
try {
    const response = await fetch(url);
    if (!response.ok) {
        console.error("REST API error:", response.status);
        return null;
    }
    return await response.json();
} catch (error) {
    console.error("Network error:", error);
    return null;
}
```

### Logging

No logging framework is used. Python uses `print()`, TypeScript uses `console.log()` /
`console.error()`. Emoji characters are used as informal severity markers in both languages.

## Key Patterns

### Flask REST Service (Python)

All three ML services share an identical class-based Flask pattern in `utils/RestService.py`:

```python
class RestService:
    def __init__(self, domain_object):
        self.app = Flask(__name__)
        CORS(self.app)
        self.setup_routes()
    def setup_routes(self):
        @self.app.route('/processstlmodel', methods=['POST'])
        def process_stl_model(): ...
```

### Neural Network Models (Python)

All GNN models subclass `torch.nn.Module` with a consistent interface:
`__init__`, `forward`, `train_loss`, `val_loss`, `test`. The `@torch.no_grad()` decorator
is used on `test()` methods.

### Entry Points (Python)

All `__main__.py` files use `argparse` with `--application_mode` (training | test).
Training mode runs the training loop; test mode starts the Flask REST API.

### Manual Resource Cleanup (Python)

After inference, code explicitly removes processed `.pt` and `.stl` files and uses `del`
for manual garbage collection of datasets and models.

## Common Pitfalls

- **Hardcoded URLs:** Frontend `restService.ts` uses `http://127.0.0.1:500X` -- not
  configurable via env vars.
- **GPU required:** ML service Docker images need NVIDIA GPU with CUDA 12.8.
- **Code duplication:** The three ML services share near-identical `RestService.py`,
  `DataImporter.py`, `HyperParameter.py`, and `network_models/` -- changes often need
  replication across all three.
- **No shared library:** There is no common package; each service is fully independent.
- **Committed artifacts:** Some `__pycache__/` and `.idea/` files are tracked in git.
- **Mixed language comments:** Code comments and error messages use both English and German.
