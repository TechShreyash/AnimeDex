from app import app
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


if __name__ == "__main__":
    app.run()
