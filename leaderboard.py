def rang(d,L):
    #retourne le rang pour la liste L
    # L sous la forme : [user, score]
    # d sous la forme {1 : [user1, score], 2 : [user2, score] ,...}
    scores = sorted([val[1] for val in d.values()], reverse=True)
    nv=1
    for score in scores:
        if L[1] < score:
            nv += 1
    return nv

def nv_score(d,L):
    nv=rang(d,L)
    if nv > len(d) :
        return d
     
    else:
        if L[1]==d[nv][1]:
            d[nv]=[d[nv],L]
        else :
            for i in range(0,len(d)-nv):
                d[len(d)-i]=d[len(d)-i-1]
            d[nv]=L
    return d

    

d = { 1 : ["user1", 300], 2:["user2", 200], 3 : ["user3", 100]} 
L=["user4", 50]
print(rang(d,L))
print(nv_score(d,L))