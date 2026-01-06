from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(file_path="./IndexesRAG/DocumentLoaders/sci-fi.pdf")

docs = loader.load()
text = """ Christopher Nolan is one of the most influential and distinctive filmmakers of the 21st century, known for blending complex storytelling with large-scale cinematic spectacle. Born in London in 1970, Nolan developed an early interest in filmmaking and went on to study English literature at University College London, where he began making short films that reflected his fascination with time, memory, and perception.

        Nolan first gained international attention with Memento (2000), a psychological thriller told in a non-linear narrative structure that forces the audience to experience the story in the same fragmented way as its protagonist. This film established many of the themes that would later become central to Nolan’s work: unreliable memory, subjective reality, and the manipulation of time.

        He achieved mainstream success with The Dark Knight Trilogy (2005–2012), which redefined the superhero genre by grounding it in realism, moral ambiguity, and complex character development. The Dark Knight in particular is often regarded as one of the greatest superhero films ever made due to its mature themes and memorable antagonist, the Joker.
"""


splitter = RecursiveCharacterTextSplitter(
    chunk_size= 420,
    chunk_overlap= 0
)

# it uses this separators default for splitting -> separators=["\n\n", "\n", " ", ""] 
# 1st it try with `\n\n` means on paragraph basis and then 2nd \n on line basis then 3rd " " on word basis and then 4th "" character basis 
# this is for texts
result_text = splitter.split_text(text)
# this is for documents
result_docs = splitter.split_documents(documents=docs)

print(len(result_text))
print(result_text)
# print(result_docs[0].page_content)