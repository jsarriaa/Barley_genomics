# %%
import re   # Import regular expressions
import subprocess
import argparse
import os
import gzip

# %%
#Aqui ira el agparse para meter argumentos por consola
parser = argparse.ArgumentParser(description="""Generate a distance matrix compairing all SNPs available in each varieties pairs from a VCF file. 
\n The output files are a matrix of distance, in which "1" means identity, 
and a matrix of counts, in which the number of SNPs in common between two varieties is shown. Both as tsv (/tab separated values).
\nBy default, the matrix is build using all the varieties present in the VCF file. If you want to select a subset of varieties, you can use the option --interestlist or --interestfile. \n
If no output file is specified, it will be saved working directory and named as "distance_matrix.tsv" and "count_matrix.tsv".
\n there is also the option to plot and save the results as a heatmap.""")
# Add the arguments
parser.add_argument('VCFfile', type=str, nargs='?', default='Empty', help='The input VCF file path. It must be a compresed vcf.gz file', metavar='<input.vcf.gz>')
parser.add_argument('--out-distance-matrix', '-od', type=str, required=False, help='The output distance matrix file path', metavar='<distance_matrix.tsv>')
parser.add_argument('--out-count-matrix', '-oc', type=str, required=False, help='The output count matrix file path', metavar='<count_matrix.tsv>')
parser.add_argument('--interestlist', '-list', type=str, required=False, help='The input list of varieties to select inside the VCF file. Separe them with COMMA', metavar='<variety1,variety2,...>')
parser.add_argument('--interestfile', '-file-list', type=str, required=False, help='A .txt file containing the list of varieties to select inside the VCF file. Each line belong to each variety name', metavar="<list.txt>")
parser.add_argument('--plot', '-p', nargs='?', const='default', default='Empty', type=str, required=False, help='Plot the distance matrix in a heatmap distributed by a hierarchical dendrogram. If not an output path is provided, by default a distance_heatmap.pdf will be generated at executing folder', metavar='<output.pdf>')
parser.add_argument('--color-threshold', '-ct', type=float, required=False, default=0.45, help='The color threshold for the heatmap. The default is 0.45', metavar='<0-1    e.g. -ct 0.55>')

# Parse the arguments
args = parser.parse_args()

# %%
# Indico los documentos, de entrada, y las dos matrices de salida

#Primero, queja de que no se ha introducido ningun archivo
if args.VCFfile == 'Empty':
    raise FileNotFoundError("You must introduce a VCF file to proceed. Please, try again.")
else:
    VCFfile = args.VCFfile


#Segundo, comprueba que el archivo existe y es un archivo vcf.gz
if not os.path.exists(VCFfile):
    raise FileNotFoundError("The file introduced does not exist. Please, try again.")

if args.out_distance_matrix:
    distfile = args.out_distance_matrix
else:
    distfile = "distance_matrix.tsv"

if args.out_count_matrix:
    countfile = args.out_count_matrix
else:
    countfile = "count_matrix.tsv"

# %%
#By default, the script will use all varieties at the VCF file to calculate the distance matrix

VCFcolumns = {}  # Initialize an empty dictionary to hold the output

with gzip.open(VCFfile, 'rt') as file:  # Open the gzipped file
    for line in file:
        if line.startswith('#CHROM\t'):
            fields = line.split()
            VCFcolumns = {field: i for i, field in enumerate(fields, start=1)}  # Swap keys and values
            VCFcolumns = dict(list(VCFcolumns.items())[9:])
            #print(VCFcolumns) #just to check if it is working
            break    

if args.interestlist:
#go and search in VCFcolumns for the columns of the varieties of interest
    interestlist = args.interestlist.split(',')
#only pick columns from VCFcolumns that are in the interestlist
    VCFcolumns = {key: value for key, value in VCFcolumns.items() if key in interestlist}
    #print(VCFcolumns) #just to check if it is working

    
if args.interestfile:
    interestfile = args.interestfile
    with open(interestfile, 'r') as f:
        interestlist = f.read().splitlines()
        VCFcolumns = {key: value for key, value in VCFcolumns.items() if key in interestlist}
        #print(VCFcolumns) #just to check if it is working

