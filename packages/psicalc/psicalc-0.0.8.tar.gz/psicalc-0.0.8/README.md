# Psi-Calc

This is a package for clustering Multiple Sequence Alignments (MSAs) utilizing normalized mutual information as a measure of relative strength. For more details visit: https://github.com/mandosoft/psi-calc.

As an example:

```
import psicalc as pc

file = "<your_fasta_file>" # e.g "PF02517_seed.txt"

data = pc.read_txt_file_format(file) # read Fasta file

pc.find_clusters(7, data) # will sample every 7th column
```

The program will run and return a csv file with the strongest clusters found in the MSA provided.
