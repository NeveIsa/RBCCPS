prev_dir=`pwd`
BASEDIR=$(dirname "$0")
tput setaf 1;echo "changing dir to $BASEDIR"
cd $BASEDIR

git add .
git commit -m "auto commit"
git push

tput setaf 1;echo "changing dir to $prev_dir"
cd $prev_dir
