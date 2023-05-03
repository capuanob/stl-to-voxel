#!/usr/bin/env python3
import atheris
import sys
import fuzz_helpers
import io
import contextlib

with atheris.instrument_imports(include=(['stltovoxel'])):
    import stltovoxel
@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = io.StringIO()
    yield
    sys.stdout = save_stdout

def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    with fdp.ConsumeTemporaryFile(suffix='.stl', all_data=True, as_bytes=True) as f, nostdout():
        try:
         stltovoxel.convert_file(f, '/dev/null')
        except (ValueError, TypeError, AssertionError):
            return -1

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
