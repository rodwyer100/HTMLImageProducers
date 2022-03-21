import ROOT as r
from ROOT import TCanvas,TH1F,TH2F,TH2D,TLegend,THStack
import os,sys,glob

import argparse

def makeHTML(outDir,filename,title,plots,branchnames,mode):#,selection):
    os.chdir(outDir)
    outfilebase = os.path.split(outDir)[1]
    f = open(filename+'.html',"w+")
    f.write("<!DOCTYPE html\n")
    f.write(" PUBLIC \"-//W3C//DTD HTML 3.2//EN\">\n")
    f.write("<html>\n")
    f.write("<head><title>"+ title +" </title></head>\n")
    f.write("<body bgcolor=\"EEEEEE\">\n")
    f.write("<table border=\"0\" cellspacing=\"5\" width=\"100%\">\n")
    for i in range(0,len(plots)):
        pname = ""
        offset = 1
        if i==0 or i%2==0: f.write("<tr>\n")
        if mode==0:
		f.write("<td width=\"10%\"><a target=\"_blank\" href=\"" + plots[i] + "\"><img src=\"" + plots[i] + "\" alt=\"" + plots[i] + "\" title=\"" + pname + "\" width=\"85%\" ></a></td>\n")
        if mode==1:
		if plots[i][len(plots[i])-1]=="l":
			f.write("<td width=\"10%\"><a target=\"_blank\" href=\"" + plots[i] + "\">"+branchnames[i]+"</a></td>\n")	
		else:
			f.write("<td width=\"10%\"><a target=\"_blank\" href=\"" + plots[i] + "\"><img src=\"" + plots[i] + "\" alt=\"" + plots[i] + "\" title=\"" + pname + "\" width=\"85%\" ></a></td>\n")	
	if i==offset:
            f.write("</tr>\n")
        elif (i>offset and (i-offset)%2==0) or i==len(plots):
            f.write("</tr>\n")

    f.write("</table>\n")
    f.write("</body>\n")
    f.write("</html>")
    f.close()
    path_parent=os.path.dirname(os.getcwd())
    os.chdir(path_parent)


parser = argparse.ArgumentParser(description="The baseConfig options for plotHistDir")

parser.add_argument("-i","--inFileBase",type=str,dest="inf",action='store',help="input file base, use when files are in the same directory", default=None)
parser.add_argument("-o","--outFileBase",type=str,dest="outf",action='store',help="Generates Pictures and HTML Webpage Here", default=None)
parser.add_argument("-r","--ratioEnable",type=int,dest="ratio",action='store',help="Enables Ratio Curves", default=0)
parser.add_argument("-mc","--mcFileBase",type=str,dest="mc",action='store',help="Enables MC and Takes in Curves", default="Nope")
parser.add_argument("-l","--list",nargs=4,type=float,dest="leglist",action='store',help="Relocates the Legend",default=[.73,.32,.97,.53])

options = parser.parse_args()
inf=options.inf
outf=options.outf
R=(options.ratio==1)#or(not(options.mc=='Nope'))
MC=options.mc
leglist=options.leglist
print(leglist)
#treeNum=options.treeNum
#branchNum=options.branchNum

colors = [r.kBlack,r.kRed,r.kBlue,r.kGreen+2,r.kOrange-2]
#legends=["",""]

#print(os.listdir(inf))

inFileList=os.listdir(inf)
if (not(options.mc=='Nope')):
	mcFileList=os.listdir(MC)
if R:
	inFileList=inFileList[:2]
r.gROOT.SetBatch(1)

DFS=r.TFile(inf+"/"+inFileList[0])#DirectoryForSize
SubDirs=[DFS.Get(DFS.GetListOfKeys().At(i).GetName()) for i in range(0,len(DFS.GetListOfKeys()))]
SubDirNames=[DFS.GetListOfKeys().At(i).GetName() for i in range(0,len(DFS.GetListOfKeys()))]
BranchNames=[[SubDirs[i].GetListOfKeys().At(j).GetName() for j in range(len(SubDirs[i].GetListOfKeys()))] for i in range(len(SubDirs))]
#OneD=[]
for i in range(len(DFS.GetListOfKeys())):
	OneD=[]
	for  j in range(len(SubDirs[i].GetListOfKeys())):
		#print(BranchNames[i][j])
		c=r.TCanvas()
		leg = TLegend(leglist[0],leglist[1],leglist[2],leglist[3])#TLegend(.73,.32,.97,.53)
		DFSnow=r.TFile(inf+"/"+inFileList[0])
		Entry=DFSnow.Get(SubDirNames[i]+"/"+BranchNames[i][j])	
		is2d=(type(Entry)==TH2D)
		#print(is2d)
		try:
			if (not(is2d))and(not(options.mc=='Nope')):
				ths1=THStack(BranchNames[i][j],BranchNames[i][j])
				for I in range(len(mcFileList)):
					DFSnow=r.TFile(MC+"/"+mcFileList[I])
					Entry=DFSnow.Get(SubDirNames[i]+"/"+BranchNames[i][j])
					Entry.SetDirectory(0)
					ths1.Add(Entry)
				ths1.Draw("stack")
				print("hello")
		except:
			print("Failed at "+BranchNames[i][j])
		if R and not(is2d):
			c.Divide(1,2)
			c.cd(1)		
		for I in range(len(inFileList)):
			DFSnow=r.TFile(inf+"/"+inFileList[I])
			Entry=DFSnow.Get(SubDirNames[i]+"/"+BranchNames[i][j])	
			if is2d:
				Entry.SetTitle(inFileList[I])
				Entry.Draw("colz")
				c.Print(outf+"/pic"+str(i)+"_"+str(j)+"_"+str(I)+".png","png")
				c.Clear()
				continue
			Entry.SetDirectory(0)
			Entry.SetLineColor(colors[I%5])
			if options.mc=='Nope':
				leg.AddEntry(Entry,inFileList[I],"L")
			Entry.Draw("colz same")
		try:
			if R and not(is2d):
				c.cd(2)
				f1=r.TFile(inf+"/"+inFileList[0])
				Entry1=f1.Get(SubDirNames[i]+"/"+BranchNames[i][j])
				Entry1.SetDirectory(0)
				f2=r.TFile(inf+"/"+inFileList[1])
				Entry2=f2.Get(SubDirNames[i]+"/"+BranchNames[i][j])
				Entry2.Divide(Entry1)
				#print("hello")
				Entry2.Draw("colz")
		except:
			print("Failed on 1D Histogram for "+BranchNames[i][j])
		if is2d:	
			makeHTML(outf,BranchNames[i][j],BranchNames[i][j],["pic"+str(i)+"_"+str(j)+"_"+str(I)+".png" for I in range(len(inFileList))],[],0)
			print("hello")
			OneD.append(0)
		else:
			leg.Draw()
			c.Print(outf+"/"+BranchNames[i][j]+".png","png")
			c.Clear()
			OneD.append(1)
	filetype=[".html",".png"]
	#ThreeD=OneD
	#print(OneD)
	#print(len(BranchNames[0]))
	print([BranchNames[i][j]+"_"+str(OneD[j])+"_"+filetype[OneD[j]] for j in range(len(BranchNames[i]))])
	makeHTML(outf,SubDirNames[i],SubDirNames[i],[BranchNames[i][j]+filetype[OneD[j]] for j in range(len(BranchNames[i]))],BranchNames[i],1)
makeHTML(outf,"master","Master",[SubDirNames[i]+".html" for i in range(len(SubDirNames))],SubDirNames,1)
