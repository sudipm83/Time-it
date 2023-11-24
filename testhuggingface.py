
import os

import requests

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hugginfface_token"

url = "https://raw.githubusercontent.com/hwchase17/langchain/master/docs/modules/state_of_the_union.txt"
res = requests.get(url)
with open("state_of_the_union.txt", "w") as f:
    f.write(res.text)
from langchain.document_loaders import TextLoader
# document loader
loader = TextLoader('./state_of_the_union.txt')
documents = loader.load()