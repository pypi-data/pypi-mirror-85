from .authentication import Authentication
import requests
import json

def isLastPage(results):
    if len(results) == 0:
        return True
    if results[0]["ui"] == "NONE" and results[0]["name"] == "NO RESULTS":
        return True
    return False

def interpretSourceType(result):
    if isinstance(result, dict):
        return result["results"]
    return result

def kGreaterThanResults(k, results):
    if not k:
        return True
    return (k > len(results))

class CUI:
    def __init__(self, apikey, cui, name):
        self.apikey = apikey
        self.cui = cui
        self.name = name

    def synonyms(self):
        umls = UMLS(self.apikey)

        content_endpoint = '/content/current/CUI/'+self.cui+'/atoms'
        query = {}
        results = umls.getData(content_endpoint, query)
        synonyms = []
        for result in results:
            if result["language"] != "ENG":
                continue
            synonyms.append(result["name"])
        return synonyms

    def hasMapping(self, codeset):
        umls = UMLS(self.apikey)
        content_endpoint = '/content/current/CUI/'+self.cui+'/atoms'
        query = {'sabs': codeset}
        results = umls.getData(content_endpoint, query)
        if len(results) > 0:
            return True
        return False







class UMLS:
    def __init__(self, apikey):
        self.apikey = apikey
        self.auth = Authentication(apikey)
    def convertType(self, type):
        if type == "Term":
            return "atom"
        if type == "CUI":
            return "sourceUi"
        if type == "Code":
            return "code"


    def getData(self,content_endpoint, query, k=None):

        tgt = self.auth.gettgt()
        uri = "https://uts-ws.nlm.nih.gov/rest/"
        results = []
        page = 1

        while True:
            if not kGreaterThanResults(k, results):
                break

            ticket = self.auth.getst(tgt)
            query['pageNumber'] = page
            query['ticket'] = ticket
            r = requests.get(uri+content_endpoint,params=query)

            r.encoding = 'utf-8'
            items  = json.loads(r.text)

            if "result" not in items:
                break
            res = interpretSourceType(items["result"])
            if isLastPage(res):
                break

            results = results + res
            page = page + 1

        if not kGreaterThanResults(k,results):
            results = results[:k]
        return results

    def convertToCUI(self,results):
        res = []
        for result in results:
            res.append(CUI(self.apikey, result["ui"],result["name"]))
        return res


    def search(self, term, k=None):
        if k and not isinstance(k, int):
            raise Exception("k needs to be an integer...")
        query = {'string':term}
        search_endpoint = "/search/current"
        results = self.getData(search_endpoint, query, k)
        return self.convertToCUI(results)




###
