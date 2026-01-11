import os
import subprocess
from typing import Final

from picobuild import build_cython_executable

if __name__ == "__main__":
    # Paths
    SRC_FILE: Final[str] = __file__.replace("cy_exec.py", "executable.py")
    DST_FILE: Final[str] = __file__.replace("cy_exec.py", "bin/executable")

    os.makedirs(os.path.dirname(DST_FILE), exist_ok=True)

    # Build the executable
    build_cython_executable(SRC_FILE, DST_FILE)

    # Run the executable
    subprocess.run([DST_FILE], check=True)

    # Clean up
    os.remove(DST_FILE)
    os.remove(DST_FILE + ".c")

    # Remove bin directory if empty
    bin_dir = os.path.dirname(DST_FILE)
    if os.path.isdir(bin_dir) and not os.listdir(bin_dir):
        os.rmdir(bin_dir)
