
mkdir sdk/$1

mkdir working
cd working

mkdir $1
cd $1

curl -O https://ftp.mozilla.org/pub/mozilla.org/labs/jetpack/addon-sdk-$1.tar.gz
tar -xf addon-sdk-$1.tar.gz
cd addon-sdk-$1
source bin/activate
cfx sdocs
tar -xf addon-sdk-docs.tgz
mv addon-sdk-docs/* ../../../sdk/$1
mv doc/* ../../../sdk/$1
cd ../../
