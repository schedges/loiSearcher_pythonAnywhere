def loiSearch(frontierToSearch,searchTerm,caseSensitive=0):
    import pickle

    #For linking to LOIs
    mainsite = "http://www.snowmass21.org/docs/files/summaries"

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

    #Remove quotes if user supplied when inputting frontier
    frontierToSearch=frontierToSearch.strip("'")
    frontierToSearch=frontierToSearch.strip('"')

    #Make subset of frontiers to search if requested
    frontierFound=0
    if frontierToSearch in frontiers:
      loiList = [loiList[i] for i in range(0,len(loiList)) if loiList[i][0]==frontierToSearch]
      frontierFound=1

    #Step through LOIs, searching for word or phrase
    matchingLOIs=[]
    for loi in loiList:
      if caseSensitive==1:
        nTimes = loi[2].count(searchTerm)
        caseSensitiveString = "(case-sensitive)"
      else:
        nTimes = loi[2].lower().count(searchTerm.lower())
        caseSensitiveString = "(case-insensitive)"
      if nTimes>0:
        matchingLOIs.append([loi[0],loi[1],loi[2],nTimes])

    #Sort by number of occurrences of the search word
    matchingLOIs.sort(key = lambda x: x[3])
    matchingLOIs.reverse()

    #Update results to display if fewer than nResultsToShow
    if len(matchingLOIs)<nResultsToShow:
      nResultsToShow=len(matchingLOIs)

    #Generate output string to display results. Start with number of matching results
    line="<b>Found "+str(len(matchingLOIs))+" matching LOIS in "
    if frontierFound==1:
        line += frontierToSearch + " frontier"
    else:
        line += " all frontiers"
    line += " for term '"+searchTerm+"' "+caseSensitiveString+"</b>\n\n"

    #Print search ranking, frontier, pdf title/link, and preview text
    for i in range(0,nResultsToShow):
        #Check there are enough characters to display the intended preview length. If not, shorten how many are displayed.
        if len(matchingLOIs[i][2]) < nPreviewChars:
            charsToDisplay=len(matchingLOIs[i][2])
        else:
            charsToDisplay=nPreviewChars
        line += "<b>"+str(i+1)+". "+matchingLOIs[i][0]+" - "+'<a href='+mainsite+'/'+matchingLOIs[i][0]+'/'+matchingLOIs[i][1]+'>'+matchingLOIs[i][1]+'</a>'
        line += " - " + str(matchingLOIs[i][3]) + " occurrences"+"</b>\n"
        line += matchingLOIs[i][2][0:charsToDisplay]+"...\n\n"

    #Make newlines html breaks
    line = line.replace('\n', '<br>')

    #Close LOIs.pickle
    f.close()

    #Return output string
    return line
    '''
    #Display top results


    '''
