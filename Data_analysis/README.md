# Calculate genomic distance between varieties in a VCF file.
### You can also plot it in a heat map, clustering your samples.

Take as input a VCF file with several varieties of a population and compair all against eacho other. Recomended to prepair files with [Data_Trimmering](https://github.com/jsarriaa/VCF_Manager/tree/main/Data_Trimmering).

Generate a distance matrix compairing all SNPs available in each varieties pairs from a VCF file. The output files are a matrix of distance, in which "1" means identity, and a support matrix of counts, in which the number of SNPs in common between two varieties is shown. Both as tsv (/tab separated values). 
By default, the matrix is build using all the varieties present in the VCF file. If you want to select a subset of varieties, you can use the option --interestlist or --interestfile. If no output file is specified, it will be saved working directory and named as "distance_matrix.tsv" and "count_matrix.tsv". 
There is also the option to plot and save the results as a heatmap.


## HOW TO

### Execute
Run at terminal with python (v 3.11.7)
You must provide your VCF as argument:

`python /path/VCF_Distance_V1.py </path/yourVCFfile.vcf.gz>`

_Note: Your VCF file must be compressed (gz)_
---
### Options
---
**-h, --help**

Shows up the help message and closes the script

`python /path/VCF_Distance_V1.py --help`

---
**-od, --out-distance-matrix**

Edit path and name of distance matrix output

`python /path/VCF_Distance_V1.py -od <distancematrixname.tsv>`

---
**-oc, --out-count-matrix**

Edit path and name of count matrix output

`python /path/VCF_Distance_V1.py -oc <countmatrixname.tsv>`

---
**-list, --interestlist**

Select only a list of samples to include at the distance matrix. Separe varieties with comma.

`python /path/VCF_Distance_V1.py -list <variety1,variety2,variety3...>`

---
**-file-list, --interestfile**

A _.txt_ file containing the list of varieties to select and include into the distance matrix from the VCF.
Set the file having one name each line:

_interest_list.txt_

>variety1

>variety2

>variety3

`python /path/VCF_Distance_V1.py -file-list <interest_list.txt>`

---
**-p, --plot**

Plot the distance matrix in a heatmap distributed by a hirarchical dendrogram. If an output path is not provided, by default a distance_heatmap.pdf will be generated at working directory.

`python /path/VCF_Distance_V1.py -p`

`python /path/VCF_Distance_V1.py -p <distance_heatmap_NAME.pdf>`

a `distance_tree.txt` will be also saved, in a [Newick tree](https://en.wikipedia.org/wiki/Newick_format) format. 
To avoid the generation of this file, just add the ´--ignore-tree´ / ´-notree´ arguments:

`python /path/VCF_Distance_V1.py -p <distance_heatmap_NAME.pdf> -notree`


---
**-ct, --color-threshold**

If _--plot__ option is up, you can change the threshold to color the different clusters of hierarchical dendrogram. Values between 0 and 1 (e.g. 0.55). If it is not modified by default is 0.45.

`python /path/VCF_Distance_V1.py -p <distance_heatmap_NAME.pdf> ct 0.75`

`python /path/VCF_Distance_V1.py -p <heatmap_distance.pdf> -ct 0.55`
