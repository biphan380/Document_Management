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
    thread_text = thread['thread']
    thread_id = thread['metadata']['id']
    timestampe = thread['metadata']['timestamp']
    documents.append(Document(thread_text, doc_id=thread_id, extra_info={'date': timestampe}))