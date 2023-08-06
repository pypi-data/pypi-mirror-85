import os
from os import environ
import json
import http.client


# custom exceptions
class ContentAIError(Exception):
    """ represents a contentai error """
    pass

# environment variables


# The job_id given to this dag by the ContentAI Platform
job_id = os.getenv("EXTRACTOR_JOB_ID", "")

# The location of the asset you wish to perform inference on
content_url = os.getenv("EXTRACTOR_CONTENT_URL", "")

# when you download the content (download_content())
# you can access the artifact at content_url
content_path = os.getenv("EXTRACTOR_CONTENT_PATH", "")

# write results to this location which you want saved to the Data Lake
result_path = os.getenv("EXTRACTOR_RESULT_PATH", "")

# get extractor name
extractor_name = os.getenv("EXTRACTOR_NAME", "")

# json supplied to this job
metadata_json = os.getenv("EXTRACTOR_METADATA", None)

# whether or not we're running in the platform
running_in_contentai = False
if "RUNNING_IN_CONTENTAI" in os.environ:
    running_in_contentai = (os.environ["RUNNING_IN_CONTENTAI"] == "true")

if running_in_contentai:
    for env_test in ["EXTRACTOR_JOB_ID", "EXTRACTOR_CONTENT_URL", "EXTRACTOR_CONTENT_PATH",
                     "EXTRACTOR_RESULT_PATH", "EXTRACTOR_NAME"]:
        if os.getenv(env_test) is None:
            raise ContentAIError(
                "The environment variable '{}' is required.".format(env_test))

api_host = "127.0.0.1"

# use a docker-friendly host if using the test harness
if "RUNNING_IN_TESTHARNESS" in os.environ:
    if (os.environ["RUNNING_IN_TESTHARNESS"] == "true"):
        api_host = "contentai"


def download_content():
    """ download content to work with locally

returns local path where content is written
    """
    if running_in_contentai:
        path = "/content/"
        conn = http.client.HTTPConnection(api_host)
        conn.request("GET", path)
        res = conn.getresponse()
        body = res.read()
        conn.close()
        if res.status != 200:
            raise ContentAIError(f"GET {path} returned {res.status}: {body}")
        result = json.loads(body)
        return result["contentPath"]


def extractors():
    """ returns a list of all extractors executed against this content url

example:
```json
[
    "extractor1",
    "extractor2"
],
```

```python
# get all data from all extractors
for extractor in contentai.extractors():
    for key in contentai.keys(extractor):
        data = contentai.get(extractor, key)
```
    """
    # json of latest extractors with job ids 
    extractor_runs_json = os.getenv("EXTRACTOR_RUNS", None)

    if extractor_runs_json is not None:        
        return json.loads(extractor_runs_json).keys()
    return []

def metadata():
    """ returns a dict containing input metadata

example:

access metadata that was supplied when running a job
```sh
contentai run s3://bucket/video.mp4 -d '{ "input: "value" }'
```
```python
input = contentai.metadata()["input"]    
```
    """
    result = {}
    if metadata_json is not None:
        result = json.loads(metadata_json)
    return result


def keys(extractor_name):
    """ get a list of keys for specified extractor

returns a dict containing a list of keys
```json
[
  "data.json",
  "data.csv",
  "data.txt"
]
```

example:
```python
keys = contentai.keys("azure_videoindexer")
for key in keys:
    data = contentai.get("azure_videoindexer", key)
```
    """
    if running_in_contentai:
        path = f"/results/{extractor_name}"
        conn = http.client.HTTPConnection(api_host)
        conn.request("GET", path)
        res = conn.getresponse()
        body = res.read()
        conn.close()
        if res.status == 200:
            return json.loads(body)["keys"]
        else:
            raise ContentAIError(f"GET {path} returned {res.status}: {body}")


def get(extractor_name, key):
    """ get the contents of a particular key

example:
```python
# get another extractor's output
data = contentai.get("some_extractor", "output.csv")
```
    """
    if running_in_contentai:
        path = f"/results/{extractor_name}/{key}"
        conn = http.client.HTTPConnection(api_host)
        conn.request("GET", path)
        res = conn.getresponse()
        body = res.read()
        conn.close()
        if res.status == 200:
            return body.decode()
        else:
            raise ContentAIError(f"GET {path} returned {res.status}: {body}")


