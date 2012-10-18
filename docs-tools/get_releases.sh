mkdir sdk/$1
mkdir sdk/$2
mkdir sdk/$3

mkdir working
cd working
mkdir $1
mkdir $2
mkdir $3

function get_release {
  cd $1
  curl -O https://ftp.mozilla.org/pub/mozilla.org/labs/jetpack/addon-sdk-$1.tar.gz
  tar -xf addon-sdk-$1.tar.gz
  cd addon-sdk-$1
  source bin/activate
  cfx sdocs
  tar -xf addon-sdk-docs.tgz
  mv doc/* ../../../sdk/$1
  cd ../../
}

# get the latest release
cd $1
git clone https://github.com/mozilla/addon-sdk.git
cd addon-sdk
git checkout $1
source bin/activate
pos=$(expr $1 : '[0-9,\.]*')
echo ${1:0:$pos}
cfx sdocs --override-version=$1
tar -xf addon-sdk-docs.tgz
mv doc/* ../../../sdk/$1
cd ../../

get_release $2
get_release $3

rm -rf *
rm -rf .DS_Store
cd ..
rmdir working


