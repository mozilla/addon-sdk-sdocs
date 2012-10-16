mkdir sdks
cd sdks
mkdir $1
mkdir $2
mkdir $3

function obsolete {
  cd ../../$1
  curl -O https://ftp.mozilla.org/pub/mozilla.org/labs/jetpack/addon-sdk-$1.tar.gz
  tar -xf addon-sdk-$1.tar.gz
  cd addon-sdk-$1
  python ../../../obsolete.py doc/static-files/base.html
  source bin/activate
  cfx docs
}

cd $1
git clone https://github.com/mozilla/addon-sdk.git
cd addon-sdk
git checkout $1
source bin/activate
pos=$(expr $1 : '[0-9,\.]*')
echo ${1:0:$pos}
cfx docs #--version=$1
echo expr match "$1" '\(.[b-c]*[A-Z]..[0-9]\)'

obsolete $2
obsolete $3
