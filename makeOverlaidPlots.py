import ROOT as r
import numpy as np


def buildLegend(canvas,x1=0.50, y1=0.60,x2=0.70,y2=0.8,textsize=0.025,separation=0.1,fill=0,border=0):
    #canvas.cd()
    legend = canvas.BuildLegend(x1,y1,x2,y2)
    legend.Draw()
    legend.SetTextSize(textsize)
    #legend.SetEntrySeparation(separation)
    #legend.SetFillStyle(fill)
    legend.SetFillColorAlpha(r.kGray,0.7)
    legend.SetBorderSize(border)

def read2DPlotsFromRootDir(infile, directory, keyword="none"):
    plots = {}
    rootdir = infile.Get(directory)
    rootdir.cd()
    for key in rootdir.GetListOfKeys():
        if "TH2" not in key.GetClassName():
            continue
        if keyword != "none":
            if keyword not in key.GetName():
                continue
        plot = rootdir.Get(key.GetName())
        name = plot.GetName().replace(" ","_").replace(".","")
        plot.SetName(name)
        plots[name] = plot

    return plots

def read1DPlotsFromRootDir(infile, directory, keyword="none"):
    plots = {}
    rootdir = infile.Get(directory)
    rootdir.cd()
    for key in rootdir.GetListOfKeys():
        if "TH1" not in key.GetClassName():
            continue
        if keyword != "none":
            if keyword not in key.GetName():
                continue
        plot = rootdir.Get(key.GetName())
        name = plot.GetName().replace(" ","_").replace(".","")
        plot.SetName(name)
        plots[name] = plot

    return plots

def format1DPlot(plot, name, title = "",linecolor = 1, linewidth = 2, linestyle = 1):
    plot.SetLineWidth(linewidth)
    plot.SetLineColor(linecolor)
    plot.SetLineStyle(linestyle)
    plot.SetName(name)
    if title != "":
        plot.SetTitle(title)
     


def overlay1DPlots(plots,canvas_name, plots_dir,legend_names = []):
    #statsbox formatting
    statspositions,height = getStatsYPositions(len(plots))

    ymax = -99999
    for i,plot in enumerate(plots):
        ymaxi = plot.GetMaximum()
        if ymaxi > ymax:
            ymax = ymaxi


    c = r.TCanvas("%s"%(canvas_name),"%s"%(canvas_name),1800,1000)
    c.cd()

    #set yaxis
    for i,plot in enumerate(plots):
        plot.GetYaxis().SetRangeUser(0.00001,ymax*1.1)
        if i < 1:
            plot.Draw("hist")
            setStatsBox(plot,ypos=statspositions[i],height=height,linecolor=colors[i])
        else:
            plot.Draw("histsames")
            setStatsBox(plot,ypos=statspositions[i],height=height,linecolor=colors[i])

    if len(legend_names) > 0:
        for i, plot in enumerate(plots):
            plot.SetTitle(legend_names[i])

    buildLegend(c)
    plots[0].SetTitle(canvas_name)
    c.SaveAs("%s/%s.png"%(plots_dir,canvas_name))
    #r.gPad.Update()
    c.Close()


def getStatsYPositions(nplots):
    start = 1.0
    end = 0.1
    height = (start-end)/nplots
    if height > 0.1:
        height = 0.1
    #ypositions = list(range(start,end,height))
    ypositions = np.arange(end,start,height)
    ypositions=np.flip(ypositions)
    print(ypositions)
    return ypositions,height

    
def setStatsBox(plot,xpos=0.9,ypos=0.9,height=0.2,width=0.1,linecolor=r.kBlack,color=r.kWhite,alpha=0.8):
    r.gPad.Update()
    stats = plot.GetListOfFunctions().FindObject("stats")
    stats.SetFillColorAlpha(color,alpha)
    stats.SetLineColor(linecolor)
    r.gStyle.SetStatY(ypos)
    r.gStyle.SetStatH(height)
    r.gStyle.SetStatW(width)
    r.gStyle.SetStatX(xpos)
    r.gPad.Update()

def savePlotAsPNG(plot, plot_dir, drawOptions=""):
    c = r.TCanvas(plot.GetName(),plot.GetName(),1800,900)
    c.cd()
    plot.Draw("%s"%(drawOptions))
    setStatsBox(plot,xpos=0.8,ypos=0.8)
    c.Update()
    c.SaveAs("%s/%s.png"%(plot_dir,plot.GetName()))
    #r.gPad.Update()
    c.Close()
            
colors = [r.kBlue, r.kGreen+2, r.kBlack, r.kOrange]
        

if __name__ == "__main__":
    main()

#################################################################################
def main():
    r.gROOT.SetBatch(1)
    plots_dir = 'overlay_plots'
    oldfile = r.TFile('/home/alic/HPS/projects/dqm/fit_shape_params/2019/hps_10030_evio_oldfitparams.root',"READ")
    newfile = r.TFile('/home/alic/HPS/projects/dqm/fit_shape_params/2019/hps_10030_evio_newfitparams_witht0shift.root',"READ")

    #svtpulse fits
    h_old = read1DPlotsFromRootDir(oldfile, "SVTPulseFits")
    hh_old = read2DPlotsFromRootDir(oldfile, "SVTPulseFits")

    h_new = read1DPlotsFromRootDir(newfile, "SVTPulseFits")
    hh_new = read2DPlotsFromRootDir(newfile, "SVTPulseFits")

    for name in h_old:
        canvasname = name.replace("half","").replace("module_","")
        plot1 = h_old[name]
        name1 = ("%s_%s"%(plot1.GetName(), "oldfitparams")).replace("half","").replace("module_","")

        plot2 = h_new[name]
        name2 = ("%s_%s"%(plot2.GetName(), "newfitparams")).replace("half","").replace("module_","")

        format1DPlot(plot1, name1,title=name1, linecolor=colors[0])
        format1DPlot(plot2, name2, title=name2, linecolor=colors[1])
        
        plots = [plot1, plot2]
        overlay1DPlots(plots,canvasname,plots_dir)


    h_old = {}
    h_new = {}

    h_old = read1DPlotsFromRootDir(oldfile, "Clusters")
    h_new = read1DPlotsFromRootDir(newfile, "Clusters")

    for name in h_old:
        canvasname = name.replace("half","").replace("module_","")
        plot1 = h_old[name]
        name1 = ("%s_%s"%(plot1.GetName(), "oldfitparams")).replace("half","").replace("module_","")

        plot2 = h_new[name]
        name2 = ("%s_%s"%(plot2.GetName(), "newfitparams")).replace("half","").replace("module_","")

        format1DPlot(plot1, name1,title=name1, linecolor=colors[0])
        format1DPlot(plot2, name2, title=name2, linecolor=colors[1])
        
        plots = [plot1, plot2]
        overlay1DPlots(plots,canvasname,plots_dir)
