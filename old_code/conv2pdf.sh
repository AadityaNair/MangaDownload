cd ./$1

for ch_name in *
do
    if [ "$ch_name" == "list_location" ]
    then
        continue
    fi
    cd ./"$ch_name"

    convert `ls -tr` ../"$ch_name".pdf
    cd ..
done

cd ..
mkdir "$1_2"
cd $1

cp *.pdf ../"$1_2"
cd ..

rm -rf $1
mv "$1_2" $1
