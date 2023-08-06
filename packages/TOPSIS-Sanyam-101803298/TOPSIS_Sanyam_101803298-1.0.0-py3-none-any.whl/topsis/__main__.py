def main():
    import pandas as pd
    import copy
    import sys

    if len(sys.argv) != 5:
        print("Incorrect number of parameters - ", len(sys.argv))
        exit(0)
    weights = sys.argv[2]
    impacts = sys.argv[3]
    result = sys.argv[4]

    try:
        weights = [float(x) for x in weights.split(",")]
    except:
        print("Weights not separated by comma")
        exit(0)

    try:
        impacts = impacts.split(",")
    except:
        print("Impacts not separated by comma")
        exit(0)

    for ele in impacts:
        if (ele != "+" and ele != "-"):
            print("Impacts must be either +ve or -ve")
            exit(0)
    try:
        df = pd.read_csv(sys.argv[1])
    except:
        print("File not found")
        exit(0)

    arr = list(df)
    r = len(list(df[arr[0]]))
    c = len(arr)

    if (c-1 != len(weights) or c-1 != len(impacts) or len(impacts) != len(weights)):
        print("Number of weights, number of impacts and number of columns from 2nd to last columns are not equal")
        exit(0)

    k = 0
    splus = [0]*r
    sneg = [0]*r
    for i in range(1, c):
        col = list(df[arr[i]])
        val = 0
        for ele in col:
            try:
                val += (ele**2)
            except:
                print("Non numeric values are present in column - ", i+1)
                exit(0)
        val = val**0.5
        for j in range(0, len(col)):
            col[j] = (col[j]/val)*weights[k]
        if impacts[k] == '+':
            vplus = max(col)
            vneg = min(col)
        else:
            vplus = min(col)
            vneg = max(col)
        for j in range(0, r):
            splus[j] += ((col[j]-vplus)**2)
            sneg[j] += ((col[j]-vneg)**2)
        k += 1

    for i in range(0, r):
        splus[i] = (splus[i]**0.5)
        sneg[i] = (sneg[i]**0.5)
    spn = [0]*r
    for i in range(0, r):
        spn[i] += (splus[i]+sneg[i])
    perf_score = [0]*r
    for i in range(0, r):
        perf_score[i] = (sneg[i]/spn[i])
    li = copy.deepcopy(perf_score)
    li.sort(reverse=True)
    m = {}
    for i in range(0, len(li)):
        m[li[i]] = i+1
    ranks = [0]*r
    for i in range(0, len(perf_score)):
        ranks[i] = m[perf_score[i]]
    df["Topsis Score"] = perf_score
    df["Rank"] = ranks
    df.set_index('Model', inplace=True)
    df.to_csv(result)


if __name__ == '__main__':
    main()
