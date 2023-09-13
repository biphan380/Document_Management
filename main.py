# NOTE: follow the jupiter notebook file for complete context and instructions. 
# This main file excludes many of the instructional steps
# that are shown in the jupiter notebook
import json
import os

with open("./discord_dumps/help_channel_dump_05_25_23.json", "r") as f:
    data = json.load(f)

with open("conversation_docs.json", "r") as f:
    threads = json.load(f)

from llama_index import Document

# create document objects using doc_ids and dates from each thread
documents = []
for thread in threads:
    thread_text = thread["thread"]
    thread_id = thread["metadata"]["id"]
    timestamp = thread["metadata"]["timestamp"]
    documents.append(
        Document(text=thread_text, id_=thread_id, metadata={"date": timestamp})
    )

from llama_index import VectorStoreIndex

# This is saved in-memory (RAM) and not persisted to disk at this time
# index = VectorStoreIndex.from_documents(documents)

# print("ref_docs ingested: ", len(index.ref_doc_info))
print("number of input documents: ", len(documents))

thread_id = threads[0]["metadata"]["id"]
# print(index.ref_doc_info[thread_id])

# We persist to disk
# index.storage_context.persist(persist_dir="./storage")

# We can now freely load from disk
from llama_index import StorageContext, load_index_from_storage
index = load_index_from_storage(StorageContext.from_defaults(persist_dir="./storage"))

print('Double check ref_docs ingested: ', len(index.ref_doc_info))