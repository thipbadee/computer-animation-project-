from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def run_web(host: str, port: int):
    from app import app

    app.run(host=host, port=port, debug=True, threaded=True)


def run_benchmark():
    from experiments.benchmark import main

    main()


def run_demo():
    from visualization.animate_results import main

    main()


def main():
    parser = argparse.ArgumentParser(description="Computer Animation project entry point")
    parser.add_argument(
        "--mode",
        choices=["web", "benchmark", "demo"],
        default="web",
        help="Execution mode",
    )
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    if args.mode == "benchmark":
        run_benchmark()
    elif args.mode == "demo":
        run_demo()
    else:
        run_web(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
