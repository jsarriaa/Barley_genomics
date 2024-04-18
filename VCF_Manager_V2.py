# %%
#Code prepaired to extract from a big VCF file a smaller one with only the columns of interest varieties.
#The code will also remove the lines with more than 20% missing data.
#This file will be quiclky processed by Distance.py to calculate the genetic distance between the varieties.

import subprocess
import re
import csv
import gzip
import argparse

parser = argparse.ArgumentParser(description="This script extracts a subset of a VCF file and removes lines with more than 20% missing data.\n The output file will be used to calculate the genetic distance between the varieties.\n The script will also create a dictionary with the varieties of interest and the columns of the VCF file that correspond to them.\n Please, run the script a first time to create a dictionary with the varieties names.\n Run it twice adding the list of varieties to add.", usage="%(prog)s [--inputVCFfile INPUTVCFFILE] --outVCFfile OUTVCFFILE --interestlist INTERESTLIST")# Add the arguments
parser.add_argument('inputVCFfile', type=str, nargs='?', default='Empty', help='The input VCF file path')
parser.add_argument('--outVCFfile', '-o', type=str, required=False, help='The output VCF file name and path')
parser.add_argument('--interestlist', '-list', type=str, required=False, help='The input list of varieties of interest (e.g. -list "A, B ,C")')
parser.add_argument('--missdata', '-m', type=float, required=False, help='The maximum percentage of missing data allowed [range 0-1] (e.g. -m 0.2) by default is 0.2')
# Parse the arguments
args = parser.parse_args()

Varieties_dictionary = {}
InterestList_Columns = []


# %%
# Insert VCF file and the names of the varieties of interest
VCFfile = args.inputVCFfile
InterestList_Names = [args.interestlist]

#If you run the script without the names of the varieties of interest, the script will print the names of the varieties present in the VCF file
if VCFfile == "Empty":
    print("I have not found the VCF file. Please insert the path to the file as an argument. Get some help with --help.")
    print("\n")
    exit()

else:
    if InterestList_Names == [None]:
        print("I have not found the list of varieties of interest. Please insert the list as an argument. Get some help with --help.")
        print("You did not specify the list of varieties of interest. Here is a list of the varieties present in the VCF file:")
        extract_names_cdm = f'zcat {VCFfile} | perl -lane \'if(/^#CHROM\t/){{ foreach $c (0 .. $#F){{ $cr=$c+1; print "$cr\t$F[$c]" }}; last }}\' | cut -f 2 | tail -n +10'
        print("\n")
        print(subprocess.check_output(extract_names_cdm, shell=True).decode())
        print("\n")
        print("Run the script adding your varieties as a list: -list \"A, B, C")
        exit()
    else : 
        print(InterestList_Names)

#Prepare the imputated list to be processed as a python list
if args.interestlist is not None:
    InterestList_Names = args.interestlist.split(', ')
else:
    InterestList_Names = []

#Exported file name
if args.outVCFfile is None:
    Output_file = 'output.vcf.gz'   #Default name
else:
    Output_file = args.outVCFfile


#Use this lines if you already have a file with the names of the varieties of interest
#InterestsList_Names = "" #Insert the path to the file with the names of the varieties of interest here



# %%

#Define the dictionary with the names of the varieties of interest and each column number in the VCF file
perl_cmd_dictionary = f'zcat {VCFfile} | perl -lane \'if(/^#CHROM\t/){{ foreach $c (0 .. $#F){{ $cr=$c+1; print "$cr\\t$F[$c]" }}; last }}\''

#Execute the perl command to get the dictionary
perl_cmd_dictionary_output = subprocess.check_output(perl_cmd_dictionary, shell=True).decode('utf-8').strip()
#print(perl_cmd_dictionary_output)

# Create a dictionary from the output
Varieties_dictionary = dict(item.split('\t')[::-1] for item in perl_cmd_dictionary_output.split('\n') if '\t' in item)
#print(Varieties_dictionary)

try:
    InterestList_Columns = [Varieties_dictionary[variety] for variety in InterestList_Names]
except KeyError:
    print("One of the varieties of interest is not present in the VCF file. Please, check the names of the varieties and try again. Here is a list of the varieties present in the VCF file:")
    extract_names_cdm = f'zcat {VCFfile} | perl -lane \'if(/^#CHROM\t/){{ foreach $c (0 .. $#F){{ $cr=$c+1; print "$cr\t$F[$c]" }}; last }}\' | cut -f 2 | tail -n +10'
    print("\n")
    print(subprocess.check_output(extract_names_cdm, shell=True).decode())
    print("\n")
    print("Run the script adding your varieties as a list: -list \"A, B, C")
    exit()

InterestList_Columns_string = ','.join(map(str, InterestList_Columns))      #Thats to prepare the string to be used in the next command


# Have in mind that from column 1 to 9 are the information of the SNP, so the names of the varieties start from column 10
print(InterestList_Columns_string)

#Check a column number
#print(Varieties_dictionary['INSERTHEREVARIETYNAME'])





# %%
#command to cut the VCF file and remove the lines with more than 20% missing data
if args.missdata is None:
    args.missdata = 0.2 #default value

perl_cmd_cut = f'zcat {VCFfile} | cut -f 1-9,{InterestList_Columns_string} | perl -lane \'if(/^#/){{ print }} else {{ $M=0; while(/\\.\\/\\.:/g){{ $M++ }}; $M/=($#F-8) if ($#F > 8); print if($M <= {args.missdata}) }}\''
#print(perl_cmd_cut)

#Execute the perl command to get the dictionary
perl_cmd_cut_output = subprocess.check_output(perl_cmd_cut, shell=True).decode('utf-8', 'ignore').strip()
#print(perl_cmd_cut_output)

#Export the output to a file .vcf
with open('temporal_output', 'w') as f:
    f.write(perl_cmd_cut_output)

#Compress the file into a .vcf.gz
subprocess.run(f'bgzip -c temporal_output > {Output_file}', shell=True)


# %%
#Reminder to index
print("Don\'t forget to index the file with bcftools before merging it with the other vcf.gz files.")

#Remove the temporal file
subprocess.run('rm temporal_output', shell=True)


