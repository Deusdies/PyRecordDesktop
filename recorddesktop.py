#!/usr/bin/python2.7
#########################################################
#### PyRecordDesktop 0.1
#### By Bogdan Milanovic
####
#### In the absence of a decent linux application that
#### records a desktop into a video (and no, the
#### recordMyDesktop does not qualify as one), I have 
#### decided to write my own.
####
#### PyRecordDesktop uses ffmpeg (which most distros come
#### installed with) to capture the video and encode it
#### on the fly. It also uses ALSA to capture the sound
#### from any input devices (such as a microphone). 
#### A Qt powered GUI is planned.
#########################################################

import subprocess
import sys
import argparse
import shlex
import os

#First we define the default values of the main parameters
DEFAULT_RESOLUTION = "1920x1080"
DEFAULT_CODEC = "h264"
DEFAULT_OUTPUTFILE = "output.avi"

#Then we define tuples (immutable) of the supported formats and resolutions.
#Hopefully we'll be able to grab these values automatically in the future
RESOLUTION_LIST = ("1920x1080", "1366x768", "1280x720")
CODEC_LIST = ("mpeg4", "flv", "h264")

#Parsing the arguments given in the command line
#These arguments include: output file, desired recording resolution, and the video encoding codec
parser = argparse.ArgumentParser()
parser.add_argument("outputfile", help="The output filename")
parser.add_argument("--res", help="Recording resolution: 1920x1080, 1366x768, or 1280x720")
parser.add_argument("--codec", help="Video encoding codec: libx264, mpeg4, flv, h264")
args = parser.parse_args()

#We check to make sure that the arguments have been passed 
#Otherwise we use the default values  as defined above
resolution = args.res if args.res else DEFAULT_RESOLUTION
codec = args.codec if args.codec else DEFAULT_CODEC
outputfile = args.outputfile if args.outputfile else DEFAULT_OUTPUTFILE

#A couple of checks to make sure the resolution and the codec are valid
if resolution not in RESOLUTION_LIST:
	print "Invalid resolution. Run {0} -h for details".format(__file__)
	sys.exit(1)

if codec not in CODEC_LIST:
	print "Invalid codec. Run {0} -h for details".format(__file__)
	sys.exit(1)

#The command string that we'll execute. LOTS of manipulation here available!
command = """ffmpeg -f x11grab -y -r 30 -s {0} -i :0.0 -vcodec {1} -sameq -f alsa -i default -ar 44100 -acodec libmp3lame -ac 2 {2}""".format(resolution, codec, args.outputfile)

#print command

arguments = shlex.split(command)

#Finally, we call the command and start recording (naturally within try/except clause)
try:
	process = subprocess.Popen(arguments)
	process.communicate()[0]
except KeyboardInterrupt:
	process.kill()
	print "\r\n"
	print "The file has been saved to {0}".format(os.path.abspath(args.outputfile))
	print "Goodbye!"	
	sys.exit(0)
except Exception, e:
	print "Something went wrong when we tried to start the recording!"
	print "The error is {0}".format(str(e))
	sys.exit(2)

