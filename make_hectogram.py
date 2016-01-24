from numpy import genfromtxt, delete, zeros
import matplotlib.pyplot as plt
import matplotlib as mpl
import argparse
import sys

#Script for creating a Hectogram

#arg parsing for terminal use
parser = argparse.ArgumentParser(description='Get the output pdf and input csv')
parser.add_argument("--infile", help="input file of type csv. default is data.csv")
parser.add_argument("--outfile", help="output file of type png or pdf. default is image.pdf")
args = parser.parse_args()
if args.infile:
    csvfile = args.infile
else:
    csvfile = 'data.csv'
if args.outfile:
    imagefile = args.outfile
else:
    imagefile = 'image.pdf'

#format the input file
csv = genfromtxt(csvfile, delimiter = ",", skip_header = 3, dtype = int)

#truncate off empty channels (second index of csv)
for i in range(0,csv.shape[1]):
    if all(csv[:,i] == -1):
        break
    
#i therefore is the col incl. and after which all everything is empty
csv = csv[:,0:i]

#truncate off tailing time points
bad = []
for j in range(0,csv.shape[0]):
    if sum([x for x in csv[j,:] if x == -1]) < -1*i + 5:
        bad.append(j)
csv = delete(csv, bad, axis = 0) #update the data

#generate incidence of sleep
sleep = zeros(csv.shape)
for h in range(0,csv.shape[1]):
    for j in range(5,csv.shape[0]):
        if sleep[j-1,h] == 1 and csv[j,h] == 0:
            sleep[j,h] = 1
        elif sleep[j-1,h] == 1 and csv[j,h] > 0:
            pass
        elif all(csv[(j-6):j,h] == 0):
            sleep[j,h] = 1

#format the output image
fig_kw = {'figsize': (8, 6), 'dpi':80}
fig, ax = plt.subplots(**fig_kw)

cmap = mpl.colors.ListedColormap(["w", "k"])
bounds = [0., 0.5, 1.]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
ax.imshow(sleep.T, interpolation = "None", cmap = cmap, norm = norm, aspect = "auto")

plt.xlabel("Minutes")
plt.ylabel("Channel")
plt.title("Appropriate title goes here")

#save it to the the given filepath
plt.savefig(imagefile)
