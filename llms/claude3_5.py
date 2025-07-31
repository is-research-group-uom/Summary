import json
from botocore.exceptions import ClientError
from credentials import get_bedrock_client


def claude3_5(batches):
    # Create an Amazon Bedrock Runtime client.
    brt = get_bedrock_client()

    # Set the model ID
    model_id = "us.anthropic.claude-3-5-sonnet-20240620-v1:0"
    summaries = []

    for batch in batches:
        prompt = f"""
        As a professional summarizer, create a concise and comprehensive summary of the provided text, be it an article, post, conversation, or passage, while 
        adhering to these guidelines:
        
        1. Craft a summary that is detailed, thorough, in-depth, and complex, while maintaining clarity and conciseness.
        2. Incorporate main ideas and essential information, eliminating extraneous language and focusing on critical aspects.
        3. Rely strictly on the provided text, without including external information.
        4. Format the summary in paragraph form for easy understanding.
        5. Conclude your notes with [End of Notes, Message #X] to indicate completion, where "X" represents the total number of messages that I have sent. In other words, include a message counter where you start with #1 and add 1 to the message counter every time I send a message.
        6. The Summary MUST be in greek.
        
        By following this optimized prompt, you will generate an effective summary that encapsulates the essence of the given text in a clear, concise, and 
        reader-friendly manner.
        
        Comments:
        {"\n\n".join(batch)}
        """

        # Format the request payload (back to simple text)
        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 131072,
            "top_k": 250,
            "stop_sequences": [],
            "temperature": 0.7,
            "top_p": 0.999,
            "system": f"""You are an assistant that is meant to act is a deliberation tool and moderate online forums and debates. 
            You are associated with the AI4Deliberation group in the University of Macedonia with the sole purpose of analyzing the articles and comments that are given
            to you, providing ratings and summaries of debates and deliberations, and synthesizing reports""",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        # Convert the native request to JSON
        request = json.dumps(native_request)

        try:
            # Invoke the model with the request
            response = brt.invoke_model(modelId=model_id, body=request)

        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
            exit(1)

        # Decode the response body
        model_response = json.loads(response["body"].read())

        # Extract and print the response text
        response_text = model_response['content'][0]['text']
        summaries.append(response_text)

    return summaries
