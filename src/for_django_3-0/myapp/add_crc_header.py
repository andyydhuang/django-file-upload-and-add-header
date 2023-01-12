#!/usr/bin/env python

import argparse
from argparse import RawTextHelpFormatter
from modules.bitstream import Bitstream
import pathlib

#big endian
#def int_to_bytes(val, num_bytes):
#    return bytearray([(val & (0xff << pos*8)) >> pos*8 for pos in reversed(range(num_bytes))])
#little
def int_to_bytes(val, num_bytes):
    return bytearray([(val & (0xff << pos*8)) >> pos*8 for pos in range(num_bytes)])

def get_file_checksum(in_filename, minus=0):
	try:
		in_file = open(in_filename, 'rb')
	except IOError as e:
	    print ("File I/O error({0}): {1}".format(e.errno, e.strerror))
	    raise

	bits_stream = Bitstream()
	bits_stream.initialize()
	bits_stream.read(in_file)

	crc = 0
	array = bits_stream.get_raw_byte_array()
	for i in range(0, bits_stream.size() - minus, 2):
		val = array[i+1]<<8 | array[i]
		crc = (crc + val) & 0xFFFF
		#print "{:04x}: val={:02x} crc={:04x}".format(i, val, crc) 
		#print "{:04x}: {:02x} {:02x}".format(i, array[i], array[i+1])
		#if i > 32:
		#	print 'PAUSE'
		#	break

	print ("CRC16: {:04x}".format(crc))
	return crc


parser = argparse.ArgumentParser(description='This tool adds defined header.')
parser.add_argument('major_rev', metavar='major_rev', type=str, 
	        		help='Image major version')
parser.add_argument('minor_rev', metavar='minor_rev', type=str, 
	        		help='Image minor version')
parser.add_argument('file_index', metavar='file_index', type=str,
                                help='File index')
parser.add_argument('--input', type=str, help='Input file name')
parser.add_argument('--output', type=str, help='Output file name')

args = parser.parse_args()


input_file_path = args.input
try:
    print ("input_file_path:" + input_file_path)
    input_file = open(input_file_path, 'rb')
except IOError as e:
    print ("File I/O error({0}): {1}".format(e.errno, e.strerror))
    raise

stream = Bitstream()
stream.initialize()


file_index     = int(args.file_index, 16)

stream.append(int_to_bytes(file_index, 4))

cpld_fw_major_ver = int(args.major_rev, 16)
cpld_fw_minor_ver = int(args.minor_rev, 16)
checksum = get_file_checksum(input_file_path)
cpld_version = cpld_fw_major_ver | (cpld_fw_minor_ver << 8) | (checksum << 16)

stream.append(int_to_bytes(cpld_version, 4))

stream.read(input_file)

added_header_file_path =  args.output
added_header_file = open(added_header_file_path, 'wb')
stream.write(added_header_file)

raw_byte = stream.get_raw_value(0, 8)
print('-----------------')
print (' '.join(format(x, '02x') for x in raw_byte))

added_header_file.close()
print ("Generated " + added_header_file_path)

#hexdump -C -n 64 output_files/xxx
