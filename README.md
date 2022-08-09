# bioflex: Python package for calling BioTuring API

**bioflex** allows scientists to use simple yet powerful commands to retrieve gene expression data,<br>
cell metadata from thousands of single-cell studies in BioTuring Database.

## Installation

```sh
pip install bioflex
```

For access token, register at [BioTuring Data Science](https://datascience.bioturing.com)

## Requirements

- [Requests](https://requests.readthedocs.io/)
- [NumPy](https://www.numpy.org)
- [SciPy](https://scipy.org/)
- [tqdm](https://tqdm.github.io/)
- [H5Py](https://www.h5py.org/)

## Examples

### Create a connection using access token:

```python
import bioflex
connection = bioflex.connect('70d2acfda3a54ca6a4390699394****')
```

### List available databases:

```python
databases = connection.databases()
```
>```
> [DataBase(id="5010c7d573ae4ff2b9691422b99aa2cd",
>           name="BioTuring database",species="human",version=1),
> DataBase(id="5010c7d573ae4ff2b9691422b99aa2cd",
>           name="BioTuring database",species="human",version=2),
> DataBase(id="5010c7d573ae4ff2b9691422b99aa2cd",
>           name="BioTuring database",species="human",version=3)]

### Get database cell types gene expression summary

```python
database = databases[2]
database.get_celltypes_expression_summary(['CD3D', 'CD3E'])
```
>```
> {'CD3D': [Summary(name="B cell",sum=707108874.0,mean=4192.7096,rate=0.035,count=168652.0,total=4812967),
> 	Summary(name="CD4-positive, alpha-beta T cell",sum=9489987442.0,mean=4657.5619,rate=0.5283,count=2037544.0,total=3856590),
> 	...
> 	Summary(name="corneal progenitor",sum=0.0,mean=0.0,rate=0.0,count=0.0,total=3973),
> 	Summary(name="nucleus pulposus progenitor cell",sum=0.0,mean=0.0,rate=0.0,count=0.0,total=2310)]}


### Create study instance, using study hash ID from [BioTuring studies](https://talk2data.bioturing.com/studies/):

```python
study = database.get_study('GSE96583_batch2')
study
```
>```
> Study(id="1557",hash_id="GSE96583_batch2",
>       title="Multiplexed droplet single-cell RNA-sequencing using natural genetic variation (Batch 2)",
>       reference="https://www.nature.com/articles/nbt.4042")

### Take a peek at study metadata:

```python
study.metalist
```
>```
> [Metadata(id=0,name="Number of mRNA transcripts",type="Numeric"),
>  Metadata(id=1,name="Number of genes",type="Numeric"),
>  Metadata(id=2,name="Batch id",type="Category"),
>  Metadata(id=3,name="Stimulation",type="Category"),
>  Metadata(id=4,name="Author's cell type",type="Category")]

### Fetch a study metadata:

```python
metadata = study.metalist[4]
metadata
```
>```
>Metadata(id=4,name="Author's cell type",type="Category")
```python
metadata.fetch()
metadata.values
```
>```
> array(['CD8 T cells', 'Dendritic cells', 'CD4 T cells', ...,
>        'CD8 T cells', 'B cells', 'CD4 T cells'], dtype='<U17')

### Query genes:

```python
exp_mtx = study.query_genes(['CD3D', 'CD3E'], bioflex.UNIT_LOGNORM)
exp_mtx
```
>```
> <29065x2 sparse matrix of type '<class 'numpy.float32'>'
>     with 15492 stored elements in Compressed Sparse Column format>

### Get study barcodes:

```python
study.barcodes()
```
>```
> ['GSM2560249_AAACATACCAAGCT-1',
>  'GSM2560249_AAACATACCCCTAC-1',
>  ...
>  'GSM2560249_AATTGTGATTCACT-1',
>  'GSM2560249_AATTGTGATTTCGT-1',
>  ...]

### Get study features:

```python
study.features()
```
>```
> ['5S_RRNA',
>  '5_8S_RRNA',
>  ...
>  'AC006273',
>  'AC006277',
>  ...]

### Get study full matrix:

```python
study.matrix(bioflex.UNIT_LOGNORM)
```
>```
> <29065x64642 sparse matrix of type '<class 'numpy.float32'>'
> 	with 17570739 stored elements in Compressed Sparse Column format>

----
For further information please check the [documentation](https://datascience.bioturing.com/).
