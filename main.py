from ArticleExtraction import scrape_post_urls, scrape_post_content
import pandas as pd
import re
from relevance.relevance_claude import relevance_claude
from seperate_comments import calculate_tokens, get_tokens
from llms.claude3_5 import claude3_5
from llms.llama_30b import llama
from llms.deepseek_r1 import deepseek

url = "https://www.opengov.gr/yyka/?p=4433"  # Replace with the target URL
post_contents = scrape_post_urls(url)
if post_contents:
    for i, content in enumerate(post_contents, 1):
        if 'links' in content:
            print(f"Links from consnav (set {i}): {content['links']}\n")

content_posts = []
title_posts = []
posts = []
for i, content in enumerate(post_contents):
    for link in content['links']:
        url = f'{link}'
        print(link)
        post_content, post_title = scrape_post_content(url)

        dict = {
            "Title": post_title,
            "Content": post_content
        }

        posts.append(dict)

print(f'Scrapted Content posts: {posts}')


dataframe1 = pd.read_excel('data/yyka_comments_54.xls')

comments_per_article = dataframe1.values.tolist()
article_comment = []

for post in posts:
    comments = []
    comment_from_article = re.sub(r"\s*[-–]\s*", " ", post['Title'][0])
    for comment in comments_per_article:
        comment_from_excel = re.sub(r"\s*[-–]\s*", " ", comment[0])
        if comment_from_excel == comment_from_article:
            # print(f'comments for article {comment_from_excel} and {comment_from_article}')
            comments.append(comment[1])
    dict = {
        "Title": post['Title'][0],
        "Content": post['Content'][0],
        "Comments": comments
    }

    article_comment.append(dict)

index = 0
for idx, article in enumerate(article_comment):
    index += 1
    article_with_title = article['Title'] + '\n' + article['Content']

    comments = article['Comments']
    # print(f'Comments1: {comments}')
    print(f'Length1: {len(comments)}')
    for comment in comments[:30]:
        response = relevance_claude(article_with_title, comment)

        score = int(response)
        if score < 50:
            comments.remove(comment)
    # print(f'Comments2: {comments}')
    print(f'Length2: {len(comments)}')

    batches = calculate_tokens(comments)

    print('Article: ', len(batches))
    for index, batch in enumerate(batches):
        print(f"{index+1} Batch: {len(batch)}\n-------------\n")

    if len(batches) > 0:
        summaries = claude3_5(batches)
        generated_tokens = get_tokens(summaries)
        print(f"Tokens for summary: {generated_tokens}")

        print(f"Summaries of {idx+1} article:\n{"\n----------------\n\n".join(summaries)}")

    with open(f"outputs/article{idx+1}.txt", "w", encoding="utf-8") as f:
        f.write(llama(summaries))

    if len(comments) > 0:
        summary = claude3_5(comments)
        print(summary)

