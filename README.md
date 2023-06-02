# Filter-spectra
Filter spectra that didn't match to any peptides from mzml files 

this script takes two arguments:
1-  Directory that contains mzml files
2-  msms.txt file from the outputs of any search engine

it returns for each mzml file a new file mzml_unmatched_spectra.mzml file that contains the spectra that didn't match to any peptides


requirememts:
!pip install spectrum_io
