from tinytag import TinyTag
import os, sys, shutil, subprocess

################## Define some useful stuff

def swq(astring):
	return "\"" + str(astring) + "\""

songs = []
baseMusicPath = "./Music/"
pk3MusicPath = "./Jukebox/music/"
acsScriptPath = "./Jukebox/source/"
acsOutPath = "./Jukebox/acs/"

pk3Name = "EZDoomJukebox.pk3"

songArray = "str songNames["
songRNArray = "str songRealNames["
durationArray = "int durations["

arrayJoin = 	"] = {"
arrayFin = 		"};"

templateSongArray = "<<MUSICSTRINGS>>"
templateNameArray = "<<MUSICNAMES>>"
templateDurationArray = "<<MUSICLENGTHS>>"
templateSongNumber = "<<NUMTRACKS>>"

#Ensure we actually have the destinations available
os.makedirs(pk3MusicPath, exist_ok=True)
os.makedirs(acsScriptPath, exist_ok=True)
os.makedirs(acsOutPath, exist_ok=True)

#get new pk3 name
newPk3Name = input("Enter name for output pk3 (default EZDoomJukebox.pk3): ")
if(not newPk3Name == ""):
	if(not newPk3Name.endswith(".pk3")):
		newPk3Name = newPk3Name + ".pk3"
	pk3Name = newPk3Name

################## Find the songs we're gonna use

for(_, _, filenames) in os.walk(baseMusicPath):
	for fn in filenames:
		if(fn.endswith(".txt")):
			os.remove(baseMusicPath + fn)
			continue
		try:
			tag = TinyTag.get(baseMusicPath + fn)
			title = tag.title
			if(title == None):
				title = os.path.splitext(fn)[0]
			artist = tag.artist
			if(not artist == None):
				artist = artist + " - "
			else:
				artist = ""
			songs.append([fn, tag.duration, artist+title]) #use filename as song name (for now)
		except Exception as e:
			print("Skipping " + fn + "\nReason: " + str(e))
			continue

songArray = songArray + str(len(songs)) + arrayJoin
songRNArray = songRNArray + str(len(songs)) + arrayJoin
durationArray = durationArray + str(len(songs)) + arrayJoin

################## Copy them into the right directory and create arrays

if(len(songs) == 0):
	print("Add some music, that's what you got this for right?")
	input()
	sys.exit(-1)

for i in range(len(songs)):
	print("Copying from " + baseMusicPath + songs[i][0] + " to " + pk3MusicPath + songs[i][0]) #don't actually do it yet
	shutil.copyfile(baseMusicPath + songs[i][0], pk3MusicPath + songs[i][0])
	songArray = songArray + swq("music/" + songs[i][0])
	songRNArray = songRNArray + swq(songs[i][2])
	durationArray = durationArray + str(int(songs[i][1])+1)
	if(i < len(songs)-1):
		songArray = songArray + ", "
		songRNArray = songRNArray + ", "
		durationArray = durationArray + ", "
songArray = songArray + arrayFin
songRNArray = songRNArray + arrayFin
durationArray = durationArray + arrayFin

print(songArray)
print(songRNArray)
print(durationArray)

################## Now we do the fun part, using the template

template = open("./Jukebox/templates/NEDM.txt", 'r')
acs = open("./Jukebox/source/NEDM.acs", 'w')
for line in template:
	if(templateSongArray in line):
		line = line.replace(templateSongArray, songArray)
	elif(templateNameArray in line):
		line = line.replace(templateNameArray, songRNArray)
	elif (templateDurationArray in line):
		line = line.replace(templateDurationArray, durationArray)
	elif(templateSongNumber in line):
		line = line.replace(templateSongNumber, str(len(songs)))
	acs.write(line)
template.close()
acs.close()

################## Now that that's done, use subprocess to create the pk3
loadACS = open('./Jukebox/LOADACS.txt', 'w')
for(_, _, filenames) in os.walk(acsScriptPath):
	for script in filenames:
		#compile with gdcc-acc
		subprocess.call(["./tools/gdcc_acc/gdcc-acc.exe", acsScriptPath + script, acsOutPath + script.split('.')[0] + ".o"])
		loadACS.write(script.split('.')[0] + "\n")
loadACS.close()
subprocess.call(["./tools/7za.exe", "a", "-tzip", pk3Name, ".\\Jukebox\\*.*", ".\\Jukebox\\*"]) #compress into pk3

################## Now clean up the directory
os.remove('./Jukebox/LOADACS.txt')

for file in os.listdir(acsOutPath):
	os.remove(acsOutPath + file)

for file in os.listdir(acsScriptPath):
	os.remove(acsScriptPath + file)

for file in os.listdir(pk3MusicPath):
	os.remove(pk3MusicPath + file)