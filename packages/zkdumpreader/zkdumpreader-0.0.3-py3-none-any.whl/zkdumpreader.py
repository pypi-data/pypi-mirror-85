def dumpread(ftoread,ftowrite,tfd=20):
    """
    Reads the lammps dump file with given name and find how many of the bound TFs stay bound. 
    Creates a report.txt and a csv file with given name . Csv file has two colums first being
    timestep and the second being number of remaining bound TFs.
    """
    #transferring dump data into an 3D array---------------------------------------
    #importing necessary modules----------------------------------------------------
    import numpy as np
    from math import sqrt

    #reading dump file line-by-line------------------------------------------------
    dump = open(ftoread, "r")
    lines = dump.readlines()
    dump.close()

    #scale back coeff--------------------------------------------------------------
    coeff = lines[5].split()
    xco = float(coeff[1])
    coeff2 = lines[6].split()
    yco = float(coeff2[1])
    coeff3 = lines[7].split()
    zco = float(coeff3[1])

    #finding the number of the atoms and number of the lines between timesteps-----
    number_atom = int(lines[3])
    batch = number_atom + 9

    n = 0
    oo = 0
    for a in lines[9:batch+1]:
        b = a.split()[1]
        if b == "1" or b=="2":
            n +=1

    btf = int(n/tfd)
    #number of the timesteps-------------------------------------------------------
    time_num = int(len(lines)/batch)
    boundN = np.zeros(time_num)
    ts = np.zeros(time_num)

    first = btf

    #creating array of zeros with intented size------------------------------------
    data = np.zeros([time_num,number_atom,3])
    times = np.zeros([time_num,1])

    #opening new file for results--------------------------------------------------
    repp = "ftoread"+"report.txt"
    rp = open(repp,"w")

    c = 0
    #for loop to create array of times--------------------------------------------
    for i in range(time_num):

        step = int(lines[i*(batch)+1])
        times[i,0] = step

        c = c + 1
        print("Processing... " + str(c) + " of " + str(time_num))
        minuS = 0

        kk = -3
        #for loop to make the 3D array--------------------------------------------
        for k in range(number_atom):

            values = lines[i*batch+k+9].split()
            atomID = int(values[0])

            data[i,atomID-1,0] = float(values[2])
            data[i,atomID-1,1] = float(values[3])
            data[i,atomID-1,2] = float(values[4])

            #promoter sites taken avarage of psotion-------------------------------
        for j in range(1,n):
            if j%tfd == 1:
                #find promoter site takes avarage
                aP = (data[i,j-1] + data[i,j])/2
                #find bound tfs and takes avarage
                kk +=3
                index = n + kk
                aTF = (data[i,index] + data[i, index + 2])/2

                #find distance between them
                ds2 = (xco*(aP[0]-aTF[0]))**2 + (yco*(aP[1]-aTF[1]))**2 + (zco*(aP[2]-aTF[2]))**2
                distance = sqrt(ds2)

                #print(kk)
                if distance > 2.5:
                    rp.write("promoter with atom ID " + str(j) + " is apart from the TF with ID "+str(index + 1) +" in timestep " + str(step)+" (Distance: " + str(distance)+")\n")
                    minuS += 1


        last = first - minuS
        boundN[i] = last
        ts[i] = i + 1
        #print (last)

        rp.write("End of timestep " + str(step) + "\n\n")


    ts = np.array(ts)
    boundN = np.array(boundN)

    lenn = len(ts)

    ts = ts.reshape(lenn,1)
    boundN = boundN.reshape(lenn,1)

    lc = np.append(ts, boundN, axis = 1)

    lc = lc.reshape(lenn,2)

    np.savetxt(ftowrite,lc,fmt= "%s",delimiter=",")

    print("--------------         DONE            --------------")
    return

if __name__ == "__main__":
    dumpread("dump.main","main.csv")