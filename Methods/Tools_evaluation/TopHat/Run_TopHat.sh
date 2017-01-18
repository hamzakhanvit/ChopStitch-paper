#!/bin/bash
usage() { printf "Usage: $0 [-r Reference Genome] [-i <Bowtie index filename for Reference genome>] [-g <Reference GTF file>] [-a <RNA-Seq PE FASTQ1>] [-b <RNA-Seq PE FASTQ2>] [-o <output directory>]\n" 1>&2; exit 1; }

while getopts ":r:i:g:a:b:o:" x; do
	case "${x}" in
        r)
            r=${OPTARG}
            ;;
        i)
            i=${OPTARG}
            ;;
        g)
            g=${OPTARG}
            ;;
	a)
            a=${OPTARG}
            ;;
        b)
            b=${OPTARG}
            ;;
        o) 
            o=${OPTARG}
            ;;
	*)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${r}" ] || [-z "${i}"] || [ -z "${g}" ] || [ -z "${a}" ] || [ -z "${b}" ] || [ -z "${o}" ]; then
    usage
fi

reference=$r
reference_index=$i
bowtie-build ${reference} ${reference_index}
transcript_annotation=$g #Example: Homo_sapiens.GRCh38.84.gtf
output=$o
tophat -p 20 -G ${transcript_annotation} -o ${output} ${reference_index} ${a} ${b} 
samtools sort ${output}/accepted_hits.bam ${output}/accepted_hits.sorted
samtools index ${output}/accepted_hits.sorted.bam
