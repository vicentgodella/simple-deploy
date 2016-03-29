#! /usr/bin/python

import argparse
import os

tmp_directory = '/tmp/_simple-deploy/' + str(os.getpid())
os.makedirs(tmp_directory)
cache_directory = tmp_directory + '/cache'


def deploy(url):
    filename = tmp_directory + '/file.tar.gz'
    os.system('/usr/local/bin/aws s3 cp ' + url + ' ' + filename)
    os.system('rm -rf ' + cache_directory)
    os.makedirs(cache_directory)
    os.system('tar xfz ' + filename + ' -C ' + cache_directory)


def install(environment):
    os.chdir(cache_directory)
    os.system('./install.sh {}'.format(environment))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deploy a package.')
    parser.add_argument('url', help='S3 url of the package to install: s3://BUCKET/KEY.tar.gz')
    parser.add_argument('environment', help='Environment', choices=["beta", "pre", "prod"])

    args = parser.parse_args()
    url = args.url
    environment = args.environment

    deploy(url)
    install(environment)
    # Clean up
    os.system('rm -rf ' + tmp_directory)

