import queue
import requests
import yaml

ELEM = {'h':1,'d':1, 't':1, 'he':2, 'li':3, 'be':4, 'b':5, 'c':6, 'n':7, 'o':8,
        'f':9, 'ne':10, 'na':11, 'mg':12, 'al':13, 'si':14, 'p':15, 's':16,
        'cl':17, 'ar':18, 'k':19, 'ca':20, 'sc':21, 'ti':22, 'v':23, 'cr':24,
        'mn':25, 'fe':26, 'co':27, 'ni':28, 'cu':29, 'zn':30, 'ga':31, 'ge':32,
        'as':33, 'se':34, 'br':35, 'kr':36, 'rb':37, 'sr':38, 'y':39, 'zr':40,
        'nb':41, 'mo':42, 'tc':43, 'ru':44, 'rh':45, 'pd':46, 'ag':47, 'cd':48,
        'in':49, 'sn':50, 'sb':51, 'te':52, 'i':53, 'xe':54, 'cs':55, 'ba':56, 
        'la':57, 'ce':58, 'pr':59, 'nd':60, 'pm':61, 'sm':62, 'eu':63, 'gd':64,
        'tb':65, 'dy':66, 'ho':67, 'er':68, 'tm':69, 'yb':70, 'lu':71, 'hf':72,
        'ta':73, 'w':74, 're':75, 'os':76, 'ir':77, 'pt':78, 'au':79, 'hg':80, 
        'tl':81, 'pb':82, 'bi':83, 'po':84, 'at':85, 'rn':86, 'fr':87, 'ra':88,
        'ac':89, 'th':90, 'pa':91, 'u':92, 'np':93, 'pu':94, 'am':95, 'cm':96,
        'bk':97, 'cf':98, 'es':99, 'fm':100, 'md':101, 'no':102, 'lr':103,
        'rf':104, 'db':105, 'sg':106, 'bh':107, 'hs':108, 'mt':109, 'ds':110,
        'rg':111, 'cn':112, 'uut':113, 'uuq':114, 'uup':115, 'uuh':116,
        'nh':117, 'og':118} 


def _parse_text_bfs(txt):
    visited, q = set(), queue.Queue()
    q.put((txt,[]))
    while not q.empty():
        val = q.get()
        if val[0] == '':
            return val
        for key in ELEM:
            if val[0].startswith(key) and val[0][len(key):] not in visited:
                visited.add(val[0][len(key):])
                q.put((val[0][len(key):],val[1]+[key])) 
    return None

def parse_text(txt):
    txt = txt.replace(' ', '')
    txt = txt.lower()
    return _parse_text_bfs(txt)

def generate():
    word_site = ("http://svnweb.freebsd.org/csrg/share/dict/words?view=co&"
                 "content-type=text/plain")
    response = requests.get(word_site)
    WORDS = response.content.splitlines()
    with open("word_dict.yaml", 'r') as yaml_file:
        details = yaml.load(yaml_file)
        details['prec'] = {}
        for word in WORDS:
            word = word.decode('utf-8')
            ans = parse_text(word)
            if ans != None:
                details['prec'][word] = (len(ans[1]), ans[1])
            else:
                details['prec'][word] = None

    with open('word_dict.yaml', 'w') as outfile:
        outfile.write( yaml.dump(details, default_flow_style=False))

def check_word(txt):
    txt = txt.replace(  

if __name__ == '__main__':
    generate()
    # print(parse_text('Nonrepresentationalisms')[1])


