from bs4 import BeautifulSoup
import re
from py_mini_racer import py_mini_racer

class GS_CDATA_decoder:
    def __init__(self, data=None, soup=None):
        if data is None and soup is None and not (data is not None and soup is not None):
            raise ValueError("You must input data or soup!")
        if data:
            soup = BeautifulSoup(data, "html.parser")
        cdata = soup.find(text=re.compile("CDATA"))
        raw_cdata = str(cdata)
        matches = re.search(r"<!\[CDATA\[\n(.*)\n\/\/\]\]>", raw_cdata)
        if len(matches.groups()) != 1:
            raise ValueError("Could not extract CDATA!")
        js = matches[1]
        self.ctx = py_mini_racer.MiniRacer()
        self.ctx.eval("window={};gon={};")
        self.ctx.eval(js)
    
    def extract(self, query: str):
        return self.ctx.eval(query)
    
    def get_gon(self) -> dict:
        return self.extract("gon")

if __name__ == "__main__":
    with open("out.html", "rb") as f:
        d = f.read()
    decoder = GS_CDATA_decoder(d)
    import IPython
    IPython.embed()
