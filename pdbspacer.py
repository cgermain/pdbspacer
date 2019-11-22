import os
import sys
import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument('pdb_dir', action="store", help="Path to the dir that holds PDBQT files")

file_extension = ".pdbqt"			# File extension we are looking to modify
column_location = 46				# Column name minus one to account for zero indexing
output_directory_name = "spaced"	# Output directory will be named this and located inside input dir
line_prefix = "HETATM"				# Lines that start with this are ones that we would like to modify

def make_output_filename(filename):
	#Disassemble each piece of the filename
	path = os.path.abspath(filename)
	directory = os.path.split(path)[0]
	full_filename = os.path.split(path)[1]
	base = os.path.splitext(full_filename)[0]
	extension = os.path.splitext(full_filename)[1]
	out_dir = os.path.join(directory, output_directory_name)
	
	# If this is the first time we are assembling a filename
	# to write to, create the output dir
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	return os.path.join(out_dir, base + file_extension)

def main():
	arguments = parser.parse_args()
	pdb_dir = arguments.pdb_dir

	if not os.path.isdir(pdb_dir):
		print("Command line argument needs to be a directory, not a file.")
		return

	# Create a list of all of the files in the specified dir
	# that end with the file extension we are looking to modify
	pdb_files = [f for f in os.listdir(pdb_dir) \
				if os.path.isfile(os.path.join(pdb_dir, f)) \
				and f.endswith(file_extension)]

	if len(pdb_files) == 0:
		print("Directory doesn't contain any files that match our criteria.")
		return

	# For each of the files we are looking to modify
	for pdb_file in pdb_files:
		full_path = os.path.join(pdb_dir,pdb_file)
		# Open that file to read
		with open(full_path, 'r') as current_file:
			# Determine the filename to write out and open that file for writing
			output_filename = make_output_filename(full_path)	
			out_file = open(output_filename,'w+')
			# For each line of the file we are reading
			# if we determine its one that we want to edit
			# add a space at the column that is specified
			# and write the file out
			for line in current_file:
				if line.startswith(line_prefix):
					line = line[:column_location] + " " + line[column_location:]
				out_file.write(line)
			# Close the file that we have completed writing out the modified lines to
			out_file.close()
		# Close the current input file that we are reading from
		current_file.close()

if __name__ == "__main__":
	main()