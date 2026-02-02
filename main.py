import argparse
from modules.vision import init_picam, vision_loop

#-----------------------
# Argument parsing
#-----------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="hailo10h vision"
    )

    parser.add_argument(
        "--resolution",
        default="full",
        choices = ["full", "1080p", "720p", "480p"],
        help="Camera resolution presets - full (default), 1080p, 720p, 480"
    )
    return parser.parse_args()

#-----------------------
# MAIN
#-----------------------
def main():
    args = parse_args()
    picam2 = init_picam(args.resolution)
    vision_loop(picam2)

if __name__ == "__main__":
    main()
