import numpy as np
import cv2
#점과 직선 사이의 거리를 구하는 함수
def dist(C,L):
    area = abs ( (L[0] - C[0]) * (L[3] - C[1]) - (L[1] - C[1]) * (L[2] - C[0]) )
    AB = ( (L[0] - L[2]) ** 2 + (L[1] - L[3]) ** 2 ) ** 0.5
    return ( area / AB )

#점 사이의 거리를 구하는 함수
def distC(c1,c2):
    d=((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)**0.5
    return(round(d,2))

#이미지를 입력받고 간략화
src = cv2.imread("picture1.png")
dst = src.copy()
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

#윤곽선, 직선 검출
canny = cv2.Canny(gray, 5000, 1500, apertureSize = 5, L2gradient = True)
lines = cv2.HoughLinesP(canny, 0.8, np.pi / 180, 90, minLineLength = 10, maxLineGap = 100)

#직선의 양 끝점의 좌표를 딕셔너리로 저장
L={}
for i in lines:
    cv2.line(dst, (i[0][0], i[0][1]), (i[0][2], i[0][3]), (0, 0, 255), 2)
    i[0][0] = int(i[0][0])
    i[0][1] = int(i[0][1])
    i[0][2] = int(i[0][2])
    i[0][3] = int(i[0][3])
    L[(i[0][0], i[0][1],i[0][2],i[0][3])]=[]

print("L=",L)

#코너 검출
corners = cv2.goodFeaturesToTrack(gray, 100, 0.1, 30, blockSize=3, useHarrisDetector=True, k=0.03)

#코너의 좌표를 딕셔너리로 저장
C={}

for dot in corners:
    x,y = dot[0]
    x = int(x)
    y = int(y)
    cv2.circle(dst, (x, y), 3, (0, 255, 0), 1, cv2.LINE_AA)
    C[(x,y)]={}

print("C=",C)

#같은 직선 위의 코너들을 L에 넣음
Keys=list(C.keys())

for i in L:
    for j in Keys:
        if dist(j,i)<30:
            L[i].append(j)

print("L=",L)

#한 코너에서 같은 직선 위의 코너와 그 사이의 거리를 구함
for i in L:
    for j in L[i]:
        for k in L[i]:
            if distC(j,k)!=0:
                C[j][k]=[i,distC(j,k)]

print("C=",C)

#그 중에 간접적으로 이어진 코너들의 값을 0으로 만듦
for i in C:
    for j in C[i]:
        for k in C[i]:
            if C[i][j][0]==C[i][k][0] and distC(i,j)<distC(i,k) and distC(j,k)<distC(i,k):
                C[i][k][1]=0

print("C=",C)

#직접 연결된 코너들로만 이루어진 딕셔너리
Corners={}
for i in C:
    for j in C[i]:
        if C[i][j][1]!=0:
            if i in Corners:
                Corners[i].append(j)
            else:
                Corners[i]=[j]

print("Corners=",Corners)

#한붓그리기 가능여부 판별
odd=0
for i in Corners:
    if len(Corners[i])%2==1:
        odd+=1

if odd==0 or 2:
    print("한붓그리기 알고리즘")#나중에 채울 것
else:
    print("한붓그리기 불가능")

cv2.imshow("dst", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
