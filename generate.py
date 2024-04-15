from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
#from langchain.prompts import PromptTemplate
import chardet
import re
import os

OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')

def generate_text(user_text):
    # テキスト読み込み
    with open('pokedan.txt', 'rb') as file:
        rawdata = file.read()
        result = chardet.detect(rawdata)
    encoding = result['encoding']
    with open('pokedan.txt', 'r', encoding=encoding) as file:
        lines = file.readlines()
    sentence_list = []
    texts = [] # チャンクのまとまり
    paragraph = "" # チャンク
    for line in lines:
        # 開業まで同じ塊
        if line == "\n":
            texts.append(paragraph)
            paragraph = ""
        else:
            line = line.strip()
            sentences = re.split(r'[。！？]', line)
            for sentence in sentences:
                sentence_list.append(sentence)
            paragraph += line
    # ベクトルデータベースの作成
    docsearch = FAISS.from_texts(
        texts=texts,  # チャンクの配列
        embedding=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)  # 埋め込み
    )
    #prompt_template = """Use the following pieces of context ... Answer in Japanese:"""
    #PROMPT = PromptTemplate(
    #template=prompt_template, input_variables=["context", "question"]
    #)
    # 質問応答チェーンの作成 AIを作った
    qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY),
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        #chain_type_kwargs={"prompt": PROMPT}
    )
    system_text = str(qa_chain.run(user_text))
    
    return system_text