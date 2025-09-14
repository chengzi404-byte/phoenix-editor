:: Initlaze a virtual environment and install dependencies
echo "##@## #   # #####"
echo "#   # #   # #"
echo "###@# ##### #####"
echo "#     #   # #"
echo "#     #   # ##### ditor setup environment TOOL"
echo ""

echo "Setting up virtual environment..."
python -m venv .venv
.venv\Scripts\activate.bat

:: Install required packages
pip install pip --upgrade
pip install ttkbootstrap
pip install loguru
pip install easygui
pip install requests

:: Finished
echo "Environment setup complete. You can now run the application."