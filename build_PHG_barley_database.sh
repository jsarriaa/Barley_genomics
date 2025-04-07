# Date: 26.03.2025
# Works with PHGv2 
# citation: 10.1093/bioinformatics/btac410
# Used in version phg version 2.4.52.207

# Last update: 07.04.2025
# Time for a full run: Approx 3 days
# Space used arround 500gb nowadays

###
# _________________________________________________________________________________________________
###


# Remember to run with proper conda environment
conda activate phgv2-conda
phg --version

# Update the proper conda env:

# phg setup-environment
# Commented to avoid it during tests

# Generate necessary folders
mkdir -p data
mkdir -p output
mkdir -p vcf_dbs
mkdir -p output/alignment_files
mkdir -p output/vcf_files
mkdir -p gmap_db

# Initialize the database
phg initdb --db-path vcf_dbs/

# Get the genomes
# from the folder:
# https://galaxy-web.ipk-gatersleben.de/libraries/folders/Fd071e794759ab192
# citation: https://doi.org/10.1038/s41586-024-08187-1

# Download the genomes
# https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783365.1?download=true&gzip=true   HOR_14121
# https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783375.1?download=true&gzip=true   HOR_21595
# https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783475.1?download=true&gzip=true   HOR_3474
# https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783295.1?download=true&gzip=true   HOR_13942
# https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783435.1?download=true&gzip=true   HOR_21599
# https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783415.1?download=true&gzip=true   HOR_3365
# https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783545.1?download=true&gzip=true   HOR_2830
# https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783585.1?download=true&gzip=true   HOR_10892
# https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783485.1?download=true&gzip=true   HOR_2779
# https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783555.1?download=true&gzip=true   HOR_1168
# https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783505.1?download=true&gzip=true   HOR_12184
# https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_904849725.1?download=true&gzip=true   MorexV3

if [ ! -f data/HOR_14121.fasta.gz ] && [ ! -f data/HOR_14121.fa ]; then
    wget "https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783365.1?download=true&gzip=true" -O data/HOR_14121.fasta.gz
fi
if [ ! -f data/HOR_21595.fasta.gz ] && [ ! -f data/HOR_21595.fa ]; then
    wget "https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783375.1?download=true&gzip=true" -O data/HOR_21595.fasta.gz
fi
if [ ! -f data/HOR_3474.fasta.gz ] && [ ! -f data/HOR_3474.fa ]; then
    wget "https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783475.1?download=true&gzip=true" -O data/HOR_3474.fasta.gz
fi
if [ ! -f data/HOR_13942.fasta.gz ] && [ ! -f data/HOR_13942.fa ]; then
    wget "https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783295.1?download=true&gzip=true" -O data/HOR_13942.fasta.gz
fi
if [ ! -f data/HOR_21599.fasta.gz ] && [ ! -f data/HOR_21599.fa ]; then
    wget "https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783435.1?download=true&gzip=true" -O data/HOR_21599.fasta.gz
fi
if [ ! -f data/HOR_3365.fasta.gz ] && [ ! -f data/HOR_3365.fa ]; then
    wget "https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783415.1?download=true&gzip=true" -O data/HOR_3365.fasta.gz
fi
if [ ! -f data/HOR_2830.fasta.gz ] && [ ! -f data/HOR_2830.fa ]; then
    wget "https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783545.1?download=true&gzip=true" -O data/HOR_2830.fasta.gz
fi
if [ ! -f data/HOR_10892.fasta.gz ] && [ ! -f data/HOR_10892.fa ]; then
    wget "https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783585.1?download=true&gzip=true" -O data/HOR_10892.fasta.gz
fi
if [ ! -f data/HOR_2779.fasta.gz ] && [ ! -f data/HOR_2779.fa ]; then
    wget "https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783485.1?download=true&gzip=true" -O data/HOR_2779.fasta.gz
fi
if [ ! -f data/HOR_1168.fasta.gz ] && [ ! -f data/HOR_1168.fa ]; then
    wget "https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783555.1?download=true&gzip=true" -O data/HOR_1168.fasta.gz
fi
if [ ! -f data/HOR_12184.fasta.gz ] && [ ! -f data/HOR_12184.fa ]; then
    wget "https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_949783505.1?download=true&gzip=true" -O data/HOR_12184.fasta.gz
fi
if [ ! -f data/MorexV3.fasta.gz ] && [ ! -f data/MorexV3.fa ]; then
    wget "https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_904849725.1?download=true&gzip=true" -O data/MorexV3.fasta.gz
fi

