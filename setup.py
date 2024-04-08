import sys

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os"],  # Add additional packages as needed
    "include_files": ["./Chrome/", "startChromeDebug.bat", "addEnv.bat", "./config.ini", "./app.ico"]  # Include non-python files
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"
icon="app.ico"
setup(
    name="my_app",
    version="0.1",
    description="My application description",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, icon=icon)]
)
