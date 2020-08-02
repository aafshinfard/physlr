import sys
import re
import argparse
import gzip

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Interleave and barcode TELL-seq read files (R1/R2/I1)')
	parser.add_argument("input_r1", help='Input file containing R1 reads without barcode (gzipped)', type=str)
	parser.add_argument("input_i1", help='Input file (I1) containing barcodes (gzipped)', type=str)
	parser.add_argument("input_pair", help='If the input is -1 (R1) or -2 (R2)', type=str)
	parser.add_argument("output_prefix", help='Prefix of the output file', type=str)
	parser.add_argument("input_state", help='Wether the input is raw (1) or TELL-read processed (2) [2]', type=int, default=2)
	args = parser.parse_args()
	
	number = str.encode(args.input_pair, encoding="ascii") + b'\n'
	r1_file_name = args.input_r1
	r1_file = gzip.open(r1_file_name, 'r')
	i1_file_name = args.input_i1
	i1_file = gzip.open(i1_file_name, 'r')
	out_file_prefix = args.output_prefix
	out_file_R1 = gzip.open(out_file_prefix + '_R1_barcoded.fastq.gz', 'wb')
	r1_header = ''
	r1_seq = ''
	r1_orient = ''
	r1_qual = ''
	i1_seq = ''
	cnt = 1	
	
	with gzip.open(r1_file_name, 'r') as r1_file:
		for r1_line in r1_file:
			if cnt==1:
				if args.input_state==1
					r1_header = str.encode(r1_line.decode("ascii").split(" ")[0], encoding="ascii")
				if args.input_state==2
					r1_header = str.encode(r1_line.decode("ascii").split(" ")[0][:-1], encoding="ascii")
				next(i1_file)
			if cnt==2:
				r1_seq = r1_line
				i1_seq = next(i1_file)[:-1]
			if cnt==3:
				r1_orient = r1_line
				next(i1_file)
			if cnt==4:
				r1_qual = r1_line
				next(i1_file)
				out_4line = r1_header + b' BX:Z:' + i1_seq + number + r1_seq + r1_orient + r1_qual
				out_file_R1.write(out_4line)
				cnt = 0
			cnt += 1
	i1_file.close()
	out_file_R1.close()
