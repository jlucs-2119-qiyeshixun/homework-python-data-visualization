python3 script/popular_data.py 

tme=`date`
commit="git commit -m'[data]`date`'"
echo $commit
git add .

echo $commit | bash

git push origin master:popular_data
