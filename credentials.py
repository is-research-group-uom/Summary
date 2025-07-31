AWS_CREDENTIALS ={
    'aws_access_key_id':'ASIAQUFLQFJYL4AGPUMJ',
    'aws_secret_access_key':'BcWyQWOQt8hEbcN9bVVjAPzxl24F6ru/BbxuvJi2',
    'aws_session_token':'IQoJb3JpZ2luX2VjEKn//////////wEaDGV1LWNlbnRyYWwtMSJIMEYCIQCv5Rt9JeaJHg9JA401tiEJRK6OeMUKUtzBPRKURKWRhwIhALOJenAqAI62M0adHJuWyiPeonA6LFtJLQcSB6CtAj+WKu4CCNL//////////wEQABoMMDQzMzA5MzQ1MzkyIgx4T/ulo3vaOBiEkFAqwgIO7dq2CNUY3OVymTiIsF1V1//fko+uZSIjA9zgT4q3cmw7gVkbidNCxJZ5VSNOEiW5wNPrtzn/nhcIKlBo+uJsGlRQHdnpFC8pCIfjZe0ZhGzttp570grEUL/hIiSJT/qjgc3NJGULJAvfrYwyiu0+KKaH8nrdDhr65abOz7E4KnCRXIxLDgy0TCXlWUClESw12gfE7HHE3g0xjG0BaT6YKbpT1Div0shkQcL+rUwtqawSI7yplViZ0yyT0Z3X2RCVWdsc4A0XXAJqOBjDv/TwVzODTFHVdJwdiGJAQYO/F22PKbah0YA5fbJh8ZsychVRZ6USvr8B5ICzlmVB5rpTE6ciRoadZWWaHxrgfXRS0BRQbVGL6LUT93aY+TK3ot6ZHIUKXLPaPDJZpQfiLn2neQVA5SF9GZbhWK0/rOB95F89MK/qrMQGOqYBPTTFY4GrGQfKigcah2JWJq3Ahmg/+0wxsHyKqhsQtEEOT8luqeKJnHmcn6JN8+GgUC2gQi/Asy5IJASKB0WtTL89/C5Ue5bAqiUiylurQVRrQwqCO2qGW5mgbrLqpcZ8eL5ULPBxtbPENpVBitFzpKQk1sTM/hBJlO4VZPRMp7Za8OiFIeuiZXp90l5HnqFOdv8bg1zgjoY8P5W7hbVxoesW35x4cw==',
    'region_name':'us-east-1'
}

def get_bedrock_client():
    """
    Returns a configured boto3 bedrock-runtime client using the stored credentials.

    Returns:
        boto3.client: Configured bedrock-runtime client
    """
    import boto3

    return boto3.client('bedrock-runtime', **AWS_CREDENTIALS)

def get_credentials():
    """
    Returns the AWS credentials dictionary.

    Returns:
        dict: AWS credentials
    """
    return AWS_CREDENTIALS.copy()