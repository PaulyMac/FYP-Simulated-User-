from numpy.random import choice
moviefile = open("movies.dat","r")
lines = moviefile.readlines()
movieids = {}
count = 0
ids = []
tagdic ={}
names = []
# create a list of movie ids
for line in lines[1:]:
    ids.append(line.split()[0])
    name = ''
    for word in line.split()[1:]:
        if len(word) == 7:
            try:
                int(word)
                names.append(name)
                break
            except:
                name +=  word + " "
        else:
            name += word + " "
#print(names)
#print(ids)
#create a dictionary mapping movie ids to names
for i in range(len(names)):
    movieids[ids[i]] = names[i]
#print(movieids)
moviefile.close()
#create a dictionary mapping movie ids to their tags
tagfile = open("movie_tags.dat","r")
lines1 = tagfile.readlines()
for line in lines1[1:]:
    if line.split()[0] not in tagdic:
        tagdic[line.split()[0]]=[]
for line in lines1[1:]:
    tagdic[line.split()[0]].append(line.split()[1])
newids = []
#create a list of movies with tags
for i in tagdic:
    newids.append(i)
print(len(movieids))
print(len(ids))
#print(tagdic)
#print(movieids)
#creates a simulated user
def user(x):
    choices = list(choice(newids,x,replace = False))
    print(choices)
    choicenames = []
    choicetags = []
    for i in choices:
        newids.remove(i)
        for x in tagdic[i]:
            if x not in choicetags:
                choicetags.append(x)
    print(choicetags)
    for i in choices:
        choicenames.append(movieids[i])
    print(choicenames)
    CreateJaccard(choices,choicetags)
#Function to allocate jaccard scores to each movie
def CreateJaccard(choices,choicetags):
    x = set(choicetags)
    jaccscore = {}
    for i in tagdic:
        if i not in choices:
            movietags = set(tagdic[i])
            score = len(x.intersection(movietags))/len(x.union(movietags))
            jaccscore[i] = score
    CreateProbabilities(jaccscore,choicetags,choices)
#function that updates the probability of a movie being selected
def CreateProbabilities(jaccscore,choicetags,choices):
    movieprobabilities = []
    score = 0
    for i in jaccscore:
        score += jaccscore[i]
    for i in jaccscore:
        probability = jaccscore[i]/score
        movieprobabilities.append(probability)
    DisplayChoices(movieprobabilities,jaccscore,choicetags,choices)
#function to display set of recommended movies
def DisplayChoices(movieprobabilities,jaccscore,choicetags,choices):
    displaymovies = choice(newids,3,replace = False,p = movieprobabilities)
    movienames = []
    for i in displaymovies:
        movienames.append(movieids[i])
    SelectMovie(displaymovies,jaccscore,choicetags,choices)
#function to simulate a user selecting the best movie
def SelectMovie(displaymovies,jaccscore,choicetags,choices):
    bestmovie = ''
    bestscore  = 0
    for i in displaymovies:
        newids.remove(i)
        if jaccscore[i] > bestscore:
            bestmovie = i
            bestscore = jaccscore[i]
    for i in tagdic[bestmovie]:
        if i not in choicetags:
            choicetags.append(i)
    choices.append(bestmovie)
    for i in displaymovies:
        del tagdic[i]
    print("chosen movie =  " +  movieids[bestmovie])
    if count < 10:
        count += 1
        CreateJaccard(choices,choicetags)







user(10)
