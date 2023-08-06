import argparse
from .mlrd import run

def start():
    parser = argparse.ArgumentParser(
        description="A tool to download MyCourses lecture recordings"
    )

    parser.add_argument("course_id", help="The LRS course id", type=int)

    # todo: need to expand '~' in dir (absolute path resolution)
    parser.add_argument("output_dir", help="Directory of where to download the course's lectures")
    
    parser.add_argument("auth_token", help="A fresh bearer authorization token for MyCourses")

    args = parser.parse_args()
    run(args.course_id, args.output_dir, args.auth_token)

def main():
    start()