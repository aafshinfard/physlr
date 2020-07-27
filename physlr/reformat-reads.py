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
	parser.add_argument("output_mode", help='mode of reformatting reads\n 1:single interleaved \n 2: two files (R1, R2)', type=str)
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
	if args.output_mode=="1":
		out_file_R1R2 = gzip.open(out_file_prefix + '_barcoded_interleaved.fastq.gz', 'wb')
	if args.output_mode=="2":
		out_file_R1 = gzip.open(out_file_prefix + '1_barcoded.fastq.gz', 'wb')
		out_file_R2 = gzip.open(out_file_prefix + '_barcoded.fastq.gz', 'wb')
	
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
			
# 	r1_buff = [next(r1_file) for x in range(buffer_max)]
# 	r2_buff = [next(r2_file) for x in range(buffer_max)]
# 	i1_buff = [next(i1_file) for x in range(buffer_max)]

# r1_file = gzip.open("small_NA12878_R1.fastq.gz.1", 'r')
# r2_file = gzip.open("small_NA12878_R2.fastq.gz.1", 'r')
# i1_file = gzip.open("small_NA12878_I1.fastq.gz.1", 'r')
# output_mode=b'1'
# out_file_R1R2 = gzip.open('bufftest2.fastq.gz', 'wb')
# out_file_R1 = gzip.open('bufftestR1.fastq.gz', 'wb')
# out_file_R2 = gzip.open('bufftestR2.fastq.gz', 'wb')

	buffer_cnt = 1
	buffer_max = 4 * 1000

# 	while True:
# 		r1_buff = []
# 		for r1_line in r1_file:
# 			r1_buff.append(r1_line)
# 			buffer_cnt += 1
# 			if buffer_cnt == buffer_max + 1:
# 				buffer_cnt=1
# 				break
# 		for i in range(len(r1_buff)):
# 			print(r1_buff[i])
# 		print("\n and: \n")
# 		if r1_buff == []:
# 			break

	while True:
		r1_buff = []
		r2_buff = []
		i1_buff = []
		r1r2_out_buff = b''
		r1_out_buff = b''
		r2_out_buff = b''
		for r1_line in r1_file:
			r1_buff.append(r1_line)
			buffer_cnt += 1
			if buffer_cnt == buffer_max + 1:
				buffer_cnt = 1
				break
		for r2_line in r2_file:
			r2_buff.append(r2_line)
			buffer_cnt += 1
			if buffer_cnt == buffer_max + 1:
				buffer_cnt = 1
				break
		for i1_line in i1_file:
			i1_buff.append(i1_line)
			buffer_cnt += 1
			if buffer_cnt == buffer_max + 1:
				buffer_cnt = 1
				break
		print(" Read ", len(r1_buff) ," more lines", file=sys.stderr)
		if r1_buff == []:
			break
		cnt = 1
		for i in range(len(r1_buff)):
			if cnt == 1:
				r1_header = str.encode(r1_buff[i].decode("ascii").split(" ")[0])
				r2_header = str.encode(r2_buff[i].decode("ascii").split(" ")[0])
				i1_header = str.encode(i1_buff[i].decode("ascii").split(" ")[0])
			elif cnt == 2:
				r1_seq = r1_buff[i]
				r2_seq = r2_buff[i]
				i1_seq = i1_buff[i]
			elif cnt == 3:
				r1_orient = r1_buff[i]
				r2_orient = r2_buff[i]
			elif cnt == 4:
				cnt = 0
				r1_qual = r1_buff[i]
				r2_qual = r2_buff[i]
				if args.output_mode=="1":
					r1r2_out_buff += r1_header + b'_' + i1_seq + r1_seq + r1_orient + r1_qual
					r1r2_out_buff += r2_header + b'_' + i1_seq + r2_seq + r2_orient + r2_qual
				if args.output_mode=="2":
					r1_out_buff += r1_header + b'_' + i1_seq + r1_seq + r1_orient + r1_qual
					r2_out_buff += r2_header + b'_' + i1_seq + r2_seq + r2_orient + r2_qual
			cnt += 1
		if args.output_mode=="1":
			out_file_R1R2.write(r1r2_out_buff)
			print(" Wrote ", len(r1r2_out_buff) ," more lines", file=sys.stderr)
		if args.output_mode=="2":
			out_file_R1.write(r1_out_buff)
			out_file_R2.write(r2_out_buff)
			print(" Wrote ", len(r1_out_buff)+len(r2_out_buff) ," more lines", file=sys.stderr)
	
	r1_file.close()
	r2_file.close()
	i1_file.close()
	if args.output_mode=="1":
		out_file_R1R2.close()
	if args.output_mode=="2":
		out_file_R1.close()
		out_file_R2.close()
