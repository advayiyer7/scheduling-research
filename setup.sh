#!/bin/bash
# Quick setup script for scheduling research project
# Run: bash setup.sh

set -e

echo "=== Setting up Scheduling Research Environment ==="

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "Error: conda not found. Please install Miniconda or Anaconda first."
    exit 1
fi

# Create conda environment
echo "Creating conda environment..."
conda create -n scheduling-research python=3.11 -y
eval "$(conda shell.bash hook)"
conda activate scheduling-research

# Install graphviz
echo "Installing Graphviz..."
conda install -c conda-forge graphviz python-graphviz -y

# Clone SAGA
echo "Cloning SAGA framework..."
if [ ! -d "saga" ]; then
    git clone https://github.com/ANRGUSC/saga.git
fi

# Install SAGA
echo "Installing SAGA..."
cd saga
pip install -e .
cd ..

# Install additional requirements
echo "Installing additional dependencies..."
pip install -r requirements.txt

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "To activate the environment:"
echo "  conda activate scheduling-research"
echo ""
echo "To run SAGA tests:"
echo "  pytest saga/tests -k 'HeftScheduler' --timeout=60"
echo ""
echo "To start Jupyter:"
echo "  jupyter lab"
