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

with open("./discord_dumps/help_channel_dump_06_02_23.json", "r") as f:
    data = json.load(f)

with open("conversation_docs.json", "r") as f:
    threads = json.load(f)
print("Thread keys: ", threads[0].keys(), "\n")
print(threads[0]["metadata"], "\n")
print(threads[0]["thread"], "\n")

# create document objects using doc_id's and dates from each thread
new_documents = []
for thread in threads:
    thread_text = thread["thread"]
    thread_id = thread["metadata"]["id"]
    timestamp = thread["metadata"]["timestamp"]
    new_documents.append(
        Document(text=thread_text, id_=thread_id, metadata={"date": timestamp})
    )
"""
The below will actually show 0 because this main.py program ran everything from the beginning
and because the python script to create threads overwrites the conversation_docs.json
file on every run, the 'new_documents' and 'documents' were created from the most updated
conversation_docs.json, on my latest run 
Regardless, at this point we can see that there's 13 docs yet to be ingested
based on this output:

-------------------------------------
number of input documents:  780
Double check ref_docs ingested:  767
-------------------------------------

We don't have this problem with the jupiter notebook because you can run segments of code using it, i.e., not the 
entire file every time. 

"""
print("Number of new documents: ", len(new_documents) - len(documents))

# now refresh!
refreshed_docs = index.refresh(
    new_documents,
    update_kwargs={"delete_kwargs": {'delete_from_docstore': True}}
)

print("Number of newly inserted/refreshed docs: ", sum(refreshed_docs))

index.storage_context.persist(persist_dir="./storage")

# TO DO: Understand how the refresh() function was able to not only add 13 more documents, but also overwrite and update 2 
# additional documents. Because
# new_documents - documents == 13 (supposed to be, in jupiter notebook)
# Number of newly inserted/refreshed docs:  15
# it's explained at the very end of the tutorial video