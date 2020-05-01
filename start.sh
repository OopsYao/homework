echo 'Start building SDE'
bash build-sub.sh SDE
if [ $? -ne 0 ]; then
    status=1
fi

echo 'Start building FA'
bash build-sub.sh functional-analysis
if [ $? -ne 0 ]; then
    status=1
fi

echo 'Start building TSA'
bash build-sub.sh tsa
if [ $? -ne 0 ]; then
    status=1
fi

echo 'Start building StCal'
bash build-sub.sh st-cal
if [ $? -ne 0 ]; then
    status=1
fi

# Do the cleanning
mkdir -p server/pdf
cp -r outputs/* server/pdf
WORKSPACE=$PWD
cd server/pdf
for d in */ ; do
    cd $d
    rm !(*.pdf)
    cd ..
done
cd $WORKSPACE
if [ $status -eq 1 ]; then
    exit 1
fi