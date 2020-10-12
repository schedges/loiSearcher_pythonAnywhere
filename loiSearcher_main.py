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

