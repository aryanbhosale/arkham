#!/bin/bash
# Ensure test dependencies are installed

if [ ! -d "node_modules/vite" ] || [ ! -d "node_modules/vitest" ]; then
  echo "Installing test dependencies..."
  npm install vite@5.0.8 vitest@1.6.1 --save-dev
fi

