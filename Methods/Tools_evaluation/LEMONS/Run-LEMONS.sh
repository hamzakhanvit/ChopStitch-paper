#!/bin/sh
usage() { printf "Usage: $0 [-f <transcriptome assembly file>]\n" 1>&2; exit 1; }

while getopts ":f:" o; do
    case "${o}" in
        f)
            f=${OPTARG}
            ;;

        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${f}" ]; then
    usage
fi

echo "Path to Transcriptome assembly file = ${f}"



/usr/bin/time -v python LEMONS.py  --in $f --evalue 1e-05 --db "2_D.rerio,1_H.sapiens,4_G.gallus,6_X.tropicalis,D.melanogaster,A.thaliana,5_A.carolinensis,3_M.musculus,C.elegans"

