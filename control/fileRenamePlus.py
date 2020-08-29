#!/usr/bin/python3
#
#	Datei umbenenner
#
import argparse
import os
import sys
import exifread
import PIL
from PIL import Image

 
def getFileDate(fileName):
	# Open image file for reading (binary mode)
	f = open(fileName, 'rb')

	# Return Exif tags
	tags = exifread.process_file(f)
	#print(str(tags['Image Orientation']))
	
	# extract the Date
	try:
		fileDate = str(tags['Image DateTime'])
	except KeyError:
		print ("no Key: Image DateTime")
		return False
	
	# format to the right syntax
	fileDate = fileDate[:10].replace(":","-")

	# close File	
	f.close()

	return fileDate


def getFilelist(path):
	fl = os.listdir(path)
	fl.sort()
	return fl

def rightExt(fn):
	extension = fn[fn.rfind(".") : len(fn)].lower()

	if extension != ".jpg" and extension != ".JPG" and extension != ".MP4" and extension != ".jpeg" and extension != ".HEIC" and extension != ".heic":
		return False
	else:
		return extension

def renameFiles(path, newFilename, dryRun=True, resizeOption=False ):
	
	fileDateOld = ""
	## show values ##

	print ("Pfad: %s" % path )
	print ("Dateiname: %s" % newFilename)

	if os.path.exists( path ):

		# append / if not exist
		if path[-1:] != '/':
			path = path+'/'	
	
		fileList = getFilelist(path)

		i = 1
		for filename in fileList:
			if i < 10:
				count = "0" + str(i)
			else:
				count = str(i)
			
			extension = rightExt(filename)
			if not extension:
				continue
	
			fileDate = getFileDate(path + filename)
			
			if fileDate == False:
				if 'fileDateOld' in locals():
					print("Keine Bilddateien?")
					exit
				if fileDateOld == "":
					fileDate = input("Datum eingegen: ")
				else:
					fileDate = fileDateOld
				
			fileDateOld = fileDate
			fileNameNew = fileDate + "_" + newFilename + count + extension
			
			if not dryRun:
				os.rename(path + filename, path + fileNameNew)

			
			print(filename + " umbenannt in: " + fileNameNew)
			
			i = i + 1
	
			if resizeOption:
				basewidth = int(resizeOption)
				if not dryRun:
					try:
						img = Image.open(path + fileNameNew)
						wpercent = (basewidth/float(img.size[0]))
						hsize = int((float(img.size[1])*float(wpercent)))
						img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
						img.save(path + fileNameNew)
					except (KeyboardInterrupt, SystemExit):
						break
					except:
						print("Fehler beim Bild: " + fileNameNew)
						e = sys.exc_info()[0]
						print("Error: %s" % e )
					print("Bild: " + fileNameNew + " geändert x = " + str(basewidth))
				else:
					img = Image.open(path + filename)
					print( img.size[0])
					print( img.size[1])
					img.close()
					print("Bild: " + fileNameNew + " geändert x = " + str(basewidth))

	else:
		print("Ordner existiert nicht!: " + path)


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='This script rename all files in a folder with the given name and add the date when the photo was taken')
	parser.add_argument('-i','--input', help='Path where the files placed',required=True)
	parser.add_argument('-f','--filename',help='The new filename + datet from exif data',required=True)
	parser.add_argument('-r','--resize', help='Resize the Image with the given width',required=False)
	parser.add_argument('-d','--dry', help='Dry run. Script run but don\'t touch any file' ,required=False, action='store_true')
	parser.add_argument('-k','--keep', help='Keep the old files while resizing ' ,required=False, action='store_true')
	args = parser.parse_args()
	

	renameFiles(path=args.input, newFilename=args.filename, dryRun=args.dry, resizeOption=args.resize )



