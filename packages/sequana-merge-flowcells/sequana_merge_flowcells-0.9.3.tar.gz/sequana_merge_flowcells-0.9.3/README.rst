This is is the **merge_flowcells** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ project

:Overview: Merge gzipped FastQ files from several flowcells
:Input: set of identically named FastQ files from several directories
:Output: merged FastQ files stored in an output directory. 
:Status: mature
:Citation: Cokelaer et al, (2017), ‘Sequana’: a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI doi:10.21105/joss.00352


Installation
~~~~~~~~~~~~

You must install Sequana first::

    pip install sequana

Then, just install this package::

    pip install sequana_merge_flowcells


Usage
~~~~~

::

    sequana_pipelines_merge_flowcells --help
    sequana_pipelines_merge_flowcells --input-directory DATAPATH 

This creates a directory with the pipeline and configuration file. You will then need 
to execute the pipeline::

    cd merge_flowcells
    sh merge_flowcells.sh  # for a local run

This launch a snakemake pipeline. If you are familiar with snakemake, you can 
retrieve the pipeline itself and its configuration files and then execute the pipeline yourself with specific parameters::

    snakemake -s merge_flowcells.rules -c config.yaml --cores 4 --stats stats.txt

Or use `sequanix <https://sequana.readthedocs.io/en/master/sequanix.html>`_ interface.

Requirements
~~~~~~~~~~~~

This pipelines requires the following executable(s):

- sequana
- pigz
- zcat

.. image:: https://raw.githubusercontent.com/sequana/sequana_merge_flowcells/master/sequana_pipelines/merge_flowcells/dag.png


Details
~~~~~~~~~

This pipeline runs **merge_flowcells** in parallel on the input fastq files (paired or not). 
You have to provide at least two subdirectories. You may provide more. 
The input FastQ files must be zipped in the current version. The input FastQ
files found in the first directory muts be found in all subsequent directories.


Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/sequana_merge_flowcells/master/sequana_pipelines/merge_flowcells/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file. 

Changelog
~~~~~~~~~

========= ====================================================================
Version   Description
========= ====================================================================
0.0.1     **First release.**
========= ====================================================================


