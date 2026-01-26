#!/bin/bash
set -e

echo "=== Scheduling Research Setup ==="

# Check conda
if ! command -v conda &> /dev/null; then
    echo "Error: conda not found. Install Miniconda first."
    exit 1
fi

# Create environment
echo "Creating conda environment..."
conda create -n scheduling-research python=3.11 -y

# Activate
eval "$(conda shell.bash hook)"
conda activate scheduling-research

# Install graphviz
echo "Installing Graphviz..."
conda install -c conda-forge graphviz python-graphviz -y

# Clone SAGA
echo "Cloning SAGA..."
if [ ! -d "saga" ]; then
    git clone https://github.com/ANRGUSC/saga.git
fi

# Install SAGA
echo "Installing SAGA..."
cd saga
pip install -e .
cd ..

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Activate with: conda activate scheduling-research"
echo "Test with: python scripts/explore_saga.py"