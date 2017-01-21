#!/bin/bash
usage() { printf "Usage: $0 [-s <Splice subgraph> -r <Caenorhabditis_elegans.WBcel235.cdna.all.fa>]\n" 1>&2; exit 1; }

while getopts ":s:r:" x; do
	case "${x}" in
	s)
            s=${OPTARG}
            ;;
        r) 
            r=${OPTARG}
            ;;

	*)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${s}" ] || [ -z "${r}" ]; then
    usage
fi

grep ">" $r > headers
awk {'print $1"\t"$4'} headers > transcript_gene_pairs
rm headers
    
#Remove the first line from splice_subgraph and the first character of the second line (which is a tab)
sed -i '1d' $s 
sed -i '1s/^.//' $s

#Remove the \ in splice_subgrph, then \n and \t through
sed -i -e 's/\\//g' $s
tr -d ' \t\n\r\f' < $s >splicegraph_formatted

#Also remove " from file using -
sed -i -e "s/\"//g" splicegraph_formatted

