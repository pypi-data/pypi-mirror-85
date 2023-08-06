import numpy 
import pandas 
import sys
import copy
def topsis(a, b, c):
    filename = a
    weights = b
    impacts = c
    dataset = pandas.read_csv(filename).values
    dataaat = dataset[:, 1:]
    weights = list(map(float, weights.split(',')))
    impacts = list(map(str, impacts.split(',')))
    r, c = dataaat.shape  
    if len(weights) != c:
        print("Enter correct number of weights")
        sys.exit()
    if len(impacts) != c:
        print("Enter correct number of impacts")
        sys.exit()
    for i in weights:
        if i < 0:
            print("Enter positive weights only")
            sys.exit()    
        for i in impacts:
            if i != '+' and i != '-':
                print("impacts can only be + or -")
                sys.exit()       
    sums = sum(weights)
    nm_mat = numpy.zeros([r, c])
    for i in range(c):
        for j in range(r):
            d = numpy.sqrt(sum(dataaat[:, i]**2))
            temp = dataaat[j, i]/d
            nm_mat[j, i] = temp*(weights[i]/sums)   
    postt = []
    negaa = []
    for i in range(c):
        if impacts[i] == '+':
            postt.append(max(nm_mat[:, i]))
            negaa.append(min(nm_mat[:, i]))    
        else:
            postt.append(min(nm_mat[:, i]))
            negaa.append(max(nm_mat[:, i]))     
    post = []
    negt = []
    for i in range(r):
        s = 0
        for j in range(c):
            s = s + (nm_mat[i, j]-postt[j])**2   
        post.append(numpy.sqrt(s))
    for i in range(r):
        s = 0
        for j in range(c):
            s = s + (nm_mat[i, j]-negaa[j])**2      
        negt.append(numpy.sqrt(s)) 
    ab = []
    for i in range(r):
        ab.append(negt[i]/(post[i]+negt[i]))
    item = []*r
    for i in range(r):
        item.append(dataset[i, 0])       
    item = list(item)
    rank = [0]*r
    a = copy.deepcopy(ab)
    c = 1
    for i in range(r):
        t = max(a)
        for j in range(r):
            if a[j] == t:
                rank[j] = c
                c = c+1
                a[j] = 0
                break    
    rank = list(rank)
    out = {'Item': item, 'Perforamnce score': ab, 'Rank': rank}
    resut = pandas.DataFrame(out)
    print(resut)
def main():
    a = sys.argv[1]
    b = sys.argv[2]
    c = sys.argv[3]
    topsis(a, b, c)
if __name__ == "__main__":
    main()



       
        
      



    
        
        
        
        
        
    
    
        
    
        

    





    