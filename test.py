import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure, Property, DataType, VectorDistances, VectorFilterStrategy, Tokenization
import os

# ----- Client & auth -----
weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
cohere_api_key = os.environ["COHERE_APIKEY"]

try:
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=Auth.api_key(weaviate_api_key),
        headers={"X-Cohere-Api-Key": cohere_api_key},
    )

    client.collections.create(
        "Newspaper",
        vector_config=Configure.Vectors.text2vec_weaviate(
            name="default",
            vector_index_config=Configure.VectorIndex.hnsw(
                ef_construction=300,
                distance_metric=VectorDistances.COSINE,
                filter_strategy=VectorFilterStrategy.SWEEPING
            )
        ),
        reranker_config=Configure.Reranker.cohere(),
        generative_config=Configure.Generative.cohere(),
        properties=[
            Property(name="media_name", description="Name of the media company (i.e. 'The Washington Post')", index_filterable=True, index_searchable=True, data_type=DataType.TEXT, skip_vectorization=True),
            Property(name="title", description="Title of the article", data_type=DataType.TEXT, skip_vectorization=True),
            Property(name="description", description="Overview of the article", index_filterable=True, index_searchable=True, data_type=DataType.TEXT, skip_vectorization=True),
            Property(name="author", description="Author of the article", data_type=DataType.TEXT, skip_vectorization=True),
            Property(name="date", description="Date of the article", data_type=DataType.DATE, skip_vectorization=True),
            Property(name="language", description="Language of the article", data_type=DataType.TEXT, skip_vectorization=True),
            Property(name="categories", description="The categories the article belongs to", data_type=DataType.TEXT_ARRAY, skip_vectorization=True),
            Property(name="newspaper_link", description="The hyperlink of the article", data_type=DataType.TEXT, skip_vectorization=True),
            Property(name="rss_link", description="The hyperlink of the rss", data_type=DataType.TEXT, skip_vectorization=True),
            Property(name="rss_last_build", description="Date of the rss' last build", data_type=DataType.DATE, skip_vectorization=True),
            Property(name="content", description="Content of the article", data_type=DataType.TEXT, index_filterable=True, index_searchable=True, tokenization=Tokenization.LOWERCASE),
        ],
    )
    pass

except Exception as e:
    print(f"This is the error: {e}")

finally:
    client.close()