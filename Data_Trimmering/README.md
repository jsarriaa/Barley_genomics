# VCF_Manager_V1.1
---
> Script written in Python (Version 3.11.2)

Manage big VCF files with large pool of varieties to extract smaller sized files to process data from a shorter list of varieties of interest. 
Works with z compressed files, aswell as the output one.

## Usage 

`Python VCF_Manager_V1.py <inputVCFfile.vcf.gz> `

This line will provide a list of the varieties names that are at the VCF file. 

Then, execute:

`Python VCF_Manager_V1.py <inputVCFfile.vcf.gz> -list "A, B, C, D, .. , Z" `

This will provide an output VCF.gz with only the varieties of interest, and SNP with no more of 20% of missdata among them (by default)

### Optional arguments

_Chose name and path for output file_

`-o <Output_VCFfile.vcf.gz ` 

_Change max % of allowed missing data_

`-m <0-1> (e.g. 0.5) `
