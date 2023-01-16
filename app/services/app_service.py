from operator import index
from os import listdir
from os.path import isfile, join
import os
from langcodes import closest_match
from app.constants.global_constants import GC
import json
import spacy

from app.services.response_service import ResponseService
spacy.prefer_gpu()


class AppService:

    # Already Indexed? Should index?
    def isIndexed(self, first=True) -> bool:

        actual_file_list = self.getFilesInDirectory(
            os.path.join(os.getcwd(), GC.DATASET_FOLDER))

        index_file_file_list = GC.INDEXEDWORDS.get("files", None)

        if not index_file_file_list and first:
            self.indexFiles()
            return self.isIndexed(False)
        elif not index_file_file_list:
            return False

        self.removeIgnoredFiles(actual_file_list)

        areArraysSame = self.areArraysSame(
            actual_file_list, index_file_file_list)

        if not areArraysSame and first:
            self.indexFiles()
            return self.isIndexed(False)
        elif not areArraysSame and not first:
            return False

        return True

# Preprocessing function
    def indexFiles(self):

        indexDictionary = {}
        # lemmatizer = spacy.load("en_core_web_sm", disable=['parser', 'ner'])

        files_list = self.getFilesInDirectory(
            os.path.join(os.getcwd(), GC.DATASET_FOLDER))

        # print(files_list)

        self.removeIgnoredFiles(files_list)

        files_dictionary = {}
        ctr = 0
        for file in files_list:
            files_dictionary[file] = ctr
            ctr += 1

        indexDictionary["files"] = files_list

        indexDictionary["index"] = {}

        for file in files_list:

            # print(file)
            with open(os.path.join(os.path.join(os.getcwd(), GC.DATASET_FOLDER), file), 'r+') as f:
                lineNumber = 0
                for line in f:
                    lineNumber += 1
                    if not line:
                        continue

                    lemmatized_line = GC.SPACYLEMMATIZER(line)
                    for words in lemmatized_line:
                        if words.lemma_ not in indexDictionary["index"]:
                            d = {}
                            d[files_dictionary[file]] = {}
                            d[files_dictionary[file]]["occurrence"] = [lineNumber]
                            indexDictionary["index"][words.lemma_] = d
                        else:
                            d = indexDictionary["index"][words.lemma_]
                            if files_dictionary[file] not in d:
                                d[files_dictionary[file]] = {}
                                d[files_dictionary[file]]["occurrence"] = [
                                    lineNumber]
                            else:
                                d[files_dictionary[file]]["occurrence"].append(
                                    lineNumber)
                            indexDictionary["index"][words.lemma_] = d

        GC.INDEXEDWORDS = indexDictionary
        self.computeSortedWordList()
        self.writeToFile()

    # Given a word, Return the words Occurrences

    @staticmethod
    def writeToFile():
        index_file_path = os.path.join(os.path.join(
            os.getcwd(), GC.DATASET_FOLDER), GC.JSON_FILE)

        mode = 'w+'
        with open(index_file_path, mode) as idxfile:
            try:
                json.dump(GC.INDEXEDWORDS, idxfile)
            except:
                print("ERROR WRITING")

            idxfile.close()

    def searchWord(self, word, first=True):

        if first and not GC.INDEXEDWORDS and not self.isIndexed():
            self.isIndexed()
            return self.searchWord(word, False)

        if word not in GC.INDEXEDWORDS["index"]:
            # Perform Binary Search and Return the closest
            print("NOT IN THE DICT")
            closest_word = self.searchClosestWord(word)

            print("CLOSEST WORD", closest_word)

            return ResponseService().create_response(closest_word, 0)

        if not first and not GC.INDEXEDWORDS and not self.isIndexed():
            return ResponseService().create_empty_response()

        return ResponseService().create_response(word)

    def searchClosestWord(self, word, first=True):
        if not GC.SORTEDWORDLIST:
            self.computeSortedWordList()
            return self.searchClosestWord(word, False)

        if not first and not GC.SORTEDWORDLIST:
            return ResponseService().create_empty_response()

        low = 0

        high = len(GC.SORTEDWORDLIST) - 1

        closest_word = self.binarySearch(low, high, word)

        return closest_word

    @staticmethod
    def binarySearch(low, high, word):
        mid = -1
        while(low < high):
            mid = (low + high)//2
            midpoint = GC.SORTEDWORDLIST[mid]
            if midpoint > word:
                high = mid - 1
            elif midpoint < word:
                low = mid + 1
            else:
                break

        return GC.SORTEDWORDLIST[mid]

    @staticmethod
    def getFilesInDirectory(path):
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        return onlyfiles

    @staticmethod
    def computeSortedWordList():
        if GC.INDEXEDWORDS:
            index = list(sorted(GC.INDEXEDWORDS["index"].keys()))
            GC.SORTEDWORDLIST = index

    @staticmethod
    def removeIgnoredFiles(listOfFiles):
        for file in listOfFiles:
            print(file, file.split(".")[-1])
            if file.split(".")[-1] in GC.DATASET_DIRECTORY_IGNORE_LIST:
                listOfFiles.remove(file)

    # Array 1 -> Freshly Computed File List
    # Array 2 -> Existing File List

    @staticmethod
    def areArraysSame(array1, array2):
        return list(set(array1) - set(array2)) == None
