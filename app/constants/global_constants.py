import spacy


class GC:
    DATASET_FOLDER = "app/dataset"
    JSON_FILE = "index.json"
    DATASET_DIRECTORY_IGNORE_LIST = ["json", "py", "DS_Store"]
    INDEXEDWORDS = {}
    SPACYLEMMATIZER = spacy.load("en_core_web_sm", disable=['parser', 'ner'])
    SORTEDWORDLIST = []