# Check if there are files ending in .fasta.gz in the /data directory
if ls data/*.fasta.gz 1> /dev/null 2>&1; then
    # Unzip and change the chromosome names for all files in /data ending with .fasta.gz
    for genome_file in data/*.fasta.gz; do
        output_file="data/$(basename "$genome_file" .fasta.gz).fa"
        sample_name=$(basename "$genome_file" .fasta.gz)
        if [ ! -f "$output_file" ]; then
            zcat "$genome_file" | perl -lne 'if(/^>ENA\|[^|]+\|(\S+).*?chromosome: (\S+)/){ print ">chr$2 sampleName='"$sample_name"'" } else { last if(/^>/); print }' > "$output_file"
            # rm "$genome_file" # Commented for debugging purposes
        fi
    done
else
    echo "No .fasta.gz files found in the data/ directory. Skipping this step."
fi


# # Execute prepare assemblies from PHG (but only if there is a file that should exists that does not)    ## Uses 32 threads
# for genome_file in "${genome_files[@]}"; do
#    output_file="data/prepared_assemblies/$(basename "$genome_file" .fasta.gz).fa"
#    if [ ! -f "$output_file" ]; then
#        echo "phg prepare_assemblies --keyfile data/prepare_assemblies.txt --output-dir data/prepared_assemblies/ --threads 32"
#        phg prepare-assemblies --keyfile data/prepare_assemblies.txt --output-dir data/prepared_assemblies/ --threads 32
#        break
#    fi
#done
#########   EVERYTHING COMMENTED, BECAUSE THE FILES ARE ALREADY PREPARED AT THIS VERSION OF THE SCRIPT ######################


### Download Morex.gff

if [ ! -f data/MorexV3.gff ]; then
    wget "https://doi.ipk-gatersleben.de/DOI/b2f47dfb-47ff-4114-89ae-bad8dcc515a1/5d16cc17-c37f-417f-855d-c5e72c721f6c/1/DOWNLOAD" -O data/RAW_MorexV3.gff
fi
# Not necessary to modify the gff due chromosomes names: already match with the prepared fasta files
# But remove all is not in 7 chromosomes

if [ ! -f data/MorexV3.gff ]; then
    perl -ne 'if(/^chr[1-7]H\t/){print}' data/RAW_MorexV3.gff > data/MorexV3.gff
    rm data/RAW_MorexV3.gff
fi

# Prepare reference-ranges
if [ ! -f output/ref_ranges.bed ]; then
    phg create-ranges --gff data/MorexV3.gff --boundary gene -o output/ref_ranges.bed --reference-file data/MorexV3.fa
fi


# if exists the keyfile for the aligment, delete it
if [ -f data/alignment_keyfile.txt ]; then
    rm data/alignment_keyfile.txt
fi

# Create the keyfile for the alignment
# Check if the .fa files exist in the data/ directory
# If they do, create the keyfile, but not "creating" a "*.fa" file
if ls data/*.fa 1> /dev/null 2>&1; then
    for prepared_file in data/*.fa; do
        if [[ "$(basename "$prepared_file")" != "MorexV3.fa" ]]; then
            echo "$prepared_file" >> data/alignment_keyfile.txt
        fi
    done
else
    echo "No .fa files found in the data/ directory."
fi

# Save in a variable the genome files
genome_files=(data/*.fa)

# Align assemblies
# Execute align_assemblies from PHG (but only if there is a file that should exists that does not)    ## Uses 32 threads
for genome_file in "${genome_files[@]}"; do
    if [[ "$(basename "$genome_file" .fa)" == "MorexV3" ]]; then
        continue
    fi
    if [ ! -f "output/alignment_files/$(basename "$genome_file" .fa).maf" ]; then
        phg align-assemblies --gff data/MorexV3.gff -o output/alignment_files/ --total-threads 32 --in-parallel 2 --assembly-file-list data/alignment_keyfile.txt --output-dir output/alignment_files/ --reference-file data/MorexV3.fa
        break
    fi
done


# Checkpoint. Script only continues if the alignment files are created
for genome_file in "${genome_files[@]}"; do
    if [[ "$(basename "$genome_file" .fa)" == "MorexV3" ]]; then
        continue
    fi
    if [ ! -f "output/alignment_files/$(basename "$genome_file" .fa).maf" ]; then
        echo "Alignment files not created for $(basename "$genome_file" .fa). Exiting script."
        exit 1
    fi
done

# Build the agc file to store the genomes
if [ ! -f vcf_dbs/assemblies.agc ]; then
    phg agc-compress --db-path vcf_dbs/ --fasta-list data/alignment_keyfile.txt --reference-file data/MorexV3.fa
fi

# Create the reference VCF
if [ ! -f vcf_dbs/hvcf_files/MorexV3.h.vcf.gz ]; then
    phg create-ref-vcf --bed output/ref_ranges.bed --reference-file data/MorexV3.fa --reference-name MorexV3 --db-path vcf_dbs/
fi

# Create from allignments the VCFs
# Execute create-maf-vcf from PHG (but only if there is a file that should exists that does not)    ## Uses 32 threads
for genome_file in "${genome_files[@]}"; do
    if [[ "$(basename "$genome_file" .fa)" == "MorexV3" ]]; then
        continue
    fi
    if [ ! -f "output/vcf_files/$(basename "$genome_file" .fa).h.vcf.gz" ]; then
        phg create-maf-vcf --bed output/ref_ranges.bed --reference-file data/MorexV3.fa -o output/vcf_files/ --db-path vcf_dbs/ --skip-metrics --maf-dir output/alignment_files/
    fi
done

# Set a checkpoint to see if the files are already created
for genome_file in "${genome_files[@]}"; do
    output_file="data/$(basename "$genome_file" .fa).fa"

    if [ ! -f "vcf_dbs/hvcf_files/$(basename "$genome_file" .fa).h.vcf.gz" ]; then
        phg load-vcf --db-path vcf_dbs/ --vcf-dir output/vcf_files/ --threads 32
        break
    fi
done


# Generate necessary files: hapIDranges:
if [ ! -f output/hapIDranges.tsv ]; then
    phg sample-hapid-by-range --input-dir vcf_dbs/hvcf_files/ --output-file output/hapIDranges.tsv
fi

# Generate necessary files: hapIDranges:
if [ ! -f output/hapIDtable.tsv ]; then
    phg hapid-sample-table --hvcf-dir vcf_dbs/hvcf_files/ --output-file output/hapIDtable.tsv
fi

# Generate the gmap database
for genome_file in "${genome_files[@]}"; do
    genome_name=$(basename "$genome_file" .fa)
    if [ ! -f "gmap_db/${genome_name}/${genome_name}.chromosome" ]; then
        gmap_build -D gmap_db/ -d "${genome_name}" "data/${genome_name}.fa"
    fi
done

### In order to create the kmer index, we have had memmory issues in the past with java
### Ensure that there is enough memory
### In the past, 200gb where not enough, so its enough with 300gb
### Check how much memory is available

if [[ "$JAVA_OPTS" != *"-Xmx300g"* ]]; then
    export JAVA_OPTS="-Xmx300g"
fi

echo "Java memory set to:"
echo $JAVA_OPTS

if [ ! -f output/kmerIndex.txt ]; then
    phg build-kmer-index --db-path vcf_dbs/ --index-file output/kmerIndex.txt --hvcf-dir vcf_dbs/hvcf_files/ --use-big-discard-set
fi


### Preparing kmer mapping in BETA
if [ ! -f output/ropeBWT_index.fmd ]; then
    phg rope-bwt-index --hvcf-dir vcf_dbs/hvcf_files/ --db-path vcf_dbs/ --output-dir output/ --index-file-prefix ropeBWT_index --threads 32
fi

#######
#######
# If you want to align to the pangenome using barleymap, is necessary to have a bed file of each genome haplotypes:
#######
#######

# Create, if not exists, the python script that process the hvcf files into bed files

if [ ! -f hvcf2bed.py ]; then
    echo "Creating hvcf2bed.py script"

    hvcf2bed_script="hvcf2bed.py"

    cat << 'EOF' > "$hvcf2bed_script"
import gzip
import subprocess
import sys

if len(sys.argv) != 3:
    print("Usage: python hvcf2bed.py /path/to/folder/ SampleName")
    sys.exit(1)

hvcf_folder = sys.argv[1]
sample_name = sys.argv[2]

hvcf_file = f"{hvcf_folder}{sample_name}.h.vcf.gz"
bed_file = f"{hvcf_folder}{sample_name}.bed"
sorted_bed_file = f"{hvcf_folder}{sample_name}.h.bed"

# Create the BED file
with gzip.open(hvcf_file, "rt") as f, open(bed_file, "w") as out:
    for line in f:
        if line.startswith("##ALT"):
            line = line.rstrip().split(",")
            ID = line[0].split("=")[2]
            variety = line[3].split("=")
            region = line[4]
            chrom = region.split(":")[0].split("=")[1]
            # if chrom starts with ", it's kind of bugged, remove it
            if chrom.startswith("\""):
                chrom = chrom[1:]
            start = int(region.split(":")[1].split("-")[0])
            end = int(region.split(":")[1].split("-")[1])
            if start > end:
                start, end = end, start
            out.write(f"{chrom}\t{start}\t{end}\t{ID}\t{variety[1]}\n")

# Sort the BED file by chromosome and start position
subprocess.run(["sort", "-k1,1", "-k2,2n", bed_file, "-o", sorted_bed_file])

print(f"Sorted BED file: {sorted_bed_file}")
# Remove the unsorted BED file
subprocess.run(["rm", bed_file])
EOF
fi

# Create the bed files for each genome
for genome_file in "${genome_files[@]}"; do
    genome_name=$(basename "$genome_file" .fa)
    if [ ! -f "vcf_dbs/hvcf_files/${genome_name}.h.bed" ]; then
        echo "Creating bed file for $genome_name"
        python3 hvcf2bed.py vcf_dbs/hvcf_files/ "$genome_name"
    fi
done

# Index the fasta files
for genome_file in "${genome_files[@]}"; do
    genome_name=$(basename "$genome_file" .fa)
    if [ ! -f "data/${genome_name}.fa.fai" ]; then
        echo "Indexing fasta file for $genome_name"
        samtools faidx "data/${genome_name}.fa"
    fi
done
