usage() { printf "Usage: $0 [-p <Path to output directory>] [-t <Number of threads>] [-f <FASTQ1 FASTQ2>]\n" 1>&2; exit 1; }

while getopts ":f:p:t:" o; do
    case "${o}" in
        f)
            f=${OPTARG}
            ;;
        p)
            p=${OPTARG}
            ;;
	t)
            t=${OPTARG}
            ;;

        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${f}" ] || [ -z "${p}" ]; then
    usage
fi

echo "Path to FASTQ files = ${f}"
echo "Path to Output directory = ${p}"

my_outdir=$p
THREADS=$t

transabyss --pe $f  -k 25 --name k25 --outdir ${my_outdir}/k25 --threads $THREADS

transabyss --pe $f  -k 35 --name k35 --outdir ${my_outdir}/k35 --threads $THREADS

transabyss --pe $f  -k 45 --name k45 --outdir ${my_outdir}/k45 --threads $THREADS

transabyss-merge ${my_outdir}/k25/k25-final.fa ${my_outdir}/k35/k35-final.fa ${my_outdir}/k45/k45-final.fa --mink 25 --maxk 45 --prefixes k25 k35 k45 --SS --out
${my_outdir}/k25_35_45_merged.fa --threads $THREADS

#Extract sequences with more than 100 bases - 
cat ${my_outdir}/k25_35_45_merged.fa| awk '{y= i++ % 2 ; L[y]=$0; if(y==1 && length(L[1])>=100) {printf("%s\n%s\n",L[0],L[1]);}} > ${my_outdir}/k25_25_45_merged_100+.fa
