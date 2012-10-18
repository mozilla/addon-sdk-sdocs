# prepare git for a fresh set of docs
#bash git_prepare_commit.sh

pos=$(expr $1 : '[0-9,\.]*')
latest_version=${1:0:$pos}

# get the releases and generate docs for them
latest_version_tag=$1
old_version1=$2
old_version2=$3
bash get_releases.sh $latest_version_tag $old_version1 $old_version2

# obsolete old versions
pos=$(expr $latest_version_tag : '[0-9,\.]*')
latest_version=${1:0:$pos}

python obsolete.py $old_version1 $latest_version $4
python obsolete.py $old_version2 $latest_version $4

# make the commit
#bash git_commit.sh $1
