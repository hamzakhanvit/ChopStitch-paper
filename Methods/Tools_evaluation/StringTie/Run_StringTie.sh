#!/bin/bash
usage() { printf "Usage: $0 [-a <Run_TopHat.sh output file accepted_hits.bam>]\n" 1>&2; exit 1; }

while getopts ":a:" x; do
	case "${x}" in
	a)
            a=${OPTARG}
            ;;
	*)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${a}" ] ; then
    usage
fi

/usr/bin/time -v stringtie -p 32  $a > stringtie-results