def get_json(extractor_name, key):
    """ get the json contents of a particular key

example:
```python
# get another extractor's output
data = contentai.get_json("some_extractor", "data.json")
```
    """
    if running_in_contentai:
        path = f"/results/{extractor_name}/{key}"
        conn = http.client.HTTPConnection(api_host)
        conn.request("GET", path)
        res = conn.getresponse()
        body = res.read()
        conn.close()
        if res.status == 200:
            return json.loads(body)
        else:
            raise ContentAIError(f"GET {path} returned {res.status}: {body}")


def get_bytes(extractor_name, key):
    """ get the contents of a particular key in raw bytes

example:
```python
# get another extractor's output
data = contentai.get_bytes("some_extractor", "output.bin")
```
    """
    if running_in_contentai:
        path = f"/results/{extractor_name}/{key}"
        conn = http.client.HTTPConnection(api_host)
        conn.request("GET", path)
        res = conn.getresponse()
        body = res.read()
        conn.close()
        if res.status == 200:
            return body
        else:
            raise ContentAIError(f"GET {path} returned {res.status}: {body}")


def set(key, value):
    """ set results data for this extractor

can be called multiple times with different keys

value is a string

example:
```python
contentai.set("output", "hello world")
```
    """
    result_path = os.environ["EXTRACTOR_RESULT_PATH"]
    with open(result_path + key, 'w') as f:
        f.write(value)


def set_json(key, value):
    """ set results data for this extractor

can be called multiple times with different keys

value can be anything

example:
```python
data = {}
data["foo"] = bar
contentai.set_json("output", data)
```
    """
    set(key, json.dumps(value))


def set_bytes(key, value):
    """ set results data for this extractor

can be called multiple times with different keys

value is bytes

example:
```python
some_file = open("some-file", "rb")
contentai.set_bytes("output", some_file.read())
```
    """
    result_path = os.environ["EXTRACTOR_RESULT_PATH"]
    with open(result_path + key, 'wb') as f:
        f.write(value)


def save_results():
    """ save results immediately, instead of waiting until process exits
    """
    if running_in_contentai:
        path = "/results/"
        conn = http.client.HTTPConnection(api_host)
        conn.request("POST", path)
        res = conn.getresponse()
        body = res.read()
        conn.close()
        if res.status != 201:
            raise ContentAIError(f"GET {path} returned {res.status}: {body}")


def parse_content_url():
    """ extract details from content url   

returns

- source_bucket_name - the s3 bucket name derived from content_url
- source_bucket_key - the s3 bucket key derived from content_url
- source_bucket_region - the s3 bucket region derived from content_url        

the following `content url` formats are supported:

- Simple (CLI) Format - `s3://{bucket}/{key}`
- Virtual Hosted Format - `https://{bucket}.s3.amazonaws.com/{key}`
- Virtual Hosted Format with Region - `https://{bucket}.s3.{region}.amazonaws.com/{key}`
    """

    content_url = os.environ["EXTRACTOR_CONTENT_URL"]

    # default region
    source_bucket_region = "us-east-1"

    # Get source_bucket_name and source_bucket_key
    # Basic
    #  s3://%s%s", bucket, key
    if (content_url.startswith("s3://")):
        content_url = content_url.replace("s3://", "")

        indexValue = content_url.index("/")

        # Location of the video file we want to process
        source_bucket_name = content_url[0:indexValue]
        source_bucket_key = content_url[indexValue + 1:]

    # VirtualHosted
    #  "http://%s.s3.amazonaws.com%s", bucket, key
    # VirtualHosted_Region
    #  "http://%s.s3-%s.amazonaws.com%s", bucket, region, key
    elif (content_url.startswith("http")):
        # bucket name = get me everything between :// and .s3
        start = "://"
        end = ".s3"
        source_bucket_name = content_url[content_url.find(
            start)+len(start):content_url.rfind(end)]

        # everything after "amazonaws.com/" is the key
        source_bucket_key = content_url.split("amazonaws.com/", 1)[1]

    else:
        raise NameError(
            f"content url {content_url} does not match expected format")

    # Get source_bucket_region
    # VirtualHosted_Region
    #  "http://%s.s3-%s.amazonaws.com%s", bucket, region, key
    if ".s3-" in content_url:
        start = ".s3-"
        end = ".amazonaws.com"
        source_bucket_region = content_url[content_url.find(
            start)+len(start):content_url.rfind(end)]
    elif ".s3." in content_url and ".s3.amazonaws.com" not in content_url:
        start = ".s3."
        end = ".amazonaws.com"
        source_bucket_region = content_url[content_url.find(
            start)+len(start):content_url.rfind(end)]

    return source_bucket_name, source_bucket_key, source_bucket_region
