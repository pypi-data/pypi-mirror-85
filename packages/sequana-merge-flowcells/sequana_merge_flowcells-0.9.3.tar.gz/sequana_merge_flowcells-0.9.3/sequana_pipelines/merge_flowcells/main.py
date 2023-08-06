import sys
import os
import argparse

from sequana_pipetools.options import *
from sequana_pipetools.misc import Colors
from sequana_pipetools.info import sequana_epilog, sequana_prolog

col = Colors()

NAME = "merge_flowcells"


class Options(argparse.ArgumentParser):
    def __init__(self, prog=NAME, epilog=None):
        usage = col.purple(sequana_prolog.format(**{"name": NAME}))
        super(Options, self).__init__(usage=usage, prog=prog, description="",
            epilog=epilog,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        # add a new group of options to the parser
        so = SlurmOptions()
        so.add_options(self)

        # add a snakemake group of options to the parser
        so = SnakemakeOptions(working_directory=NAME)
        so.add_options(self)

        #so = InputOptions()
        #so.add_options(self)

        so = GeneralOptions()
        so.add_options(self)

        pipeline_group = self.add_argument_group("pipeline")

        pipeline_group.add_argument("--flowcell-paths", dest="flowcell_paths",
            required=True, nargs="+", default=[])
        pipeline_group.add_argument("--input-pattern", dest="input_pattern",
            default="*fastq.gz",
            help="""pattern for the input FastQ files (default: *fastq.gz)""")


    def parse_args(self, *args):
        args_list = list(*args)
        if "--from-project" in args_list:
            if len(args_list)>2:
                msg = "WARNING [sequana]: With --from-project option, " + \
                        "pipeline and data-related options will be ignored."
                print(col.error(msg))
            for action in self._actions:
                if action.required is True:
                    action.required = False
        options = super(Options, self).parse_args(*args)
        return options



def main(args=None):

    if args is None:
        args = sys.argv

    # whatever needs to be called by all pipeline before the options parsing
    from sequana_pipetools.options import before_pipeline
    before_pipeline(NAME)

    # option parsing including common epilog
    options = Options(NAME, epilog=sequana_epilog).parse_args(args[1:])

    from sequana.pipelines_common import SequanaManager

    # the real stuff is here. 
    manager = SequanaManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()
    from sequana import logger
    logger.level = options.level


    if options.from_project is None:
        # fill the config file with input parameters
        cfg = manager.config.config
        # There is no need for input pattern / parameters in this pipeline, just
        # the input path where fastq files are to be found.
        cfg.input_pattern = options.input_pattern
        cfg.flowcell_paths = [os.path.abspath(x) for x in options.flowcell_paths]

        if len(cfg.flowcell_paths) == 1:
            logger.error("To merge flowcells, you must provide at least two directories")
            sys.exit(1)

        for path in cfg.flowcell_paths:
            manager.exists(path)

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    # No need to check for input files since the
    # input_directory / read_tag is not used in this pipeline
    manager.teardown(check_input_files=False)


if __name__ == "__main__":
    main()
