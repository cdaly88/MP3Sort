import os
import shutil
import re
from mutagen.easyid3 import EasyID3

def tagExamine(root, musicfile):
	'''Examine id3 tags via external library Mutagen, specifically EasyID3. Takes the 
	root directory and the name of a music file and returns the filepath and the artist of the file as
	described in the ID3 tag.'''
	artist, filePath = "" , ""
	try:
		filePath = os.path.join(root, musicfile)
		examineFile = EasyID3(filePath)
		artist = (examineFile['artist'][0])
	except:
		pass
	return filePath, artist

def search():
	'''Searches a filepath designated by the user, or the current dir if no path is supplied. Iterates
	through the supplied filepath and calles tagExamine to read id3 tags on any mp3 files it comes across.
	Returns a dictionary of filepath: artistname for those files; files without an artist tag are labeled
	Unknown.'''
	musicDict = {}
	artist, filePath = "" , ""
	searchPathTemp = input("Designate search path, or press enter to search from current directory: ")
	if searchPathTemp == "":
		searchPath = "."
	else:
		searchPath = searchPathTemp	
	for root, dirs, files in os.walk(searchPath, topdown=True):
		for x in files:
			if x.lower().endswith((".mp3")):
				filePath, artist = tagExamine(root, x)
				if artist == "":
					musicDict[filePath] = "Unknown"
				else:
					musicDict[filePath] = artist
	return musicDict


def main():
	musicDict = search()
	destinationPathTemp = input("Designate destination path, or press enter to default to current directory: ")
	while True:
		escapeOption = (input("Warning: running this script will cause your music files to be moved\n"
						"permanently from their original location and may disrupt system process. Continue? Y/N "))
		escapeOption = escapeOption.lower()
		if escapeOption == "y":
			break
		if escapeOption == "n":
			print("Process aborted.")
			quit()
		else:
			print("Please enter Y or N.")
	if destinationPathTemp == "":
		destinationPath = "."
	else:
		destinationPath = destinationPathTemp
	for path, artist in musicDict.items():
		#print(path)
		artistPath = os.path.join(destinationPath, artist)
		if not os.path.exists(artistPath):
			#print(artistPath)
			os.mkdir(artistPath)
			os.rename(path, os.path.join(artistPath, os.path.basename(path)))
		else:
			os.rename(path, os.path.join(artistPath, os.path.basename(path)))

if __name__ == "__main__": main()