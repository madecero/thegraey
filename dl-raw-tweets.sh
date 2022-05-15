#!/bin/bash

repo_dir="$(git rev-parse --show-toplevel)"
url=$1
filename=$2

# Functions
usage() {
    echo -e "Usage: \n\t$0 [url] [filename] \n"
    exit 0
}

download_raw_tweets_file (){
    # Download file from URL into git repo directory
    echo -e "Downloading file from the following url:\n\t$url\n"

    time wget -O $filename $url

    echo -e "\nDownload complete..\nFile directory location:\n\t$repo_dir\nFiles:"
    ls -l $repo_dir

}

main() {
    # Check if help flag is supplied when invoking script
    if [[ ( $@ == "--help" ) || $@ == "-h" ]]
    then
        usage
	exit 1
    fi

    download_raw_tweets_file
}

main

