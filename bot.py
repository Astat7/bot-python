from random import randint

throwAway = 0


mood = "neutral"
moods = ["sad", "neutral", "happy"]

casualGreets =[ "hello", "hi", "greetings"]

questionStarter = ["how", "where", "when", "who", "what"]

neutralStatementResponses = ["alright", "ok"]

positiveWords = ["nice", "cool"]

basicVerbs = ["are", "is"]
basicNVerbs = ["aren't", "isn't"]

acknowsP = ["Thanks", "Thank you"]
acknowsN = ["Oh"]

#                     0            1          2          3                 4                5
sentencePoints = ["greeting", "question", "insult", "compliment", "ironic compliment", "statement"]

memory = {"bot.name" : "Placeholder", "bot.mood" : "fine"}





def evaluateInput(inputX):
    frstGuess = 5
    wordsInSentence = str(inputX.lower())
    wordsInSentence = wordsInSentence.split(" ")

    order = 1

    target = None
    positivnes = True
    subjectMeaning = "Neutral"



    greetsInSentence = []
    
    # states: 0 = idle, 1 = looking for object name to memorize, 2 = memorize value for object, 3 = question intermission, 4 = question object owner, 5 question object
    state = 0

    # get data from sentence
    wordsCount = wordsInSentence.__len__()
    
    forIteration = 0
    for word in wordsInSentence:
        forIteration += 1
        if state == 0:
            if word in casualGreets:
                greetsInSentence.append(word)

            if word == "my" or word == "mine":
                
                memorizeData = []
                memorizeDataTemp = []
                
                memorizeData.append("user")
                state = 1

            if word == "what" and forIteration == 1:
                frstGuess = 1
                state = 3

            if word == "how" and forIteration == 1:
                frstGuess = 1
                state = 3
        
            
            if word == "you" or word == "bot":
                target = "bot"
            elif word in basicNVerbs:
                positivnes = not positivnes
            elif word == "not":
                positivnes = not positivnes
            elif word in positiveWords:
                subjectMeaning = "Positive"
            


        # question - recover from memory
        elif state == 3:
            state = 4
        elif state == 4:
            recoverData = []
            recoverDataTemp = []
            if word == "mine" or word == "my":
                recoverData.append("user")
            elif word == "your" or word == "yours":
                recoverData.append("bot")
            elif word == "you" and forIteration == wordsCount:
                recoverData.append("bot")
                recoverData.append("mood")
            else:
                recoverData.append(word)
            state = 5
            
        elif state == 5:
            if forIteration < wordsCount:
                recoverDataTemp.append(word)
            else:
                recoverDataTemp.append(word)
                state = 0
                recoverDataTemp = "_".join(recoverDataTemp)
                recoverData.append(recoverDataTemp)
                recoverDataTemp = []
                
                
        # memorising
        elif state == 1:
            if word != "is" and word != "are":
                memorizeDataTemp.append(word)
            else:
                state = 2
                memorizeDataTemp = "_".join(memorizeDataTemp)
                memorizeData.append(memorizeDataTemp)
                memorizeDataTemp = []
        elif state == 2:
            if forIteration < wordsCount:
                 memorizeDataTemp.append(word)
            else:
                memorizeDataTemp.append(word)
                state = 0
                memorizeDataTemp = "_".join(memorizeDataTemp)
                memorizeData.append(memorizeDataTemp)
                memorizeDataTemp = []
    
    # store data
    try:
        memKey = memorizeData[0] + "." + memorizeData[1]
        memory[memKey] = memorizeData[2]
    except:
        throwAway = 0
            
    # recover data from memory
    try:
        ansKey = recoverData[0] + "." + recoverData[1]
    except:
        throwAway = 0
            
    try:
        if greetsInSentence[0] == wordsInSentence[0]:
            frstGuess = 0
    except:
        throwAway = 0

    if frstGuess == 5:
        if target == "bot":
            if positivnes == True and subjectMeaning == "Positive":
                frstGuess = 3
            elif positivnes == False and subjectMeaning == "Negative":
                frstGuess = 3
            elif positivnes == True and subjectMeaning == "Negative":
                frstGuess = 2
            elif positivnes == False and subjectMeaning == "Positive":
                frstGuess = 2
    
    try:
        return([sentencePoints[frstGuess], ansKey])
    except:
        return([sentencePoints[frstGuess]])

def greet():
    randomVal = randint(1, casualGreets.__len__())
    greet = casualGreets[randomVal-1]
    greet = greet.capitalize()
    try:
        greet = greet + " " + memory["user.name"].capitalize()
    except:
        throwAway = 0
    print(greet)

def decideAnswer(dataA=""):
    if dataA != "" and dataA != "bot.mood":
        response = "{} {} is {}"
        dataCluster = dataA.split(".")
        pronouns = {"bot" : "my",
                    "user" : "your"}
        pronoun = pronouns[dataCluster[0]].capitalize()
        objNames = dataCluster[1].split("_")
        objVals = memory[dataA].split("_")
        tmp = (" ")
        objName = tmp.join(objNames)
        objVal = tmp.join(objVals)
        response = response.format(pronoun, objName, objVal)
        print(response)
    elif dataA != "":
        response = "I am {}"
        response = response.format(memory[dataA])
        print(response)

def thankForCompliment():
    rnd = randint(0, acknowsP.__len__()-1)
    print(acknowsP[rnd])
    mood = "happy"
    memory["bot.mood"] = "happy"


def reactToIronny():
    throwAway = 0

def reactToInsult():
    rnd = randint(0, acknowsN.__len__()-1)
    print(acknowsN[rnd])
    mood = "sad"
    memory["bot.mood"] = "sad"

def decideStatement():
    rnd = randint(0, neutralStatementResponses.__len__()-1)
    print(neutralStatementResponses[rnd].capitalize())


def decideResponse(inputX, dataA=""):
    if inputX == "greeting":
        greet()
    elif inputX == "question":
        decideAnswer(dataA)
    elif inputX == "insult":
        reactToInsult()
    elif inputX == "compliment":
        thankForCompliment()
    elif inputX == "ironic compliment":
        reactToIronny()
    elif inputX == "insult":
        reactToInsult()
    elif inputX == "statement":
        decideStatement()

while True:
    inputt = input("Enter simple sentence for algorithm. Write whole words: ")

    inputPoints = evaluateInput(inputt)
    try:
        inputPoint = inputPoints[0]
        inputPointDTR = str(inputPoints[1])
        decideResponse(inputPoint, inputPointDTR)
    except:
        inputPoint = inputPoints[0]
        decideResponse(inputPoint)
