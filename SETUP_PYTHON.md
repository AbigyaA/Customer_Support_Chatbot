# Python Version Setup Guide

## Issue

You have Python 3.13.2, but Rasa currently requires Python 3.8-3.10.

## Solution: Use Python 3.10 in a Virtual Environment

### Option 1: Install Python 3.10 (Recommended)

1. **Download Python 3.10** from https://www.python.org/downloads/release/python-31011/

2. **Install Python 3.10** (make sure to check "Add Python to PATH" during installation)

3. **Create a virtual environment with Python 3.10**:
   ```bash
   # Windows
   py -3.10 -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3.10 -m venv venv
   source venv/bin/activate
   ```

4. **Verify Python version**:
   ```bash
   python --version
   # Should show: Python 3.10.x
   ```

5. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Option 2: Use pyenv (macOS/Linux)

If you have `pyenv` installed:

```bash
# Install Python 3.10
pyenv install 3.10.11

# Set local Python version
pyenv local 3.10.11

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Option 3: Use Anaconda/Miniconda

```bash
# Create environment with Python 3.10
conda create -n rasa-bot python=3.10
conda activate rasa-bot

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## Alternative: Try Latest Rasa Version (May Work)

If you want to try without changing Python version:

```bash
# Update requirements.txt to use latest version
pip install rasa rasa-sdk python-dateutil
```

Note: This may not work as Rasa may not officially support Python 3.13 yet.

## Verify Installation

After setting up Python 3.10 and installing dependencies:

```bash
# Check Rasa version
rasa --version

# Should show something like: 3.6.x or higher
```

## Next Steps

Once Python 3.10 is set up and dependencies are installed:

1. Train the model: `rasa train`
2. Start action server: `rasa run actions`
3. Start Rasa shell: `rasa shell`

See `QUICK_START.md` for detailed instructions.

