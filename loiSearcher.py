def loiSearch(frontierToSearch,searchTerm,caseSensitive=0):
    import pickle

    #How many results to show
    nResultsToShow=20
    nPreviewChars=500

    #Open input file
    inpFilename="/home/shedges/mysite/LOIs.pickle"
    f = open(inpFilename, 'rb')

    #Load loiList, three columns: [[Frontier, Filename, Text]]
    loiList = pickle.load(f)

    #Ask user if they want to limit search to a specific frontier
    frontiers=["AF","CF","CommF","CompF","EF","IF","NF","RF","TF","UF"]
    frontierToSearch=frontierToSearch.strip("'")
    frontierToSearch=frontierToSearch.strip('"')

    #Make subset of frontiers to search if requested
    frontierFound=0
    if frontierToSearch in frontiers:
      loiList = [loiList[i] for i in range(0,len(loiList)) if loiList[i][0]==frontierToSearch]
      frontierFound=1

    #Step through LOIs, searching for word
    matchingLOIs=[]
    for loi in loiList:
      if caseSensitive==1:
        nTimes = loi[2].count(searchTerm)
      else:
        nTimes = loi[2].lower().count(searchTerm.lower())
      if nTimes>0:
        matchingLOIs.append([loi[0],loi[1],loi[2],nTimes])

    #Sort by number of occurrences of the search word
    matchingLOIs.sort(key = lambda x: x[3])
    matchingLOIs.reverse()

    #Update results to display if fewer than nResultsToShow
    if len(matchingLOIs)<nResultsToShow:
      nResultsToShow=len(matchingLOIs)

    line=""
    if frontierFound==1:
        if caseSensitive==1:
            line+="<b>Found "+str(len(matchingLOIs))+" matching LOIs in "+frontierToSearch+" frontier for term '"+searchTerm+"' (case-sensitive)</b>\n\n"
        else:
            line+="<b>Found "+str(len(matchingLOIs))+" matching LOIs in "+frontierToSearch+" frontier for term '"+searchTerm+"' (case-insensitive)</b>\n\n"

    else:
        if caseSensitive==1:
            line+="<b>Found "+str(len(matchingLOIs))+" matching LOIs in all frontiers for term '"+searchTerm+"' (case-sensitive)</b>\n\n"
        else:
            line+="<b>Found "+str(len(matchingLOIs))+" matching LOIs in all frontiers for term '"+searchTerm+"' (case-insensitive)</b>\n\n"



    #Close LOIs.pickle
    mainsite = "http://www.snowmass21.org/docs/files/summaries"
    f.close()

    for i in range(0,nResultsToShow):
        #Check there are enough characters to display the intended preview length. If not, shorten how many are displayed.
        if len(matchingLOIs[i][2]) < nPreviewChars:
            charsToDisplay=len(matchingLOIs[i][2])
        else:
            charsToDisplay=nPreviewChars
        line += "<b>"+str(i+1)+". "+matchingLOIs[i][0]+" - "+'<a href='+mainsite+'/'+matchingLOIs[i][0]+'/'+matchingLOIs[i][1]+'>'+matchingLOIs[i][1]+'</a>'
        line += " - " + str(matchingLOIs[i][3]) + " occurrences"+"</b>\n"
        line += matchingLOIs[i][2][0:charsToDisplay]+"...\n\n"

    line = line.replace('\n', '<br>')
    return line
    '''
    #Display top results


    '''
