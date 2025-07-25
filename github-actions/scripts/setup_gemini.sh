#!/bin/bash
# Setup Gemini CLI for GitHub Actions

set -e

echo "Setting up Gemini CLI..."

# Check if API key is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY environment variable not set"
    exit 1
fi

# Install Node.js dependencies if needed
if ! command -v node &> /dev/null; then
    echo "Node.js is required but not installed"
    exit 1
fi

# Install Gemini CLI globally
echo "Installing @google/generative-ai-cli..."
npm install -g @google/generative-ai-cli

# Verify installation
if command -v gemini &> /dev/null; then
    echo "Gemini CLI installed successfully"
    gemini --version
else
    echo "Error: Gemini CLI installation failed"
    exit 1
fi

# Configure Gemini API key
export GOOGLE_API_KEY="$GEMINI_API_KEY"

echo "Gemini CLI setup complete"