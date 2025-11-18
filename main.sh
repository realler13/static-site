#!/bin/bash

# Local development script (uses default "/" basepath)
python3 src/main.py

echo "Local build complete! Site built to docs/ directory"
echo "Starting local server on http://localhost:8888"
python3 -m http.server 8888 --directory docs
