import os
import tempfile


class Editor:
    def __init__(self, content: str) -> None:
        self._content = content

    def edit(self) -> str:
        new_file, filename = tempfile.mkstemp(".yaml")
        try:
            with os.fdopen(new_file, "w") as tmp:
                tmp.write(self._content)

            os.system(f"$EDITOR {filename} || nvim {filename} || vim {filename}")

            with open(filename, "r") as tmp:
                return tmp.read()
        finally:
            os.remove(filename)
