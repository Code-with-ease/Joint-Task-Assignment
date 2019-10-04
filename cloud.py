import random
import math
import matplotlib.pyplot as plt

def edge_devie(ro,ed):

    thetaed = ed[0]*ed[1]
    ed.append(thetaed)

    phied = ro*ed[0]*ed[1] + ed[1]*(1-ed[0])
    ed.append(phied)

def access_point(ro,ed,ap):

    lambdaap = ed[3] * ((1-ed[0])/(1-ed[0]+ro*ed[0]))
    ap.append(lambdaap)
    betaap = ed[3] * ((ro*ed[0])/(1-ed[0]+ro*ed[0]))

    thetaap = ap[0]*ap[1]
    ap.append(thetaap)

    phiap = ro*ap[1]*ap[0] + ap[1]*(1-ap[0]) + betaap
    ap.append(round(phiap,2))

    ap.append(round(betaap,2))

def latency(ro,ed,ap,cc):
    led = 1/ed[2] + ro/ed[3] + ro/ap[3]
    ed.append(round(led,2))

    lap = 1/ed[3] + 1/ap[2] + ro/ap[3]
    ap.append(round(lap,2))

    lcc = 1/ed[3] + 1/ap[3] +1/cc[2]
    cc.append(round(lcc,2))

def latency_minimization(ed,ap,cc):
    r = ed[1]*(ed[0] * ed[4] + ap[0] * ap[5] + cc[0] * cc[3])
    # Since for all edge devices, lambda , and s is same therefore the latency will be equal for all hence minimum
    return r

def cleaning(L):
    m = L[0]
    flag = 0
    for n,i in enumerate(L):
        if(i<m):
            L[n] = m+flag
        elif(i>m):
            flag = 1
            m = i
    return L

def processingAtED(ed):
    Ted = ed[1] * ed[0] / ed[2];
    ed.append(Ted)

def transmitionToAP(ro , ed):
    ted = (ro*ed[0]*ed[1] + ed[1]*(1-ed[0]))/ed[3]
    ed.append(ted)

def processingAtAP(ap):
    Tap = 5*ap[1]*ap[0]/ap[2]
    ap.append(Tap)

def transmitionToCC(ro,ap):
    tap = (5*ap[1]*(1-ap[0]+ro*ap[0]) + 5*ap[4])/ap[3]
    ap.append(tap)

def processingAtCC(cc):
    Tcc = 5*cc[1]/cc[2]
    cc.append(Tcc)

def recoveryTimeMini(ed,ap,cc):
    ed1 = max(ed[5],ed[6])
    ap1 = max(ap[6],ap[7])
    m1 = max(ed1,ap1)
    Tr = max(m1,cc[4])
    return Tr

# def miniAtED(ed):


if __name__ == "__main__":

    sed = 0.05
    sap = 0.3
    scc = 0.65
    ro = 0.1
    x = []
    for i in range(1,481,60):
        x.append(i)
    # x = sorted(x)

    print("Lambda for ED's are:- ",x)
    L = []
    Tprocess = []
    T = []

    for lambdaed in x:
        ed = []
        ed.append(sed)
        ed.append(lambdaed)
        edge_devie(ro,ed)
        # ed  = [ s , lambda , theta , phi , Latency , T , t]

        ap = []
        ap.append(sap)
        access_point(ro,ed,ap = ap)
        # ap = [s , lambda , theta , phi , beta , Latency , T , t ]

        cc = []
        cc.append(scc)
        r = ro * ed[0] / (1-ed[0])
        lambdacc = ed[3]*(1-ap[0])/(1-ap[0] + ro*ap[0]+r)
        cc.append(round(lambdacc,2))
        cc.append(round(lambdacc, 2))
        # cc = [s , lambda , theta , Latency , T ]

        latency(ro,ed=ed , ap=ap , cc=cc)
        # print("ED:- ",ed)
        # print("AP:- ", ap)
        # print("CC:- ", cc)

        L.append(math.trunc(latency_minimization(ed=ed , ap = ap , cc=cc)))
        L = cleaning(L)

        processingAtED(ed)
        transmitionToAP(ro,ed = ed)
        processingAtAP(ap)
        transmitionToCC(ro,ap = ap)
        processingAtCC(cc)

        T.append(round(recoveryTimeMini(ed=ed , ap=ap , cc=cc),3))
        Tprocess.append(round((ed[5] + ed[6] + ap[6] + ap[7]+ cc[4]) , 3))



    print("The latencies are:- ", L)
    m = max(L)
    plt.title('System Latency vs Data Generation')
    plt.plot(x , L ,marker='*',markerfacecolor='red',linestyle='--',color='yellow',linewidth=2,markersize=10)
    plt.axis([-2,500,3,m+2])
    plt.show()


    print("The Processing Time are:- ", Tprocess)
    m = max(Tprocess)
    plt.title('Processing Time vs Data Generation')
    plt.plot(x,Tprocess,marker='o',markerfacecolor='yellow',linestyle='-',color='blue',linewidth=1,markersize=5)
    plt.axis([-2, 500, 5, m + 2])
    plt.show()

    print("The Recovery Time are:- ", T)
    m = max(T)
    plt.title('Recovery Time vs Data Generation')
    plt.plot(x, T, marker='o', markerfacecolor='magenta', linestyle='-', color='black', linewidth=1, markersize=5)
    plt.axis([-2, 500, 0, m + 2])
    plt.show()
