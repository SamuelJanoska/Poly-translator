from flask import Flask, request, render_template, jsonify

from urllib.request import urlopen
import requests
import threading
import json

from contextlib import suppress

app = Flask(__name__)



@app.route('/')
def hello():
    return render_template("languagesIndex.html")

    
@app.route('/response', methods=['POST'])
def response():

    a_dictionary = {}
    
    inpLang = request.form.get("inpLang")
    keyword = request.form.get("keyword")
    target = request.form.get("outLang1")
    try:
        outLang2 = request.form.get("outLang2")
    except:
        pass
    try:
        outLang3 = request.form.get("outLang3")
    except:
        pass
    try:
        outLang4 = request.form.get("outLang4")
    except:
        pass
    try:
        outLang5 = request.form.get("outLang5")
    except:
        pass
    #target="es"
    langList = []
    translatedList=[]
    #langList.append(keyword)
    langList.append(target)
    with suppress(Exception):
        langList.append(outLang2)
    with suppress(Exception):
        langList.append(outLang3)
    with suppress(Exception): 
        langList.append(outLang4)
    with suppress(Exception):        
        langList.append(outLang5)
    print(langList)
        

    for targetLang in langList:
        API_ENDPOINT = "https://libretranslate.com/translate"
        API_ENDPOINT = "https://translate.argosopentech.com/translate"
        #API_ENDPOINT = "https://libretranslate.de/translate"
        #API_KEY = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        API_KEY = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        data = {'api_dev_key':API_KEY,
                'accept':'application/json',
                'Content-Type:':'application/x-www-form-urlencoded',
                'api_paste_format':'python',
                'q':keyword,
                'source':inpLang,
                'target':targetLang}
        r = requests.post(url = API_ENDPOINT, data = data)
        pastebin_url = r.text

        res = {}
        #print (pastebin_url)
        res = pastebin_url.split(':')
        res2 = res[1].split('"')
        res3 = res2[1].split('.')
        print (res3[0]) 
        translated=res3[0]
        if not translated=="Invalid request":
            translatedList.append(translated)
        
        #print(inpLang, keyword)


    for item in langList:
        if item == None:
            langList.remove(None)
            # possible mistake might occur here
            translatedList.remove('Invalid request')
        try:
            if  item=='':
                langList.remove('')
                # possible mistake might occur here
                translatedList.remove('')
        except:
            pass
    print(langList)
    print(translatedList)
    
    # zip_iterator = zip(langList, translatedList)
    # 3a_dictionary = {}
    # a_dictionary = dict(zip_iterator)
    # a_dictionary = {}
    for key in langList:
        for value in translatedList:
            a_dictionary[key] = value
            translatedList.remove(value)
            break  
    
    print(a_dictionary)

    
    
    return render_template("languagesIndexExtended.html", name=inpLang, keyword=keyword, a_dictionary=a_dictionary)
    #return render_template("languagesIndex.html", name=inpLang, keyword=keyword)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
 
