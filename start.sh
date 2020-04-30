echo 'Start building SDE'
bash build-sub.sh SDE

echo 'Start building FA'
bash build-sub.sh functional-analysis

echo 'Start building TSA'
bash build-sub.sh tsa

echo 'Start building StCal'
bash build-sub.sh st-cal

# Do the cleanning
WORKSPACE=$PWD
cd server/pdf
for d in */ ; do
    cd $d
    rm !(*.pdf)
    cd ..
done
cd $WORKSPACE