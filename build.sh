#!/bin/bash

# Build script for GitHub Pages deployment
python3 src/main.py "/static-site/"

echo "Build complete! Site built to docs/ directory"
