import boto3
import json

from botocore.exceptions import ClientError
from credentials import get_bedrock_client


def llama(summaries):
    # Create a Bedrock Runtime client in the AWS Region of your choice.
    client = get_bedrock_client()

    # Set the model ID, e.g., Llama 3 70b Instruct.
    model_id = "arn:aws:bedrock:us-east-1:043309345392:inference-profile/us.meta.llama3-3-70b-instruct-v1:0"

    # Define the prompt for the model.
    prompt = f"""
    Based on the following paragraphs, please generate a coherent text of one or two paragraphs in Greek. 
    Your task is to connect similar or identical viewpoints, without changing the original content or introducing new ideas.
    
    Here is an example of the type of paragraph you should produce:
    Υποβλήθηκαν σχόλια που αναδεικνύουν την κρισιμότητα της κυβερνοασφάλειας ως πεδίου πολιτικής και θίγουν ζητήματα που αφορούν στη στελέχωση και τη 
    χρηματοδότηση του ν.π.δ.δ. «Εθνική Αρχή Κυβερνοασφάλειας». Τα ζητήματα της ενίσχυσης της Αρχής για την εκπλήρωση της 
    αποστολής της, της βέλτιστης οργάνωσής της και της επιχειρησιακής ικανότητάς της έχουν ληφθεί υπόψιν τόσο κατά την 
    αρχική όσο και κατά την τελική επεξεργασία των αξιολογούμενων ρυθμίσεων.
    
    Now, process the following input:
    {"\n\n".join(summaries)}
    """

    system = f"""
    You are an assistant that is meant to act is a deliberation tool and moderate online forums and debates. You are associated with the AI4Deliberation group in 
    the University of Macedonia with the sole purpose of analyzing the articles and comments that are given to you, providing ratings and summaries of debates and 
    deliberations, and synthesizing reports
    """

    # Embed the prompt in Llama 3's instruction format.
    formatted_prompt = f"""
    <|begin_of_text|>
    <|start_header_id|>system<|end_header_id|>
    {system}
    <|start_header_id|>user<|end_header_id|>
    {prompt}
    <|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """

    # Format the request payload using the model's native structure.
    native_request = {
        "prompt": formatted_prompt,
        "max_gen_len": 4096,
        "temperature": 0.5,
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        response = client.invoke_model(modelId=model_id, body=request)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

    # Decode the response body.
    model_response = json.loads(response["body"].read())

    # Extract and print the response text.
    response_text = model_response["generation"]

    return response_text

