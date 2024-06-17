Little script under testing to generate a decoy fastq from a fasta file or a sequence

`python fa2fq.py <arguments>`


### Using a fasta file

`python fa2fq.py -fa <path/to/fasta_file.fa>`

`python fa2fq.py --fasta <path/to/fasta_file.fa>`



### Using a raw sequence

`python fa2fq.py -head <NameOfYourSample> -s <raw_nucleotide_sequence>`

`python fa2fq.py --head <NameOfYourSample> --sequence <raw_nucleotide_sequence>`

`python fa2fq.py --head MorexV3 --sequence GATGATCGATGCCTAGCTAG`

__________

The output will be a fastq file named and located at same place than the original fasta file
