import easydev
import os
import tempfile
import subprocess
import sys
from sequana.pipelines_common import get_pipeline_location as getpath

sharedir = getpath('merge_flowcells')
data1 = sharedir + "/flowcell1"
data2 = sharedir + "/flowcell2"

def test_standalone_subprocess():
    directory = tempfile.TemporaryDirectory()
    cmd = """sequana_pipelines_merge_flowcells --flowcells {} {}
            --working-directory {} --force""".format(data1, data2, directory.name)
    subprocess.call(cmd.split())


def test_standalone_script():
    directory = tempfile.TemporaryDirectory()
    import sequana_pipelines.merge_flowcells.main as m
    sys.argv = ["test", "--flowcell-paths", data1, data2, 
            "--working-directory", directory.name, "--force"]
    m.main()

def test_full():

    with tempfile.TemporaryDirectory() as directory:
        print(directory)
        wk = directory

        cmd = "sequana_pipelines_merge_flowcells --flowcell-paths {} {} "
        cmd += "--working-directory {}  --force"
        cmd = cmd.format(data1, data2, wk)
        subprocess.call(cmd.split())

        stat = subprocess.call("sh merge_flowcells.sh".split(), cwd=wk)

        assert os.path.exists(wk + "/output/data_R1_001.fastq.gz")

def test_version():
    cmd = "sequana_pipelines_merge_flowcells --version"
    subprocess.call(cmd.split())