# %%
#Mensaje de que metodo estas empleando para describir las variedades

if args.interestlist or args.interestfile:
    
    print("\nYou are providing a list of varieties to select from the VCF file")
    print("The varieties to process are:\n")
    for key in VCFcolumns.keys():
        print(key)

else:
    print("\nYou are using all the varieties present in the VCF file (default)")
    print("The varieties to process are:\n")
    for key in VCFcolumns.keys():
        print(key)



# %%
# create output TSV files (handle TSV)
try:
    distmat = open(distfile, 'w')
    countmat = open(countfile, 'w')
except IOError as e:
    print(f"Error: {e}")
    exit()

# %%
# Creo la lista de keys para que esté ordenada
barleys = sorted(VCFcolumns.keys()) 
#print(barleys)

# %%
#Si queremos extraer la lista sorted con el orden que va a seguir la matriz
#print(barleys)

print("\nDistance matrix results preview:\n")

# %%
b1 = None
b2 = None
cmd = None
gt1 = None
gt2 = None
toteq =  {}
totneq = {}

# %%
for b1 in barleys:
    distmat.write(str(b1))
    countmat.write(str(b1))
    print("\t", b1)
    distmat.flush() #actualiza los files y va imprimiendo
    countmat.flush()

    for b2 in barleys:
        if b1 not in toteq:
            toteq[b1] = {}
        if b2 not in toteq:
            toteq[b2] = {}
        if b1 not in totneq:
            totneq[b1] = {}
        if b2 not in totneq:
            totneq[b2] = {}

        if b1 == b2:
            distmat.write("\t0.0000")  # distance
            countmat.write("\tNA")  # SNPs contados
            print("\t0.0000")
            distmat.flush()
            countmat.flush()
        else:
            # Re-use previously computed dist & count
            if b1 in toteq and b2 in toteq[b1]:
                eq = toteq[b1][b2]
                neq = totneq[b1][b2]
                distmat.write(f"\t{1 - (eq / (eq + neq)):.4f}")  # distancia
                countmat.write(f"\t{eq + neq}")  # snp count
                print(f"\t{1 - (eq / (eq + neq)):.4f}")  # 
                distmat.flush()
                countmat.flush()
                continue    
            elif b2 in toteq and b1 in toteq[b2]:
                eq = toteq[b2][b1]
                neq = totneq[b2][b1]
                distmat.write(f"\t{1 - (eq / (eq + neq)):.4f}")  # distancia
                countmat.write(f"\t{eq + neq}")  # snp count
                print(f"\t{1 - (eq / (eq + neq)):.4f}")  # 
                distmat.flush()
                countmat.flush()
                continue

            else:

                # print(VCFcolumns[b1])
                # print(VCFcolumns[b2]) #esto es solo para asegurarnos que esta asociando bien el loop

                #Ahora si restauramos los valores a 0
                eq = 0
                neq = 0

                # preparamos el comando que va a seleccionar las dos entradas a comparar que corresponden.
                cmd = f"zcat {VCFfile} | cut -f {VCFcolumns[b1]},{VCFcolumns[b2]}"
                # ejecutamos el comando, guardamos el output sin generar fichero, y lo leemos, linea a linea
                try:
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
                    for line in process.stdout:
                        if "./." in line or re.match(r"\d\|\d:", line):  # Saltamos missing/imputados
                            continue
                        match = re.match(r"(\S[\/|\|]\S).*?\t(\S[\/|\|]\S)", line)
                        if match:
                            gt1, gt2 = match.groups()

                            # Saltamos heterocigotos
                            if gt1 is not None and gt2 is not None:
                                match_gt1 = re.match(r"(\d+)\/(\d+)", gt1)
                                match_gt2 = re.match(r"(\d+)\/(\d+)", gt2)
                                if match_gt1 and match_gt2:
                                    if match_gt1.group(1) != match_gt1.group(2) or match_gt2.group(1) != match_gt2.group(2):
                                        continue
                            #nos aseguramos que esta haciendo bien la criba de het.
                            #print(match_gt1)            
                            #print(gt1, gt2)

                            # Sumamos el match // missmatch
                            if gt1 == gt2:
                                eq += 1
                            else:
                                neq += 1
                            #Check del valor de eq y neq
                            #print (eq, neq)

                except subprocess.CalledProcessError:
                    print("# ERROR: cannot parse zcat", cmd)
                    exit("exit")

                
                toteq[b1][b2] = eq
                toteq[b2][b1] = eq
                totneq[b1][b2] = neq
                totneq[b2][b1] = neq

                #Aviso de que algo no ha ido bien
                if eq + neq == 0:
                    print("# WARN: not enough snps to count\n")
                    
                else:
                    distmat.write(f"\t{1 - (eq / (eq + neq)):.4f}")  # distancia
                    countmat.write(f"\t{eq + neq}")  # snp count
                    print(f"\t{1 - (eq / (eq + neq)):.4f}")  # 
                    distmat.flush()
                    countmat.flush()

    distmat.write("\n")
    countmat.write("\n")
    print("\n")

