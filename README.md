# Summary
A basic template for generating summaries from user comments. Summaries are created using prompts sent to LLMs hosted on AWS Bedrock. The data source is [OpenGov](https://www.opengov.gr/home/)

#### LLM used
1. Claude 3.5
2. Llama 3.3 70b
3. Deepseek R1

#### Pipeline 
1. Retrieve the article title, content, and comments from the selected deliberation.
2. For the chosen deliberation, create a dictionary for each article containing:
   - `title`
   - `content`
   - `comments`
3. Evaluate each comment for relevance to the article. Irrelevant comments are removed.
4. For each article, split the remaining comments into batches.
   - Token count for each batch is limited to under 10,000, measured using `langchain_aws`.
5. Send each batch to the LLM to generate a bullet-point summary.
6. Combine all bullet-point summaries into a cohesive full-text summary.

#### Evaluation
No evaluation has been conducted yet, but planned metrics include:
1. BLUE
2. BERTscore
3. METEOR
4. ROUGE
5. Maybe G-Eval
