#!/bin/bash

repo_url="https://github.com/thegraey/deletedTweets.git"
repo_dir="$(git rev-parse --show-toplevel)"
forked_repo_name="$(basename $(git rev-parse --show-toplevel))"

# Functions
usage() {
    echo -e "Usage: \n\t$0 \n"
    exit 0
}

set_upstream() {
    cd $repo_dir

    echo -e "Configuring upstream git repository\n"
    # Set upstream remote repository git repo URL if project has been forked
    git remote add upstream $repo_url

}

check_mergable() {
    # Merge changes made on original project repo into forked repo
    git merge upstream/main $forked_repo_name > /dev/null 2>&1
    rc=$? && echo $rc > /dev/null 2>&1

    if [ "$rc" == 0 ]
    then
        echo -e "Attempting to merge fetched changes into forked project repo\n"
    else
        echo -e "No changes found in upstream git repository\n"
    fi

}

main() {
    # Check if help flag is supplied when invoking script
    if [[ ( $@ == "--help" ) || $@ == "-h" ]]
    then
        usage
	exit 1
    fi

    git remote | grep upstream > /dev/null 2>&1
    rc=$? && echo $rc > /dev/null 2>&1

    if [ "$rc" == 1 ]
    then
        set_upstream
    else
        echo "Upstream git repository has already been set"
    fi

    # Fetch changes made on original project repo
    echo -e "Fetching changes made on original project repo\n"
    git fetch upstream

    # Check for mergable changes from original project repo 
    check_mergable

}

main

