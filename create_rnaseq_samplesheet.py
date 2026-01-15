#!/usr/bin/env python3
import os
import sys
import glob
import argparse

class CustomParser(argparse.ArgumentParser):
    def print_help(self, file=None):
        help_text = """

Description:
Generate an RNA-seq sample sheet for a given project before running the nf-core/rnaseq analysis pipeline.
The resulting CSV is printed to the screen (stdout). To save the CSV to a file, use shell redirection.

USAGE:
  create_rnaseq_samplesheet.py <ProjectID> <Strandedness> [-d <data_path>] > <output.csv>

Examples:
  create_rnaseq_samplesheet.py P001 auto > P001.csv
  create_rnaseq_samplesheet.py P001 auto -d /my/data/path > P001.csv

Arguments:
  ProjectID      Identifier for your RNA-seq project (e.g., P001)
  Strandedness   Library strandedness (forward/reverse/unstranded/auto, use 'auto' to auto-detect)

Optional arguments:
  -d, --data     Path to your RNA-seq data folder. Default: /proj/ngi2016003/nobackup/NGI/DATA
  -h, --help     Show this help message and exit
"""
        print(help_text)

def main():
    parser = CustomParser(add_help=False)
    parser.add_argument("ProjectID", help="Identifier for your RNA-seq project (e.g., P001)")
    parser.add_argument("Strandedness", help="Library strandedness (use 'auto' to auto-detect)")
    parser.add_argument("-d", "--data", default="/proj/ngi2016003/nobackup/NGI/DATA",
                        help="Path to RNA-seq data (default: %(default)s)")
    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    args = parser.parse_args()

    # Build full path to project data
    data_path = os.path.join(args.data, args.ProjectID)

    if not os.path.exists(data_path):
        sys.exit(f"Error: data path does not exist: {data_path}")

    header = "sample,fastq_1,fastq_2,strandedness"
    print(header)

    sampleList = os.listdir(data_path)
    sampleList.sort()

    for sample in sampleList:
        path_pattern = os.path.join(data_path, sample, '**', '*R1*.gz')
        paths = glob.glob(path_pattern, recursive=True)

        for counter, R1 in enumerate(paths, 1):
            R2 = R1.replace('_R1_','_R2_')
            print(f"{sample},{R1},{R2},{args.Strandedness}")


if __name__ == "__main__":
    main()

