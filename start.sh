source build-sub.sh SDE

# Do the cleanning
WORKSPACE=$PWD
cd server/pdf
for d in */ ; do
    cd $d
    rm !(*.pdf)
    cd ..
done
cd $WORKSPACE