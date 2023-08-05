import click
import sys
import os
import shutil

import logging
import csrbox.utils as utils
import csrbox.csr_gen as csr_gen
from   csrbox import __version__ as version
from   csrbox.errors import ValidationError
import riscv_config.checker as riscv_config


@click.command()
@click.version_option(prog_name="RISC-V CSRBox Generator",version=version)
@click.option('--verbose', '-v', default='info', help='Set verbose level', type=click.Choice(['info','error','debug'],case_sensitive=False))

@click.option ('--isaspec','-ispec', type=click.Path(exists=True, resolve_path=True, readable=True), help = "RISCV-CONFIG ISA File" )
@click.option ('--grpspec','-gspec', type=click.Path(resolve_path=True, readable=True, exists=True), help = "Grouping YAML File" )
@click.option('--workdir', default='./csrbox_work', type=click.Path(resolve_path=True, writable=True), help='Work directory path')
def cli(verbose, isaspec, grpspec, workdir):
    utils.setup_logging(verbose)
    logger = logging.getLogger()
    logger.handlers = []
    ch = logging.StreamHandler()
    ch.setFormatter(utils.ColoredFormatter())
    logger.addHandler(ch)

    logger.info('****** RISC-V CSRBox Generator {0} *******'.format(version))
    logger.info('Copyright (c) 2020, IIT-Madras, InCore Semiconductors Pvt. Ltd.')
    if not os.path.exists(workdir):
        logger.debug('Creating new work directory: ' + workdir)
        os.mkdir(workdir)
    else:
        logger.debug('Removing old work directory and creating new one: ' + workdir)
        shutil.rmtree(workdir)
        os.mkdir(workdir)

    try:
        isa_file = riscv_config.check_isa_specs(isaspec, workdir, True)
    except ValidationError as msg:
        logger.error(msg)
        return 1

    bsv_dir  = os.path.join(workdir, "bsv/")
    if not os.path.exists(bsv_dir):   
        logger.debug('Creating new bsv directory: ' + bsv_dir) 
        os.mkdir(bsv_dir)

    csr_gen.csr_gen(isa_file, grpspec, bsv_dir, logging=True)


 
