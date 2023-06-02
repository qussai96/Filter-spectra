#!/usr/bin/env python

from spectrum_io.raw.msraw import MSRaw
import pandas as pd
from pathlib import Path
import sys

# get a list of nmatched spectra
def get_unmatshed_spectra(mzml_directory, msms_file):
    # convert mzml to dataframe
    raw_df = MSRaw.read_mzml(mzml_directory)

    # read_msms.txt
    msms_df = pd.read_csv(msms_file, sep='\t', index_col=False, header=0)
    msms_df.rename(columns={'Scan number': 'SCAN_NUMBER'}, inplace=True)

    # filter non matched spectra based on scan number
    merged_df = pd.merge(raw_df, msms_df, on='SCAN_NUMBER', how='inner')
    unmatched_df = raw_df[~raw_df['SCAN_NUMBER'].isin(merged_df['SCAN_NUMBER'])]
    unmatched_spectra = unmatched_df['SCAN_NUMBER'].tolist()

    # stat
    print(f'msms_file has: {len(msms_df)} scans')
    print(f'number of matched spectra: {len(raw_df)} scans')
    print(f'number of unmatched spectra: {len(unmatched_df)} scans')
    return unmatched_spectra

# iterate over all mzml files in the given directory
def process_mzml_directory(directory, unmatched_spectra):
    path = Path(directory)
    mzml_files = path.glob("*.mzML")
    for mzml_file in mzml_files:
        unmatched_file = mzml_file.with_name(f"{mzml_file.stem}_unmatched_spectra.mzML")
        remove_spectra(mzml_file, unmatched_file, unmatched_spectra)
        
# take mzml file and return a new file with the unmatched spectra
def remove_spectra(mzml_file, unmatched_file, unmatched_spectra):
    with open(mzml_file, 'r') as file:
        lines = file.readlines()

    output_lines = []
    skip_next_lines = False

    for line in lines:
        if skip_next_lines:
            if line.strip() == '</spectrum>':
                skip_next_lines = False
            continue

        if '<spectrum id=' in line:
            scan_number = int(line.split('scan=')[1].split()[0].strip('"'))
            if scan_number not in unmatched_spectra:
                skip_next_lines = True
                continue

        output_lines.append(line)

    with open(unmatched_file, 'w') as file:
        file.writelines(output_lines)


def main(argv):
    mzml_directory = argv[0]
    msms_file = argv[1]
    unmatched_spectra = get_unmatshed_spectra(mzml_directory, msms_file)
    process_mzml_directory(mzml_directory, unmatched_spectra)

if __name__ == "__main__":
    main(sys.argv[1:])
