# S3Bz
> save and load dictionary to s3 using bz compression


## Install

`pip install s3bz`

## How to use

### Create a bucket and make sure that it has transfer acceleration enabled
#### create a buket
`aws s3 mb s3://<bucketname>`
#### put transfer acceleration
`aws s3api put-bucket-accelerate-configuration --bucket <bucketname> --accelerate-configuration Status=Enabled`

First, import the s3 module

## import package

```python
from importlib import reload
from s3bz.s3bz import S3
```

### set up dummy data

```python
bucket = 'pybz-test'
key = 'test.dict'
sampleDict = {'test': 'bool'}
USER = None
PW = None
```

## save object

```python
result = S3.save(key = key, 
       objectToSave = sampleDict,
       bucket = bucket,
       user=USER,
       pw = PW,
       accelerate = True)
print(('failed', 'success')[result])
```

    success


## check if an object exist

```python
result = S3.exist('', bucket, user=USER, pw=PW, accelerate = True)
print(('doesnt exist', 'exist')[result])
```

    exist


## load object

```python
result = S3.load(key = key,
       bucket = bucket,
       user = USER,
       pw = PW,
       accelerate = True)
print(result[0])
```

    {'ib_prcode': '58813', 'ib_brcode': '1029', 'ib_cf_qty': '314', 'new_ib_vs_stock_cv': '273'}


## presign download object

```python
url = S3.presign(key=key,
              bucket=bucket,
              expiry = 1000,
              user=USER,
              pw=PW)
print(url)
```

    https://pybz-test.s3-accelerate.amazonaws.com/test.dict?AWSAccessKeyId=AKIAVX4Z5TKDVNE5QZPQ&Signature=bv5NIDX5QCyTYO8X%2Buoy%2FxogDBk%3D&Expires=1605358067


### download using signed link

```python
from s3bz.s3bz import Requests
result = Requests.getContentFromUrl(url)
```

## File operations

### save

```python
inputPath = '/tmp/tmpFile.txt'
key = 'tmpFile'
downloadPath = '/tmp/downloadTmpFile.txt'
with open(inputPath , 'w')as f:
  f.write('hello world')
```

```python
S3.saveFile(key =key ,path = inputPath,bucket = bucket)
##test
S3.exist(key,bucket)
```




    True



### load

```python
S3.loadFile(key= key , path = downloadPath, bucket = bucket)
```

```python
##test
with open(downloadPath, 'r') as f:
  print(f.read())
```

    hello world


### delete

```python
result = S3.deleteFile(key, bucket)
## test
S3.exist(key,bucket)
```




    False


