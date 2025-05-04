#!/bin/bash

# Install dependencies
npm install --legacy-peer-deps

# Make sure node_modules/.bin is executable
chmod -R +x node_modules/.bin

# Build the project
./node_modules/.bin/vite build 