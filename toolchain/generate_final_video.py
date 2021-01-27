import os
import time


def main():
    begin = time.time()
    os.system(r"""ffmpeg -r 30 -i .\rendered-images\%d.png -s 1920x1080 -c:v libx264 -b:v 500k -vf fps=30 output1.mp4 -y""")
    os.system(
        r"""ffmpeg -i output1.mp4 -i myaudio.m4a -c:v copy -c:a aac -strict experimental -b:v 500k output.mp4 -y""")
    end = time.time()
    print(f"{end-begin}s")


if __name__ == "__main__":
    main()
