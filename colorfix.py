import sys
import os
import github
from requests import get

# The script will require an argument to run, either -a or --all or the name of the theme you want to download for the script to run.

g = github.Github("PUT YOUR GITHUB ACCESS TOKEN IN HERE")
repo = g.get_user("elenapan").get_repo("dotfiles") # Here we specify user and repo of the files we want to download
elenas_files = []
filelist = os.listdir('.')
args_for_all = ['-a', '--all']
for i in repo.get_contents(".xfiles"): # Here we list all the files in the repo and put them in a list
	elenas_files.append(i.name)


# This function will move the modified files to the termux folder on an android phone... only tested on my own phone however
def move():
	rescan = os.listdir('.')
	for i in rescan:
		if i.endswith('.properties'):
			os.rename(os.getcwd() + '/' + i, '/data/data/com.termux/files/usr/share/termux-style/colors/' + i)

# This will download the specified files from the repo
def downloader(file):
    if i not in filelist:
        with open(file, 'wb') as outfile:
            response = get('https://raw.githubusercontent.com/elenapan/dotfiles/master/.xfiles/' + file)
            outfile.write(response.content)

# This will convert the files from the current format to termux format.. this will however obviously not work if elena changes the format of her files
def do_the_write(file):
	with open(file,'r') as data, open(file + '-elena.properties','w') as outfile:
		readable = data.read()
		formatted = readable.replace('*', '').replace(' ', '').replace(':', '=').replace('cursorColor', 'cursor').replace('\t','')
		outfile.write(formatted)

# RUN ALL THE THINGS! Checks for arguments either all files or named files, then downloads, converts and moves them.
def main():
	try:
		if sys.argv[1] in args_for_all:
			for i in elenas_files:
				downloader(i)
				do_the_write(i)
			for i in filelist:
				if i in elenas_files:
					do_the_write(i)
			print("All done!")
		elif sys.argv[1] in elenas_files:
				do_the_write(sys.argv[1])
				print("Done! Converted: " + sys.argv[1])
	except:
		print('No arguments specified?')
	move()

if __name__ == '__main__':
    main()
