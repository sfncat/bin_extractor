# bin_extractor
only support bin->ubi->ubifs->files

other type can use https://github.com/fkie-cad/fact_extractor

## install binwalk 

https://github.com/ReFirmLabs/binwalk/blob/master/INSTALL.md

```
git clone https://github.com/ReFirmLabs/binwalk.git
cd binwalk
python3 setup.py install
```

## install ubi_reader

```
sudo apt-get install liblzo2-dev
sudo pip3 install python-lzo
sudo pip3 install ubi_reader
```

## usage

```
python3 bin_extrator.py /tmp/a.bin
```



