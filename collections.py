import os
import math
PATH = os.getcwd() + "\\collection"
S = 0.75

class Collection:
    def __init__(self):
        self.setup()

    def setup(self):
        if not os.path.isdir(PATH):
            os.mkdir(PATH)
        self.getDocuments()
        self.createCollection()
        

    def getDocuments(self):
        self.documents = os.listdir(PATH)
        self.doc_num = len(os.listdir(PATH))

    def getDocumentTerms(self,filename):
        """
        Returns a dictionary of every word in the document mapped to how many times that word occurs
        Args:
            (str)  -> name of the file to read
        Returns:
            (dict) -> map of every word in the document & their number of occurences
            (int)  -> representing the number of terms in the document
        """
        file = open(PATH+"\\"+filename,"r") 
        words = {}
        docLen = 0
        for line in file:
            for word in line.split():
                word = word.strip('.,?!)("') #removes all special characters from each word
                word = word.strip("'")
                word = word.lower() #converts all words to lower case
                if word not in words.keys():
                    words[word] = 1
                else:
                    words[word] += 1
                docLen+=1
        return words, docLen

    def createCollection(self):
        """
        Creates a dictionary for each document in the collection
        """
        collection = {}
        total = 0
        for doc in self.documents:
            collection[doc] = {}
            collection[doc]["terms"], collection[doc]["length"] = self.getDocumentTerms(doc)
            total += collection[doc]["length"] 
        self.collection = collection
        if total > 0:
            self.avg_doc_len = total/self.doc_num
        else:
            self.avg_doc_len = 0

    def printCollection(self):
        """
        Parameters      : None
        Returns         : None
        """
        print("[Printing Collection]")
        for key in self.collection.keys():
            print(f"{key}:\n\t{self.collection[key]}")
            print("")
        print(f"[AVG DOC LENGH:] = {self.avg_doc_len}")

    def getTermFreq(self,doc,term):
        """
        Returns how many time a word occurs in a document
        Returns -1 if a word does not occur in the document
        Args:
            (dict)  -> name of the document to read
        Returns:
            (int)  -> Number of times a word occurs in a document
        """
        if term.lower() in self.collection[doc]["terms"].keys():
            return self.collection[doc]["terms"][term.lower()]
        else:
            return 0

    def getDocFreq(self,term):
        doc_freq = 0
        for doc in self.collection.keys():
            if term.lower() in self.collection[doc]["terms"].keys():
                doc_freq += 1
        return doc_freq

    def getQueryFreq(self,query):
        q_list = query.split()
        q_freq = {}
        for term in q_list:
            q_freq[term] = self.getDocFreq(term)
        return q_freq

    def getTermIDF(self, term):
        if self.getDocFreq(term) > 0:
            #print(f"{term}: log({self.doc_num+1}/{self.getDocFreq(term)})")
            return math.log10((self.doc_num+1)/self.getDocFreq(term))
        else:
            return 0
    
    def getQueryIDF(self, query):
        q_list = query.split()
        q_freq = {}
        for term in q_list:
            q_freq[term] = self.getTermIDF(term)
        return q_freq

    def getDocSimilarity(self,doc, query):
        q_freq = self.getQueryFreq(query)
        q_idf  = self.getQueryIDF(query)
        score = 0
        for term in q_freq.keys():
            #print(self.getTermFreq(doc,term), q_freq[term], q_idf[term])
            score += self.getTermFreq(doc,term) * q_freq[term] * q_idf[term]
        return score
    
    def getCollectionSimilarity(self,query):
        scores = {}
        for doc in self.collection.keys():
            scores[doc] = self.getDocSimilarity(doc,query)
        return scores

    def getQueryTermCount(self,query, term):
        q_list = query.split()
        count = 0
        for t in q_list:
            if t == term:
                count+=1
        return count

    def getPNScore(self,doc, query):
        q_list = query.split()
        score = 0
        for term in q_list:
            if self.getTermFreq(doc,term) > 0:
                tf_weight = 1 + math.log10(1+ math.log10(self.getTermFreq(doc, term)))
                len_norm = (1-S) + S * (self.collection[doc]["length"]/self.avg_doc_len)
                idf_weight = self.getQueryTermCount(query, term) * self.getTermIDF(term)
                score += (tf_weight * idf_weight) / len_norm
            else:
                score += 0
        return score

    def getPNScores(self, query):
        scores = {}
        for doc in self.collection.keys():
            scores[doc] = self.getPNScore(doc,query)
        return scores

    def __str__(self):
        return f"Docs in collection: {self.documents}\nAverage DocLength: {self.avg_doc_len}"

if __name__ == "__main__":
    collection = Collection()
    print(collection)
    #print(collection.getCollectionSimilarity("shrek"))
    collection.printCollection()
    done = False
    while(not done):
        inp = input("Enter a query: ")
        if inp == "-1":
            done = True
        else:
            print(collection.getPNScores(inp))