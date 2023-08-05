# AWS_SCHEMA
> dataclass for aws dictionaries


This library aims to parse aws dictionaries and json strings into dataclass objects

## Install

`pip install awsSchema`

## How to use

extract data from aws classes eg apigateway lambda input/output
this library uses jsondataclass, and dataclass

```python
from awsSchema.apigateway import Response, Event
```

## parsing event

```python
dummyEvent =  { "resource": "/{proxy+}", "path": "/hello/world", "httpMethod": "POST", "headers": { "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "cache-control": "no-cache", "CloudFront-Forwarded-Proto": "https", "CloudFront-Is-Desktop-Viewer": "true", "CloudFront-Is-Mobile-Viewer": "False", "CloudFront-Is-SmartTV-Viewer": "False", "CloudFront-Is-Tablet-Viewer": "False", "CloudFront-Viewer-Country": "US", "Content-Type": "application/json", "headerName": "headerValue", "Host": "gy415nuibc.execute-api.us-east-1.amazonaws.com", "Postman-Token": "9f583ef0-ed83-4a38-aef3-eb9ce3f7a57f", "User-Agent": "PostmanRuntime/2.4.5", "Via": "1.1 d98420743a69852491bbdea73f7680bd.cloudfront.net (CloudFront)", "X-Amz-Cf-Id": "pn-PWIJc6thYnZm5P0NMgOUglL1DYtl0gdeJky8tqsg8iS_sgsKD1A==", "X-Forwarded-For": "54.240.196.186, 54.182.214.83", "X-Forwarded-Port": "443", "X-Forwarded-Proto": "https" }, "multiValueHeaders":{ 'Accept':[ "*/*" ], 'Accept-Encoding':[ "gzip, deflate" ], 'cache-control':[ "no-cache" ], 'CloudFront-Forwarded-Proto':[ "https" ], 'CloudFront-Is-Desktop-Viewer':[ "true" ], 'CloudFront-Is-Mobile-Viewer':[ "False" ], 'CloudFront-Is-SmartTV-Viewer':[ "False" ], 'CloudFront-Is-Tablet-Viewer':[ "False" ], 'CloudFront-Viewer-Country':[ "US" ], '':[ "" ], 'Content-Type':[ "application/json" ], 'headerName':[ "headerValue" ], 'Host':[ "gy415nuibc.execute-api.us-east-1.amazonaws.com" ], 'Postman-Token':[ "9f583ef0-ed83-4a38-aef3-eb9ce3f7a57f" ], 'User-Agent':[ "PostmanRuntime/2.4.5" ], 'Via':[ "1.1 d98420743a69852491bbdea73f7680bd.cloudfront.net (CloudFront)" ], 'X-Amz-Cf-Id':[ "pn-PWIJc6thYnZm5P0NMgOUglL1DYtl0gdeJky8tqsg8iS_sgsKD1A==" ], 'X-Forwarded-For':[ "54.240.196.186, 54.182.214.83" ], 'X-Forwarded-Port':[ "443" ], 'X-Forwarded-Proto':[ "https" ] }, "queryStringParameters": { "name": "me", "multivalueName": "me" }, "multiValueQueryStringParameters":{ "name":[ "me" ], "multivalueName":[ "you", "me" ] }, "pathParameters": { "proxy": "hello/world" }, "stageVariables": { "stageVariableName": "stageVariableValue" }, "requestContext": { "accountId": "12345678912", "resourceId": "roq9wj", "stage": "testStage", "requestId": "deef4878-7910-11e6-8f14-25afc3e9ae33", "identity": { "cognitoIdentityPoolId": None, "accountId": None, "cognitoIdentityId": None, "caller": None, "apiKey": None, "sourceIp": "192.168.196.186", "cognitoAuthenticationType": None, "cognitoAuthenticationProvider": None, "userArn": None, "userAgent": "PostmanRuntime/2.4.5", "user": None }, "resourcePath": "/{proxy+}", "httpMethod": "POST", "apiId": "gy415nuibc" }, "body": "{\r\n\t\"a\": 1\r\n}", "isBase64Encoded": False }
event = Event.from_dict(dummyEvent)
event
```




    Event(body='{\r\n\t"a": 1\r\n}', headers={'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'cache-control': 'no-cache', 'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'False', 'CloudFront-Is-SmartTV-Viewer': 'False', 'CloudFront-Is-Tablet-Viewer': 'False', 'CloudFront-Viewer-Country': 'US', 'Content-Type': 'application/json', 'headerName': 'headerValue', 'Host': 'gy415nuibc.execute-api.us-east-1.amazonaws.com', 'Postman-Token': '9f583ef0-ed83-4a38-aef3-eb9ce3f7a57f', 'User-Agent': 'PostmanRuntime/2.4.5', 'Via': '1.1 d98420743a69852491bbdea73f7680bd.cloudfront.net (CloudFront)', 'X-Amz-Cf-Id': 'pn-PWIJc6thYnZm5P0NMgOUglL1DYtl0gdeJky8tqsg8iS_sgsKD1A==', 'X-Forwarded-For': '54.240.196.186, 54.182.214.83', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, statusCode=200)



### parsing for body

```python
Event.parseBody(dummyEvent)
```




    {'a': 1}



## creating response for lambda

```python
print(Response.returnSuccess(body={'hello':'world'}))
print(Response.returnError(message='error'))
```

    {'body': '{"hello":"world"}', 'statusCode': 200, 'headers': {}}
    {'body': '{"error":"error"}', 'statusCode': 400, 'headers': {}}


## Use in lambda function

```python
def lambda_handler(event, *args):
  # parsing event body
  body = Event.parseBody(event)
  
  
  # submitting output
  return Response.returnSuccess({'success':'true'})

lambda_handler(dummyEvent)
```




    {'body': '{"success":"true"}', 'statusCode': 200, 'headers': {}}


