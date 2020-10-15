from flask import Flask, request
#Function that actually does the searching
from loiSearcher import loiSearch

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def loiSearch_page():
    errors = ""
    #Check if we have submitted data
    if request.method == "POST":
        #Get frontier, search term
        frontierToSearch = request.form["frontierToSearch"]
        searchTerm = request.form["searchTerm"]
        #Check if the caseSensitive checkbox is included in the request.
        checked = "caseSensitive" in request.form
        if frontierToSearch is not None and searchTerm is not None:
            if checked==1:
                result = loiSearch(frontierToSearch,searchTerm,1)
            else:
                result = loiSearch(frontierToSearch,searchTerm,0)
            return '''
                <html>
                    <body>
                        <p>{result}</p>
                        <p><a href="/">Click here to search again</a>
                    </body>
                </html>
            '''.format(result=result)
    #Set up page for user to input data
    return '''
        <html>
            <body>
                {errors}


                <form method="post" action=".">
                    <p>Enter frontier (blank for all).<br>Choices: [AF, CF, CommF, CompF, EF, IF, NF, RF, TF, UF]</p>
                    <p><input name="frontierToSearch" /></p>
                    <p>Enter search term:</p>
                    <p><input name="searchTerm" /></p>
                    <p><input type="checkbox" id="caseSensitive" name="caseSensitive" value="Yes"><label for="caseSensitive">Case-Sensitive?</label>
                    <p><input type="submit" value="Search" /></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors)

###html search section###
from flask import jsonify
import pickle

inpFilename="/home/shedges/mysite/LOI_dict.pickle"
f = open(inpFilename, 'rb')

#Load loiList, {id,frontier,filename,link,text}
loiList = pickle.load(f)

#List of frontiers
frontiers=["AF","CF","CommF","CompF","EF","IF","NF","RF","TF","UF"]

@app.route('/search', methods=['GET'])
def api_id():
    #We don't want to modify the list if we restrict to a frontier,
    #so make a copy of it
    localList=loiList

    #Deal with frontier argument, if present
    frontier=""
    if 'frontier' in request.args:
        #Get the requested frontier
        frontier = request.args['frontier']
        #Check the frontier is valid
        if frontier in frontiers:
          #Reduce dictionary to subset matching request
          localList = [i for i in localList if i["frontier"]==frontier]

    #Parse the case sensitive argument, if present
    caseSensitive=0
    if 'caseSensitive' in request.args:
      caseSensitive=1

    #Holds the results from the search
    results=[]
    nTimes=0

    #Parse the search term, if there
    if 'term' in request.args:
      term = request.args['term']
    else:
      term=""

    #Do the search
    if caseSensitive==0:
      for loi in localList:
        nTimes = loi['text'].count(term)
        if nTimes>0:
          loi['nTimes']=str(nTimes)
          results.append(loi)
    else:
      for loi in localList:
        nTimes = loi['text'].lower().count(term.lower())
        if nTimes>0:
          loi['nTimes']=str(nTimes)
          results.append(loi)


    #Sort by number of occurrences of the search word
    results.sort(key = lambda x: int(x['nTimes']))
    results.reverse()

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

