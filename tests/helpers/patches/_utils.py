"""Utilities for `tests.helpers.patches`."""

import inspect
from pathlib import Path
from typing import Set, Tuple

from koopmans.files import File


def find_test_function_name():
    """Find the name of the test function that called this function."""
    # Traverse the stack to locate the test function frame
    for frame_info in reversed(inspect.stack()):
        # Get the module where the frame was defined
        module = inspect.getmodule(frame_info.frame)
        if module and frame_info.function.startswith('test_'):
            # Return the test function name and module path
            return frame_info.function, Path(frame_info.filename)
    raise ValueError('Could not find test function in the stack')


def benchmark_filename(obj) -> Path:
    """Generate a unique filename for a benchmark file."""
    base_directory = Path(__file__).parents[3]
    benchmark_dir = base_directory / 'tests' / 'benchmarks'
    tests_dir = base_directory / 'tests'
    name = getattr(obj, 'prefix', getattr(obj, 'name', None))
    assert isinstance(name, str)
    abs_dir = obj.absolute_directory
    if tests_dir / 'tmp' in abs_dir.parents:
        benchmark_name = abs_dir.relative_to(tests_dir / 'tmp') / name
    else:
        # This is a tutorial test, which we run in the tutorials directory. Because of this, we don't have access
        # to the tmp_path automatically generated by pytest, so we need to construct something similar

        # To do so, find the top-level function that contains this test
        test_function, test_file = find_test_function_name()

        # Check that the file that we found is in the tests directory
        assert tests_dir in test_file.parents
        relative_test_file = test_file.relative_to(tests_dir)
        tutorial_dir = relative_test_file.with_name(relative_test_file.stem.replace('test_', ''))

        benchmark_name = tutorial_dir / test_function / \
            obj.absolute_directory.relative_to(base_directory / tutorial_dir) / name

    return benchmark_dir / benchmark_name.with_suffix('.pkl')


def metadata_filename(calc) -> Path:
    """Generate a unique filename for a metadata file."""
    benchmark_path = benchmark_filename(calc)
    return benchmark_path.with_name(benchmark_path.name.replace('.pkl', '_metadata.json'))


def find_subfiles_of_calc(calc) -> Set[Tuple[Path, float]]:
    """Find all subfiles of a given calculation."""
    files = find_subfiles_of_dir(calc.directory)
    if 'outdir' in calc.parameters.valid:
        files = files | find_subfiles_of_dir(calc.parameters.outdir)
    return files


def find_subfiles_of_dir(base_dir: Path) -> Set[Tuple[Path, float]]:
    """Find all files in a given directory."""
    files: Set[Tuple[Path, float]]
    if base_dir.exists():
        files = set([(x, x.stat().st_mtime) for x in base_dir.rglob('*') if x.is_file()])
    else:
        files = set([])
    return files


def recursively_find_files(obj):
    """Recursively find all files in a nested object."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from recursively_find_files(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from recursively_find_files(v)
    elif isinstance(obj, File):
        yield obj.aspath()
    elif isinstance(obj, Path):
        yield obj
    return
