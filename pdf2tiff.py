import os
from PIL import Image
from os.path import basename
import subprocess
import time
import os


def convert_pdf_tiff(base_dir,dpi=300):
	for root,dirs,files in os.walk(base_dir):
		for fil in files:
			if fil.endswith(".pdf"):
				base = fil.split(".")[0]
				dest_path = os.path.join(root,(base+".tiff"))
				print(dest_path)
				clone_dest_path = os.path.join(root,(base+".tif"))
				#print("Size before conversion--- {}KB".format(os.path.getsize(os.path.join(root,fil))/1024))
				command = 'convert -density {} {} {}'.format(dpi,os.path.join(root,fil),os.path.join(root,dest_path))
				print("\nConverted Document============{}".format(fil))				
				if os.path.exists(os.path.join(root,dest_path)) or os.path.exists(os.path.join(root,clone_dest_path)):
					print("{} already exists.Moving to next file conversion".format(dest_path))
					print("\n")
					time.sleep(2)

				else:
					output = subprocess.check_call(command,shell=True)
					print(output)
					if output is None:
						raise Exception('Imagemagick Error')
					#print("Size After conversion--- {}MB".format(os.path.getsize(os.path.join(root,dest_path))*0.00000095367432))


def remove_tiff(base_dir):
	for root,dirs,files in os.walk(base_dir):
		for fil in files:
			if fil.endswith(".tiff"):
				#if not 'comp' in basename(fil):					
				os.remove(os.path.join(root,fil))
				time.sleep(2)
				#print("Removed {}".format(fil))

def lossless_compress(imagefile,dest_path):
	import os
	from PIL import Image, TiffTags
	TiffTags.LIBTIFF_CORE.add(317)
	img = Image.open(imagefile)
	img.save(dest_path, compression='tiff_lzw', tiffinfo={317: 2})


def main(base_dir):
	convert_pdf_tiff(base_dir)	
	for root,dirs,files in os.walk(base_dir):
		for fil in files:
			if fil.endswith(".tiff"):
				imagefile = os.path.join(root,fil)
				base = fil.split(".")[0]
				dest_path = os.path.join(root,(base+".tif"))				
				lossless_compress(imagefile,dest_path)

	print("\n")
	print("Conversion of documents from pdf to tiff completed")
	print("===================================================")			
	remove_tiff(base_dir)				


if __name__ == '__main__':
	base_dir = r"C:\Work\Barclays\PPI\pdfs\Hotel"	
	main(base_dir)	


