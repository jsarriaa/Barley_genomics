# %% [markdown]
# Script ready to work as notebook or as comand line program (python)

# %%
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import os
import argparse

parser = argparse.ArgumentParser(description='Convert a FASTA file to a FASTQ file.')
parser.add_argument('-fa', '--fasta', help='The input FASTA file.')
parser.add_argument('-s', '--sequence', help='The sequence to use if no FASTA file is provided.')
parser.add_argument('-head', '--head', help='If provided, the header to use for the FASTQ file.')
args = parser.parse_args()

input_fasta = None

if args.fasta:
    with open(args.fasta, 'r') as file:
        first_line = file.readline()
    if first_line.startswith(">"):
        input_fasta = args.fasta
    else:
        print("This is not a proper FASTA file.")
        exit()

else:
    if not args.fasta:
        if not args.sequence:
            print("You need to provide a sequence to convert to FASTQ. Use -s or --sequence <sequence>, or provide a FASTA file with -fa or --fasta <input.fasta>.")
            exit()
        if args.sequence.startswith(">"):
            sequence = args.sequence
        else:
            if not args.head:
                print("You need to specify a header for the sequence. Use -head or --head <gene_name>.")
                exit()
            else:
                input_fasta = ">" + args.head + "\n" + args.sequence

# %%
#Determine fastq file of output

if args.fasta:
    input_file = args.fasta
base_name = os.path.basename(input_file)
name_without_extension = os.path.splitext(base_name)[0]
directory = os.path.dirname(input_file)
output_file = os.path.join(directory, name_without_extension + ".fastq")
output_fastq = open(output_file, "w")

if not args.fasta:
        output_file = os.path.join(directory, args.head + ".fastq")
        output_fastq = open(output_file, "w")

# %%
#Convert FASTA to FASTQ

#complain if input_fasta is not defined
if not input_fasta:
    print("You need to provide a FASTA file to convert to FASTQ. Use -fa or --fasta <input.fasta>.")
    exit()
for record in SeqIO.parse(input_fasta, "fasta"):
    seq = str(record.seq)
    qual = "~" * len(seq)
    fastq_record = SeqRecord(record.seq, id=record.id, name=record.name, description=record.description)
    fastq_record.letter_annotations["phred_quality"] = [ord(letter) - 33 for letter in qual]
    SeqIO.write(fastq_record, output_fastq, "fastq")





