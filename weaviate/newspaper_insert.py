import os

import weaviate
from weaviate.classes.init import Auth

weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
cohere_api_key = os.environ["COHERE_APIKEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key),
    headers={"X-Cohere-Api-Key": cohere_api_key},
)

try:
    newspaper = client.collections.use("Newspaper")

    articles=[{
            "media_name": "The Washington Post",
            "title": "Jimmy Kimmel had to answer to the FCC. Internet comedians answer to the algorithm.",
            "description": "Jimmy Kimmel had to answer to the FCC. Internet comedians answer to the algorithm.",
            "author": "Tatum Hunter",
            "date": "2025-09-27T16:05:57Z",
            "language": "en",
            "categories": ["television", "technology", "politics"],
            "newspaper_link": "https://www.washingtonpost.com/technology/2025/09/27/jimmy-kimmel-had-answer-fcc-internet-comedians-answer-algorithm/",
            "rss_link": "https://feeds.washingtonpost.com/rss/business/technology?itid=lk_inline_manual_23",
            "rss_last_build": "2025-09-27T16:05:57Z",
            "content": 
            """
            As the nation debated whether Jimmy Kimmel’s comments following the killing of Charlie Kirk were appropriate — remarks that got him temporarily kicked off the air — a new generation of comedians online had no problem going there.
            “I don’t want to talk about it. I don’t want to talk about it. I don’t want to talk about it,” comedian Jay Jurden joked in a clip broadcast to his 211,000 Instagram followers. “I’m going to talk about it.”
            Comedy is in the spotlight since late-night host Kimmel was suspended — then reinstated this week — after he angered some Kirk supporters when he said that the “MAGA gang” was “desperately trying to characterize this kid who murdered Charlie Kirk as anything other than one of them.” He was referring to the accused killer, Tyler Robinson, who was said to have grown up in a Republican household before, according to his family, he leaned more left. Critics said Kimmel’s removal, which came after threats from the Federal Communications Commission chairman, was censoring free speech.
            """
    },{
            "media_name": "Reuters",
            "title": "Global markets rally",
            "description": "Stocks rose worldwide on news of economic recovery.",
            "author": "John Smith",
            "date": "2025-09-27T19:10:00Z",
            "language": "en",
            "categories": ["economy", "finance"],
            "newspaper_link": "https://www.reuters.com/markets/global-markets-rally",
            "rss_link": "https://www.reutersagency.com/feed/?best-topics=top-news",
            "rss_last_build": "2025-09-27T19:10:00Z",
            "content": "Stocks rose globally as investors reacted to stronger-than-expected economic reports."
}]
        
    with newspaper.batch.dynamic() as batch:
        for data_row in articles:
            batch.add_object(
                properties=data_row,
            )
            if batch.number_errors > 10:
                print("Batch import stopped due to excessive errors.")
                break
        

    print(articles)

except Exception as e:
    print(f"This is our error: {e}")

finally:
    client.close()