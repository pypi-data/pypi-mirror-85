import getpass
import argparse
import os
import pkgutil
import pkg_resources

IMAGE_MAP = {
    'base': 'jupyter/minimal-notebook',
    'scipy': 'jupyter/scipy-notebook',
    'tf': 'jupyter/tensorfolow-notebook'
}


def get_user_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a',
                        '--author',
                        default=getpass.getuser(),
                        help='creater of jupyter notebook')

    parser.add_argument('-i',
                        '--base-image',
                        choices=('base', 'scipy', 'tf'),
                        default='base',
                        help='notebook uses scipy functionality')

    parser.add_argument('-b',
                        '--build',
                        action='store_true',
                        help='build docker image')

    parser.add_argument(
        '-r',
        '--run',
        action='store_true',
        help='run jupyter while mapping current working directory')

    parser.add_argument('-c',
                        '--compose',
                        action='store_true',
                        help='generate docker compose file')

    return parser.parse_args()


def write_dockerfile(image, author, installed_packages):
    with open('Dockerfile', 'w+') as f:
        f.write(f'FROM {image}\n'
                f'LABEL author="{author}"\n'
                f'USER root\n'
                f'RUN pip install {" ".join(installed_packages)}\n'
                f'USER $NB_UID\n')


def process_user_args(args):
    image = IMAGE_MAP[args.base_image]
    author = args.author

    installed_packages = os.popen(
        "pipdeptree  | grep -v '^\s*-'").read().split()
    print(installed_packages)

    return image, author, installed_packages


def build_notebook_image():
    os.system('docker build -t docktered-nb .')


def run_notebook():
    os.system(
        'docker run -p 8888:8888 -v $(pwd):/home/jovyan/work docktered-nb')


def main():
    args = get_user_args()
    image, author, installed_packages = process_user_args(args)
    print
    write_dockerfile(image, author, installed_packages)

    if args.build:
        build_notebook_image()

    if args.run:
        run_notebook()


if __name__ == '__main__':
    main()
