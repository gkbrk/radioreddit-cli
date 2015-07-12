import subprocess
import sys
import re

streams = {
    "main": "http://173.231.136.91:8000/",
    "random": "http://173.231.136.91:8050/",
    "rock": "http://173.231.136.91:8020/",
    "metal": "http://173.231.136.91:8090/",
    "indie": "http://173.231.136.91:8070/"
}

def main():
    if len(sys.argv) > 1:
        stream_name = sys.argv[1]
    else:
        stream_name = "main"

    try:
        player = subprocess.Popen(["mplayer", streams[stream_name]], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    except KeyError:
        print("Usage: {} [station]".format(sys.argv[0]))
        print("Available stations: {}".format(", ".join(streams)))
        print("Default stream: main")
        sys.exit(1)
    except FileNotFoundError:
        print("You need to have mplayer to use radioreddit.")
        sys.exit(1)

    try:
        while not player.poll():
            player_line = player.stdout.readline().decode("utf-8")
            if player_line.startswith("ICY Info: "):
                song_name = re.match("ICY Info: StreamTitle='(.*?)';StreamUrl='';", player_line).group(1)
                print("New song! {}".format(song_name))
    except KeyboardInterrupt:
        player.kill()
    except Exception as e:
        print("Exception: {}".format(e))

if __name__ == "__main__":
    main()
