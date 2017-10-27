python IndexFilesPreprocess.py --index testsinfilter1 --path /tmp/novels --token letter
python IndexFilesPreprocess.py --index testlowercase1 --path /tmp/novels --token letter --filter lowercase 
python IndexFilesPreprocess.py --index testascii1 --path /tmp/novels --token letter --filter lowercase asciifolding
python IndexFilesPreprocess.py --index teststop1 --path /tmp/novels --token letter --filter lowercase asciifolding stop
python IndexFilesPreprocess.py --index testsnowball1 --path /tmp/novels --token letter --filter lowercase asciifolding snowball
python IndexFilesPreprocess.py --index testporterstem1 --path /tmp/novels --token letter --filter lowercase asciifolding porter_stem
python IndexFilesPreprocess.py --index testkstem1 --path /tmp/novels --token letter --filter lowercase asciifolding kstem

python IndexFilesPreprocess.py --index testsinfilter2 --path /tmp/novels --token whitespace
python IndexFilesPreprocess.py --index testlowercase2 --path /tmp/novels --token whitespace --filter lowercase 
python IndexFilesPreprocess.py --index testascii2 --path /tmp/novels --token whitespace --filter lowercase asciifolding
python IndexFilesPreprocess.py --index teststop2 --path /tmp/novels --token whitespace --filter lowercase asciifolding stop
python IndexFilesPreprocess.py --index testsnowball2 --path /tmp/novels --token whitespace --filter lowercase asciifolding snowball
python IndexFilesPreprocess.py --index testporterstem2 --path /tmp/novels --token whitespace --filter lowercase asciifolding porter_stem
python IndexFilesPreprocess.py --index testkstem2 --path /tmp/novels --token whitespace --filter lowercase asciifolding kstem

python IndexFilesPreprocess.py --index testsinfilter3 --path /tmp/novels --token classic
python IndexFilesPreprocess.py --index testlowercase3 --path /tmp/novels --token classic --filter lowercase 
python IndexFilesPreprocess.py --index testascii3 --path /tmp/novels --token classic --filter lowercase asciifolding
python IndexFilesPreprocess.py --index teststop3 --path /tmp/novels --token classic --filter lowercase asciifolding stop
python IndexFilesPreprocess.py --index testsnowball3 --path /tmp/novels --token classic --filter lowercase asciifolding snowball
python IndexFilesPreprocess.py --index testporterstem3 --path /tmp/novels --token classic --filter lowercase asciifolding porter_stem
python IndexFilesPreprocess.py --index testkstem3 --path /tmp/novels --token classic --filter lowercase asciifolding kstem

python IndexFilesPreprocess.py --index testsinfilter4 --path /tmp/novels --token standard
python IndexFilesPreprocess.py --index testlowercase4 --path /tmp/novels --token standard --filter lowercase 
python IndexFilesPreprocess.py --index testascii4 --path /tmp/novels --token standard --filter lowercase asciifolding
python IndexFilesPreprocess.py --index teststop4 --path /tmp/novels --token standard --filter lowercase asciifolding stop
python IndexFilesPreprocess.py --index testsnowball4 --path /tmp/novels --token standard --filter lowercase asciifolding snowball
python IndexFilesPreprocess.py --index testporterstem4 --path /tmp/novels --token standard --filter lowercase asciifolding porter_stem
python IndexFilesPreprocess.py --index testkstem4 --path /tmp/novels --token standard --filter lowercase asciifolding kstem


