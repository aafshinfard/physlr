import sys
import re
import argparse
import gzip

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Interleave and barcode TELL-seq read files (R1/R2/I1)')
	#parser.add_argument("input_file", help='Input file with interleaved read pairs (gzipped)', type=str)
	#parser.add_argument("output_prefix", help='Prefix of the output files', type=str)
	#args = parser.parse_args()
	parser.add_argument("input_r1", help='Input file containing R1 reads without barcode (gzipped)', type=str)
	parser.add_argument("input_r2", help='Input file containing R2 reads without barcode (gzipped)', type=str)
	parser.add_argument("input_i1", help='Input file (I1) containing barcodes (gzipped)', type=str)
	parser.add_argument("output_prefix", help='Prefix of the output file', type=str)
	args = parser.parse_args()
	
	#in_file_name = args.input_file
	#in_file = gzip.open(in_file_name, 'r')
	
	r1_file_name = args.input_r1
	r1_file = gzip.open(r1_file_name, 'r')
	r2_file_name = args.input_r2
	r2_file = gzip.open(r2_file_name, 'r')
	i1_file_name = args.input_i1
	i1_file = gzip.open(i1_file_name, 'r')
	
	out_file_prefix = args.output_prefix
	out_file = gzip.open(out_file_prefix + '_barcoded_interleaved.fastq.gz', 'wb')

	r1_header = ''
	r2_header = ''
	i1_header = ''
	r1_seq = ''
	r2_seq = ''
	i1_seq = ''
	r1_orient = ''
	r2_orient = ''
	r1_qual = ''
	r2_qual = ''
	cnt = 1
	read = 1
	overall_cnt = 1

	#for r1_header, r1_seq, r1_orient, r1_qual in read_fasta(r1_file):
	#	for r2_header, r2_seq, r2_orient, r2_qual in read_fasta(r2_file):
	#		for i1_header, i1_seq, _, _ in read_fasta(i1_file):
			
	for r1_line, r2_line, i1_line in zip(r1_file, r2_file, i1_file):
		if cnt == 1:
			r1_header = r1_line.decode("utf-8").split(" ")[1]
			r2_header = r2_line.decode("utf-8").split(" ")[1]
			i1_header = i1_line.decode("utf-8").split(" ")[1]
		elif cnt == 2:
			r1_seq = r1_line
			r2_seq = r2_line
			i1_seq = i1_line
		elif cnt == 3:
			r1_orient = r1_line
			r2_orient = r2_line
		elif cnt == 4:
			r1_qual = r1_line
			r2_qual = r2_line
			if r1_header!=r2_header or r1_header!=i1_header:
				print("Error: Expected consistent read headers among the 3 files, but found inconsistent headers at line: ", overall_cnt, file=sys.stderr)
				print(r1_header,"\n",r2_header,"\n",i1_header)
				sys.exit(1)
			r1_printLine = r1_header + '_' + i1_seq +'/1\n' + r1_seq + '\n' + r1_orient + '\n' + r1_qual + '\n'
			r2_printLine = r2_header + '_' + i1_seq +'/2\n' + r2_seq + '\n' + r2_orient + '\n' + r2_qual + '\n'
			out_file.write(r1_printLine)
			out_file.write(r2_printLine)
			cnt = 0
		cnt += 1
		overall_cnt += 1


	r1_file.close()
	r2_file.close()
	i1_file.close()
	out_file.close()
