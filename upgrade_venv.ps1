# remove existing venv
Remove-Item -LiteralPath ".venv" -Recurse -Force

# create a fresh venv
python -m venv .venv

# activate it
.\.venv\Scripts\Activate.ps1

# upgrade pip and reinstall requirements
python -m pip install --upgrade pip
pip install -r requirements.txt