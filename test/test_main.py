import pathlib
import shutil
import tempfile

from snip_copy.__main__ import main


def test_main():
    # build temp directory, load in an example file
    tmp_dir = pathlib.Path(tempfile.TemporaryDirectory().name)
    tmp_dir.mkdir()
    file = pathlib.Path('.') / 'ex_hw' / 'rubric.py'
    file_copy = tmp_dir / file.name
    shutil.copyfile(file, file_copy)

    # call "CLI"
    args = [str(file_copy), '--cmd', '# ?!', '--split', 'c']
    main(args=args)

    # check that new files are created via CLI
    assert (tmp_dir / 'rubricsolution.py').exists()
    assert (tmp_dir / 'rubricstudent.py').exists()

    # cleanup
    shutil.rmtree(tmp_dir)
