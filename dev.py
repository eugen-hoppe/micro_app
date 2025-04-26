from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent


if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.application:app",
        host=os.getenv("DEV_HOST", "127.0.0.1"),
        port=int(os.getenv("DEV_PORT", "8504")),
        reload=True,
    )
