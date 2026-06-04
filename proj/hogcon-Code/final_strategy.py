PLAYER_NAME='sprite'
G=50
MP,MC={},{}
SQR=set([i*i for i in range(1,int(G**0.5)+3)])
isp=lambda s:s in SQR
def fbs(s,o):
 o1,o10=o%10,(o//10)%10;return 2*abs(o10-o1)+1
def ss(s,o):return isp(s)
DDS={}
def dd(n):
 if n in DDS:return DDS[n]
 if n==0:DDS[0]={0:1.0};return DDS[0]
 pnn=(5/6)**n
 dp={0:1.0}
 for i in range(n):
  nd={}
  for s,p in dp.items():
   for r in range(2,7):
    nd[s+r]=nd.get(s+r,0.0)+p/5
  dp=nd
 cd={1:1.0-pnn}
 for s,p in dp.items():
  cd[s]=cd.get(s,0.0)+p*pnn
 DDS[n]=cd
 return cd
def P(s,o):
 if s>=G:return 1.0
 if o>=G:return 0.0
 if(s,o)in MP:return MP[(s,o)]
 mp,br=-1.0,-1
 for r in range(11):
  pr=0.0
  if r==0:
   ts=fbs(s,o)
   ns,no=s+ts,o
   if ss(ns,no):ns,no=no,ns
   pr=1.0 if ns>=G else 1.0-P(no,ns)
  else:
   for ts,p in dd(r).items():
    ns,no=s+ts,o
    if ss(ns,no):ns,no=no,ns
    pr+=p*(1.0 if ns>=G else 1.0-P(no,ns))
  if pr>mp:mp,br=pr,r
 MP[(s,o)],MC[(s,o)]=mp,br
 return mp
def final_strategy(s,o):
 for i in range(11):dd(i)
 P(s,o)
 return MC.get((s,o),5)