# %%
distmat.close()
countmat.close()

print(f"all done! check your files {distfile} and {countfile}\n")

# %% [markdown]
# #From here comes the plotting part of the script, only executed if --plot / -p are indicated

# %%
#!pip install pandas
#!pip install seaborn
#!pip install matplotlib
#!pip install scipy
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import warnings



# %%
if args.plot:
    if args.plot == 'default':
        plotfile = "distance_heatmat.pdf"
    else:
        plotfile = args.plot
#print(args.plot) #check if it is working

# %%
#Associating the previous distance matrix to pandas dataframe. If you just want to plot an existing matrix, and you want to skip the previous steps,
# please, use the following code substituting the distance_matrix by your tsv existring file.

if distfile is not None:
    distance_matrix = pd.read_csv(distfile, sep="\t", index_col=0, header=None)
else:
    print('Error: No distance matrix file is provided, something is wrong at code. Please, check it.')
    # Handle the case where args.out_distance_matrix is None

# %%
if args.plot:

    print("\nYou have call the plot function, so here we go. Leave me some time, im cooking your images...\n")

    # Extract the first element of each row to use as column names
    column_names = [row[0] for row in distance_matrix.iterrows()]

    with PdfPages(plotfile) as pdf:         #Save both plots in a single pdf file

        # Hierarchical clustering
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            linkage = hierarchy.linkage(distance_matrix, method='average')



        # Create a new figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 16))

        # Plot the dendrogram on the first subplot
        if args.color_threshold:
            dendrogram = hierarchy.dendrogram(linkage, labels=column_names, leaf_rotation=90, leaf_font_size=8, color_threshold=args.color_threshold, ax=ax1)
        else:
            dendrogram = hierarchy.dendrogram(linkage, labels=column_names, leaf_rotation=90, leaf_font_size=8, color_threshold=0.45, ax=ax1)
        ax1.set_title("Hierarchical clustering dendrogram")
        ax1.set_ylabel("Distance    k")

        #adjust the size of the figure
        plt.subplots_adjust(hspace=0.5, left=0.2)

        from scipy.cluster.hierarchy import leaves_list
        leaves_order = leaves_list(linkage) #saving the order of the leaves for further graphs

        # print(dendrogram['leaves']) #just code to check checkpoint
        # print(distance_matrix) #just code to check checkpoint


        # Plot the heatmap on the second subplot
        sns.heatmap(distance_matrix.iloc[dendrogram['leaves'], dendrogram['leaves']], cmap="coolwarm", annot=False, fmt=".2f", linewidths=.5, xticklabels=True)
        ax2.set_title("Heatmap distance matrix")
        ax2.set_xlabel(" ")
        ax2.set_ylabel(" ")
        ax2.set_xticks(ticks=range(len(dendrogram['leaves'])))
        ax2.set_xticklabels(labels=[barleys[i] for i in dendrogram['leaves']], rotation=90)
        ax2.set_yticks(ticks=range(len(dendrogram['leaves'])))
        ax2.set_yticklabels(labels=[barleys[i] for i in dendrogram['leaves']], rotation=0)
        plt.subplots_adjust(bottom=0.2, right=0.9)
        # Save the figure to the PDF
        pdf.savefig()
        plt.clf()  # Clear the figure after saving it to the PDF

    print(f"all done! check your file {plotfile}\n")

