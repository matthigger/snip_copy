import pathlib
import shutil
import tempfile

import snip_copy
from snip_copy.ipynb.__main__ import main


def test_main():
    # build temp directory, load in an example file
    tmp_dir = pathlib.Path(tempfile.TemporaryDirectory().name)
    tmp_dir.mkdir()
    file = pathlib.Path(snip_copy.__file__).parents[1] / 'test' / 'ex_hw' / 'rubric.ipynb'
    file_copy = tmp_dir / file.name
    shutil.copyfile(file, file_copy)

    # call "CLI"
    args = [str(file_copy), '--cmd', '# ?!', '--split', 'c']
    main(args=args)

    # check that new files are created via CLI
    assert (tmp_dir / 'rubricsolution.ipynb').exists()
    assert (tmp_dir / 'rubricstudent.ipynb').exists()

    # cleanup
    shutil.rmtree(tmp_dir)
