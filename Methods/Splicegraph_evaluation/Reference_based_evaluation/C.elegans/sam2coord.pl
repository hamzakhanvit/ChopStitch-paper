#!/usr/bin/env perl

use strict;
use warnings;

use Getopt::Long;
use File::Spec;
use Data::Dumper;

my $script_name = (File::Spec->splitpath($0))[2];
my $usage = <<HEREDOC;
Usage: $script_name [SAM file]...
Extract coordinates from SAM alignments.

Output fields:

	QNAME       query seq ID
	QSTART      start coord of alignment on query seq
	QEND        end coord of alignment on query seq
	QALEN       num bases of query seq in alignment
	QLEN        length of query seq
	RNAME       ref seq ID
	RSTART      start coord of alignment on ref seq
	REND        end coord of alignment on ref seq
	RALEN       num bases of ref seq in alignment
	RLEN        length of ref seq
	EDIT_DIST   edit distance between query and ref seqs

    In the case of unmapped reads, only the first 5 fields
	are printed (fields starting with "Q").
	
	The RLEN field will be zero unless the --rlen option
	is used. The RLEN field is not used by default because
	it requires loading a complete hash of the reference sequence
	lengths into memory (read from the SAM headers).  If
	the --rlen option is used but there are no SAM headers
	in the input, a warning will be printed and the RLEN
	column will be reported as zero.


	The EDIT_DIST field is only printed if the 'NM'
	(edit distance) field is present in the input SAM alignments.
	Unlike the NM field, this script includes soft-clipped and
	hard-clipped bases in the edit distance calculation.

Options:

	--rlen		include ref sequence lengths
    --header    include a header line
    --help      show this help message
HEREDOC

my %options = ();
my $getopt_success = GetOptions(
    \%options,
    '--header',
    '--help',
	'--rlen',
);

if ($options{help}) { print $usage; exit 0; }
die $usage unless $getopt_success;

print join(
    "\t",
    'qname',
    'qstart',
    'qend',
    'qalen',
	'qlen',
    'rname',
    'rstart',
    'rend',
    'ralen',
	'rlen',
	'edit_dist',
) . "\n" if $options{header};

my %rlength = ();

while (<>) {
    my @fields = split /\t/;
	if ($options{rlen} && /^\@SQ\s+SN:(\S+)\s+LN:(\S+)/) {
#		if (exists($rlength{$1})) {
#			die "error: sequence '$1' appears twice in SAM header\n";
#		}
		$rlength{$1} = $2;
	}
    next unless @fields >= 10;
	my $line = $_;
    my $qname = $fields[0];
    my $rname = $fields[2];
    my $rstart = $fields[3];
    my $cigar = $fields[5];
    my $qseq  = $fields[9];

    # Query
    my $qstart = 1;
    $_ = $cigar;
    s/^(\d+)[SH]/$qstart += $1/eg;
    my $qalen = 0;
    $_ = $cigar;
    s/(\d+)[M=XI]/$qalen += $1/eg;
    my $qend = $qstart + $qalen - 1;
    $_ = $cigar;
	my $end_clip_len = 0;
	s/(\d+)[SH]$/$end_clip_len += $1/eg;
	my $qlen = 0;
	if ($qalen > 0) {
		$qlen = ($qstart-1) + $qalen + $end_clip_len;
	} elsif ($qseq ne "*") {
		$qlen = length($qseq);
	}
	
    # Reference
    my $ralen = 0;
    $_ = $cigar;
    s/(\d+)[M=XDN]/$ralen += $1/eg;
    my $rend = $rstart + $ralen - 1;
	my $rlen = 0;
	if ($options{rlen} && exists($rlength{$rname})) {
		$rlen = $rlength{$rname};
	}

	# Calculate edit distance including clipping
	my $edit_dist = '';
	if ($line =~ /NM:i:(\d+)/) {
		$edit_dist = $1 + $qstart - 1 + $end_clip_len;
	}

    if ($rname eq '*') {
        # case: query sequence is unmapped
        print join("\t", $qname, $qstart, $qend, $qalen, $qlen) . "\n";
    } else {
        print join("\t", $qname, $qstart, $qend, $qalen, $qlen, $rname, $rstart, $rend, $ralen, $rlen);
		print "\t$edit_dist" if length($edit_dist) > 0;
		print "\n";

    }
}
