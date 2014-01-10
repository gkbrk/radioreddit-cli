import subprocess, sys, re

if sys.argv.__len__() > 1:
    stream_name = sys.argv[1]
else:
    stream_name = "main"

stream_name_to_url = {
    "main": "http://173.231.136.91:8000/",
    "random": "http://173.231.136.91:8050/",
    "rock": "http://173.231.136.91:8020/",
    "metal": "http://173.231.136.91:8090/",
    "indie": "http://173.231.136.91:8070/"
}

player = subprocess.Popen(["mplayer", stream_name_to_url[stream_name]], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

try:
    while not player.poll():
        player_line = player.stdout.readline()
        if player_line.startswith("ICY Info: "):
            song_name = re.match("ICY Info: StreamTitle='(.*?)';StreamUrl='';", player_line).group(1)
            print "New song! %s" % song_name
except KeyboardInterrupt:
    player.kill()
except Exception, e:
    print e
