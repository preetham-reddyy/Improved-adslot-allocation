import time
import sys


class cmine():
    def __init__(self, inpfile):
        self.minRF = 0
        self.maxOR = 0.3
        self.inpfile = inpfile
        self.cvg_pttrn = []
        self.costdict = {}
        self.nots = self.getlines(inpfile)
        self.NOk = []
        self.items, avg = self.dbscan(inpfile)
        # print(avg)
        # print(self.items)
        # print(self.items.items())
        sorteditems = sorted(self.items.items(), key=lambda a: (-a[1], a[0]))
        # print(sorteditems)
        avg = 0
        count = 0
        for i in sorteditems:
            self.costdict[i[0]] = i[1]
            avg = avg+i[1]
            count = count+1
        avg = avg/self.nots
        avg = avg/count
        self.minCS = avg

        # print("minCS", avg)
        # print(self.costdict)
        mintracs = self.minRF * 1.0 * self.nots
        # print(sorteditems)
        freqitems = filter(lambda x: (x[1] >= mintracs), sorteditems)
        # with open("freq2.txt","w") as f:
            # for item in freqitems:
                # f.write(str(item)+"\n")
        

        #print(freqitems)
        one_size_coverage = filter(lambda x: (
            x[1] >= self.minCS * 1.0 * self.nots), sorteditems)
        self.freqitems = map(lambda x: x[0], freqitems)
        self.cvgs = map(lambda x: x[0], one_size_coverage)
        
        # print("Size one coverage patterns")
        # print(self.freqitems)

        for i in self.freqitems:
            self.NOk.append([i])
        for i in one_size_coverage:
            self.cvg_pttrn.append(
                [i[0], i[1]/self.nots, 0, i[1], self.costdict[i[0]]])

        # print(len(self.NOk))
        # print(self.NOk)
        # print()

    def get_overlapratio_cs(self, pattern):
        ovr_nume_1 = set()
        for i in pattern[:-1]:
            for j in range(len(self.database)):
                if i in self.database[j]:
                    ovr_nume_1.add(j)
        ovr_deno = set()
        for j in range(len(self.database)):
            if pattern[-1] in self.database[j]:
                ovr_deno.add(j)
        cs_nume = ovr_nume_1.union(ovr_deno)
        ovr_nume = ovr_nume_1.intersection(ovr_deno)
        # print ovr_nume,ovr_deno,ovr_nume_1
        return len(ovr_nume)*1.0/len(ovr_deno), len(cs_nume)*1.0/self.nots

    def prune(self, patterns):
        f = open(self.inpfile, 'r')
        for row in f:
            row = row.rstrip('\n')
            row = row.split(" ")
            # print(row)
            if len(row[-1]) == 0:
                row.pop()
            for i in range(len(patterns)):
                ovr_flag = False
                for item in patterns[i][0][:-1]:
                    if item in row:
                        patterns[i][1] += 1
                        ovr_flag = True
                        break
                if(patterns[i][0][-1] in row):
                    patterns[i][3] += 1
                    if ovr_flag == True:
                        patterns[i][2] += 1
                    else:
                        patterns[i][1] += 1
            # print row,patterns

        NOk = []
        coverage_patterns = []
        for i in patterns:
            if i[2]*1.0/i[3] <= self.maxOR:
                NOk.append(i[0])
                if i[1]*1.0/self.nots >= self.minCS:
                    k = i
                    k[1] = i[1]*1.0/self.nots
                    k[2] = i[2]*1.0/i[3]
                    k[3] = round((k[1] - k[2]) * self.nots, 1)
                    sum = 0
                    for i in k[0]:
                        sum = sum + self.costdict[i]
                    self.cvg_pttrn.append([k[0], k[1], k[2], k[3], sum])

        # print(coverage_patterns)
        # print(len(NOk))
        # print(NOk)
        # print()
        return NOk, coverage_patterns

    def expand(self):
        cnt = 0
        cnt1 = 0
        length = 1
        while len(self.NOk) > 0:
            # print("Length :",len(self.NOk))
            # print(self.NOk)
            # print()
            print(length, len(self.NOk))

            C_k = []
            for i in range(len(self.NOk)):
                for j in range(i+1, len(self.NOk)):
                    cnt += 1
                    if(self.NOk[i][:-1] == self.NOk[j][:-1]):
                        cnt1 += 1
                        newpattern = self.NOk[i] + [self.NOk[j][-1]]
                        C_k.append([newpattern, 0, 0, 0])
                    else:
                        break
            # print(length+1, "Number of candidates", len(C_k))
            length += 1
            self.NOk, coverage_patterns = self.prune(C_k)
            # print(coverage_patterns)
        return cnt1

    def dbscan(self, inputfile):
        f = open(inputfile, 'r')
        a = {}
        # database = []
        avg = 0
        number = 0
        for row in f:
            number = number+1
            row = row.rstrip('\n')
            row = row.split(" ")
            if len(row[-1]) == 0:
                row.pop()
            # print(row)
            # database.append(row)
            count = 0
            for j in row:
                count = count+1
                if j in a:
                    a[j] += 1
                else:
                    a[j] = 1
            avg = avg + count
        avg = avg / number
        return a, avg

    def getlines(self, filename):
        with open(filename, "r") as f:
            return sum(1 for _ in f)
