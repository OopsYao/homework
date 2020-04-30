echo 'Start building SDE'
source build-sub.sh SDE

echo 'Start building FA'
source build-sub.sh functional-analysis

echo 'Start building TSA'
source build-sub.sh tsa

echo 'Start building StCal'
source build-sub.sh st-cal

# Do the cleanning
WORKSPACE=$PWD
cd server/pdf
for d in */ ; do
    cd $d
    rm !(*.pdf)
    cd ..
done
cd $WORKSPACE