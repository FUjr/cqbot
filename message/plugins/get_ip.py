from .xdbSearcher import XdbSearcher
class get_ip():
    def __init__(self,dbPath = "../../data/ip2region.xdb") -> None:
        dbPath = dbPath
        vi = XdbSearcher.loadVectorIndexFromFile(dbfile=dbPath)
        self.searcher = XdbSearcher(dbfile=dbPath, vectorIndex=vi)
        pass
    
    def get_ip(self,ip):
        region_str = self.searcher.search(ip)
        return region_str
    
    def close(self):
        self.searcher.close()
        pass
        