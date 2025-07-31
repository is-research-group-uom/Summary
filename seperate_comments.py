from langchain_aws import ChatBedrock
from credentials import get_bedrock_client

def calculate_tokens(comments):
    batches = []
    batch = []
    all_tokens = 0

    client = get_bedrock_client()

    llm = ChatBedrock(
        client=client,
        model_id="us.anthropic.claude-3-5-sonnet-20240620-v1:0",
        model_kwargs={"temperature": 0, "max_tokens": 131072},
    )

    for comment in comments[:30]:
        tokens = llm.get_num_tokens(comment)
        print('Tokens: ', tokens)
        if all_tokens + tokens <= 10000:
            all_tokens += tokens
            batch.append(comment)
        else:
            batches.append(batch)
            batch = [comment]
            all_tokens = tokens

    if batch:
        batches.append(batch)

    return batches


def get_tokens(summaries):
    client = get_bedrock_client()

    llm = ChatBedrock(
        client=client,
        model_id="us.anthropic.claude-3-5-sonnet-20240620-v1:0",
        model_kwargs={"temperature": 0, "max_tokens": 131072},
    )

    tokens = 0
    for summary in summaries:
        tokens += llm.get_num_tokens(summary)

    return tokens
