import sys
import pandas as pd
def main():
  # EX%@zR-4DL^Ycs%


  # print(sys.argv)

  if len(sys.argv) != 5:
    print("Error !! Wrong number of parameters")
    print("Only two parameters are required")
    print("usages: python tt.py <inputFile> <OutputFile>")
    print("example: python tt.py abc.txt result.txt")
    exit(0)

  try:

    data = pd.read_csv(sys.argv[1])  # Open the file in reading mode
    # writeFp = open(sys.argv[2], 'w')  # Open the file in writing mode
    '''
    w=data['Corr']
    x=data['Rseq']
    y = data['RMSE']
    z = data['Accuracy']
    ww=1
    xw=1
    yw=1
    zw=1
    ww = float((sys.argv[3].split(","))[0])
    xw = float((sys.argv[3].split(","))[1])
    yw = float((sys.argv[3].split(","))[2])
    zw = float((sys.argv[3].split(","))[3])
    '''

    w = list(data.iloc[:, 1])
    x = list(data.iloc[:, 2])
    y = list(data.iloc[:, 3])
    z = list(data.iloc[:, 4])
    ww = float((sys.argv[3].split(","))[0])
    xw = float((sys.argv[3].split(","))[1])
    yw = float((sys.argv[3].split(","))[2])
    zw = float((sys.argv[3].split(","))[3])

    # print(z)
    # print(len(z))

    def rms(A):
      sumer = 0
      for i in range(0, 5):
        sumer = sumer + (A[i] * A[i])

      return (sumer ** 0.5)

    # print(rms(z))
    w1 = []
    x1 = []
    y1 = []
    z1 = []

    for i in range(0, 5):
      w1.append((ww * w[i]) / rms(w))
    for i in range(0, 5):
      x1.append((xw * x[i]) / rms(x))
    for i in range(0, 5):
      y1.append((yw * y[i]) / rms(y))
    for i in range(0, 5):
      z1.append((zw * z[i]) / rms(z))

    # print(w1)
    # print(x1)
    # print(y1)
    # print(z1)
    wmin = min(w1)
    wmax = max(w1)
    xmin = min(x1)
    xmax = max(x1)
    ymin = min(y1)
    ymax = max(y1)
    zmin = min(z1)
    zmax = max(z1)
    # print(wmin)
    # print(wmax)
    # print(w1[0])
    sneg = []
    spos = []
    ssum = []

    for i in range(0, 5):
      sumt = 0
      sumt = ((w1[i] - wmin) ** 2) + ((x1[i] - xmin) ** 2) + ((y1[i] - ymin) ** 2) + ((z1[i] - zmin) ** 2)
      sneg.append(sumt ** 0.5)

    for i in range(0, 5):
      sumt = 0
      sumt = ((w1[i] - wmax) ** 2) + ((x1[i] - xmax) ** 2) + ((y1[i] - ymax) ** 2) + ((z1[i] - zmax) ** 2)
      spos.append(sumt ** 0.5)
    sfinal = []
    for i in range(0, 5):
      ssum.append(sneg[i] / (spos[i] + sneg[i]))
      sfinal.append(sneg[i] / (spos[i] + sneg[i]))

    # print(spos)
    # print(sneg)
    # print(ssum)

    ssum.sort(reverse=True)
    ssort = sorted(ssum, reverse=True)
    # print(ssort)
    # print(sfinal)
    posi = []
    for i in range(0, 5):
      for j in range(0, 5):
        if sfinal[i] == ssort[j]:
          posi.append(j + 1)

    print(posi)
    data['Toposis'] = sfinal
    data['Position'] = posi

    data.to_csv(sys.argv[2], index=False, header=True)







  except:
    print("Error !! something goes wrong")
    print(" - Incorrect parameters may be given")
    print(" - File not found")

if __name__ == '__main__':
    main()
