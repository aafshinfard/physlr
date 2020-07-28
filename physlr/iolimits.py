import sys
import re
import argparse
import gzip

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Interleave and barcode TELL-seq read files (R1/R2/I1)')
	parser.add_argument("input_r1", help='Input file containing R1 reads without barcode (gzipped)', type=str)
	parser.add_argument("input_i1", help='Input file (I1) containing barcodes (gzipped)', type=str)
	parser.add_argument("output_prefix", help='Prefix of the output file', type=str)
	args = parser.parse_args()
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
      			r1_header = str.encode(r1_buff[i].decode("ascii").split(" ")[0])
			next(i1_file)
    		if cnt==2:
      			r1_seq = r1_line
			i1_seq = next(i1_file)
    		if cnt==3:
      			r1_orient = r1_line
			next(i1_file)
    		if cnt==4:
      			r1_qual = r1_line
			next(i1_file)
			out_4line = r1_header + b'_' + i1_seq + r1_seq + r1_orient + r1_qual
			out_file_R1.write(out_byte)
		cnt += 1
	i1_file.close()
	out_file_R1.close()
