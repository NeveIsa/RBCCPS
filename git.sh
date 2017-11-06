prev_dir=`pwd`
BASEDIR=$(dirname "$0")
echo "changing dir to $BASEDIR"
cd $BASEDIR

git add .
git commit -m "auto commit"
git push

echo "changing dir to $prev_dir"
cd $prev_dir
