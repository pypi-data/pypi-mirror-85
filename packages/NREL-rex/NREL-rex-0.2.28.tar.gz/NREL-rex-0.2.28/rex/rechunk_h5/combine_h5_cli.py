# -*- coding: utf-8 -*-
"""
Rechunk h5 command line interface
"""
import click
import os

from rex.rechunk_h5.combine_h5 import CombineH5
from rex.utilities.cli_dtypes import INT
from rex.utilities.loggers import init_logger


@click.command()
@click.option('--combined_h5', '-comb', type=click.Path(), required=True,
              help="Path to save combined .h5 file to")
@click.option('--source_h5', '-src', type=click.Path(exists=True),
              required=True, multiple=True,
              help="Path to source .h5 file, may supply multiple")
@click.option('--axis', '-ax', type=int, default=1,
              help='axis to combine datasets along, by default 1')
@click.option('--overwrite', '-rm', is_flag=True,
              help="Flag to overwrite an existing h5_dst file")
@click.option('--process_size', '-s', default=None, type=INT,
              help="Size of each chunk to be processed")
@click.option('--log_file', '-log', default=None, type=click.Path(),
              help='Path to .log file')
@click.option('--verbose', '-v', is_flag=True,
              help='If used upgrade logging to DEBUG')
def main(combined_h5, source_h5, axis, overwrite, process_size, log_file,
         verbose):
    """
    CombineH5 CLI entry point
    """
    if verbose:
        log_level = 'DEBUG'
    else:
        log_level = 'INFO'

    if log_file is not None:
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    init_logger('rex.rechunk_h5.combine_h5', log_file=log_file,
                log_level=log_level)

    dst_dir = os.path.dirname(combined_h5)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    CombineH5.run(combined_h5, *source_h5, axis=axis, overwrite=overwrite,
                  process_size=process_size)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        raise
