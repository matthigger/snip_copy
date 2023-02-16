import pathlib
import shutil
import tempfile

import snip_copy
from snip_copy.__main__ import main


def test_main():
    ex_hw_folder = pathlib.Path(snip_copy.__file__).parents[1] / 'test' / 'ex_hw'
    file_list = [ex_hw_folder / 'rubric.py',
                 ex_hw_folder / 'rubric.ipynb']

    for file in file_list:
        # build temp directory, load in an example file
        tmp_dir = pathlib.Path(tempfile.TemporaryDirectory().name)
        tmp_dir.mkdir()
        file_copy = tmp_dir / file.name
        shutil.copyfile(file, file_copy)

        # call "CLI"
        args = [str(file_copy), '--cmd', '# ?!', '--split', 'c']
        main(args=args)

        # check that new files are created via CLI
        assert file_copy.with_stem('rubricsolution').exists()
        assert file_copy.with_stem('rubricstudent').exists()

        # cleanup
        shutil.rmtree(tmp_dir)
