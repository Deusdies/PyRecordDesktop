#!/usr/bin/python2.7
import subprocess
import sys
import argparse
import shlex
import os

DEFAULT_RESOLUTION = "1920x1080"
DEFAULT_CODEC = "h264"
DEFAULT_OUTPUTFILE = "output.avi"

RESOLUTION_LIST = ["1920x1080", "1366x768", "1280x720"]
CODEC_LIST = ["mpeg4", "flv", "h264"]

parser = argparse.ArgumentParser()
parser.add_argument("outputfile", help="The output filename")
parser.add_argument("--res", help="Recording resolution: 1920x1080, 1366x768, or 1280x720")
parser.add_argument("--codec", help="Video encoding codec: libx264, mpeg4, flv, h264")
args = parser.parse_args()

resolution = args.res if args.res else DEFAULT_RESOLUTION
codec = args.codec if args.codec else DEFAULT_CODEC
outputfile = args.outputfile if args.outputfile else DEFAULT_OUTPUTFILE

if resolution not in RESOLUTION_LIST:
	print "Invalid resolution. Run {0} -h for details".format(__file__)

if codec not in CODEC_LIST:
	print "Invalid codec. Run {0} -h for details".format(__file__)

command = """ffmpeg -f x11grab -y -r 30 -s {0} -i :0.0 -vcodec {1} -sameq -f alsa -i default -ar 44100 -acodec libmp3lame -ac 2 {2}""".format(resolution, codec, args.outputfile)

#print command

arguments = shlex.split(command)

try:
	process = subprocess.Popen(arguments)
	process.communicate()[0]
except KeyboardInterrupt:
	process.kill()
	print "\r\n"
	print "The file has been saved to {0}".format(os.path.abspath(args.outputfile))
	print "Goodbye!"	
	sys.exit(0)

