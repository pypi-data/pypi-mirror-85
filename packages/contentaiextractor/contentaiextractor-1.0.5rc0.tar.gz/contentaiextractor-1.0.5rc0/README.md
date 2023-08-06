# contentai-extractor-runtime-python

This is a python package used for implementing a custom extractor that runs on the ContentAI platform.

https://pypi.org/project/contentaiextractor/

1. [Usage](#Usage)
2. [API Documentation](#API-Documentation)
3. [Develop](#Develop)
3. [Changes](#Changes)

# Usage

```sh
pip install contentaiextractor
```

```python
import contentaiextractor as contentai

# download content locally
content_path = contentai.download_content()

# access metadata that was supplied when running a job
# contentai run s3://bucket/video.mp4 -d '{ "input": "value" }'
inputData = contentai.metadata()["input"]

# get output from another extractor
csv = contentai.get("extractor", "data.csv")
json = contentai.get_json("extractor", "data.json")

# extract some data
outputData = []
outputData.append({"frameNumber": 1})

# output data from this extractor
contentai.set("output", outputData)
```

# API Documentation

<a name="contentaiextractor.ContentAIError"></a>
## ContentAIError Objects

```python
class ContentAIError(Exception)
```

represents a contentai error


## Fields

- `extractor_name` - name of the extractor being run
- `job_id` - current job id
- `content_url` - URL of the content the extractor is run against
- `content_path` - local path where the extractor can access the content
- `result_path` - local path where the extractor should write the results
- `running_in_contentai` - boolean set to `True`; useful for testing code locally
- `metadata_json` - raw string (or `None` if not set) for active extractor run (also, see parsed [metadata()](#metadata)`)

## Functions

<a name="contentaiextractor.download_content"></a>
#### download\_content

```python
download_content()
```

download content to work with locally

returns local path where content is written

<a name="contentaiextractor.metadata"></a>
#### metadata

```python
metadata()
```

returns a dict containing input metadata

example:

access metadata that was supplied when running a job
```sh
contentai run s3://bucket/video.mp4 -d '{ "input: "value" }'
```
```python
input = contentai.metadata()["input"]    
```

<a name="contentaiextractor.keys"></a>
#### keys

```python
keys(extractor_name)
```

get a list of keys for specified extractor

returns a dict containing a list of keys
```json
[
  "data.json",
  "data.csv",
  "data.txt,"
]
```

example:
```python
keys = contentai.keys("azure_videoindexer")
for key in keys:
    data = contentai.get("azure_videoindexer", key)
```

<a name="contentaiextractor.get"></a>
#### get

```python
get(extractor_name, key)
```

get the contents of a particular key

example:
```python
# get another extractor's output
data = contentai.get("some_extractor", "output.csv")
```

<a name="contentaiextractor.get_json"></a>
#### get\_json

```python
get_json(extractor_name, key)
```

get the json contents of a particular key

example:
```python
# get another extractor's output
data = contentai.get_json("some_extractor", "data.json")
```

<a name="contentaiextractor.get_bytes"></a>
#### get\_bytes

```python
get_bytes(extractor_name, key)
```

get the contents of a particular key in raw bytes

example:
```python
# get another extractor's output
data = contentai.get_bytes("some_extractor", "output.bin")
```

<a name="contentaiextractor.set"></a>
#### set

```python
set(key, value)
```

set results data for this extractor

can be called multiple times with different keys

value is a string

example:
```python
contentai.set("output", "hello world")
```

<a name="contentaiextractor.set_json"></a>
#### set\_json

```python
set_json(key, value)
```

set results data for this extractor

can be called multiple times with different keys

value can be anything

example:
```python
data = {}
data["foo"] = bar
contentai.set_json("output", data)
```

<a name="contentaiextractor.set_bytes"></a>
#### set\_bytes

```python
set_bytes(key, value)
```

set results data for this extractor

can be called multiple times with different keys

value is bytes

example:
```python
some_file = open("some-file", "rb")
contentai.set_bytes("output", some_file.read())
```

<a name="contentaiextractor.save_results"></a>
#### save\_results

```python
save_results()
```

save results immediately, instead of waiting until process exits

<a name="contentaiextractor.parse_content_url"></a>
#### parse\_content\_url

```python
parse_content_url()
```

extract details from content url

returns

- `source_bucket_name` - the s3 bucket name derived from content_url
- `source_bucket_key` - the s3 bucket key derived from content_url
- `source_bucket_region` - the s3 bucket region derived from content_url        

the following `content url` formats are supported:

- Simple (CLI) Format - `s3://{bucket}/{key}`
- Virtual Hosted Format - `https://{bucket}.s3.amazonaws.com/{key}`
- Virtual Hosted Format with Region - `https://{bucket}.s3.{region}.amazonaws.com/{key}`


# Develop

```
 Choose a make command to run

  build    build package
  deploy   upload package to pypi
  docs     generates api docs in markdown
```

### Changes

- 1.0.4
  - updated changelog

- 1.0.3
  - fixes issue where `EXTRACTOR_METADATA` envvar was indavertently required

- 1.0.2
  - add safety to setting retrieval on local runs
  - documentation updates 

- 1.0.1
  - api docs for publish to pypi

- 1.0.0
  - initial release
