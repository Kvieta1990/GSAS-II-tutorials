# -*- coding: utf-8 -*-
#makeGitTutorial.py
'''Make an index.html page to go into the Tutorials repository and 
another set of index.html pages to go into every data directory
'''
from __future__ import print_function
import os
import sys
import glob
import datetime
import tutorialIndex as G2G

script = sys.argv[0]
timestamp = datetime.datetime.ctime(datetime.datetime.now())
onlineVideos = []
'''a list of videos that are in box.com, since I don't know 
how to retrieve this automatically any more. 
'''
def makeDataIndex(datadir,title):
    '''Create an index.html file in the specified directory, 
    with a URL for each file in the directory. This is run on 
    every <tutorial>/data directory to provide web browser access to 
    the contents since GitHub does not offer allow directory views.
    '''
    fp = open(os.path.join(datadir,'index.html'),'w')
    fp.write(f'''<!-- Do not edit this file. It is created by makeGitTutorial.py --!>
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html><head><title>Data: {title}</title></head>
<center>
<img src="../../gsas2logo.png" align=right>
<H2>{title}<BR>Tutorial Exercise Files</H2>
</center>

<body>
Click on the links below to download each file
<UL>
''')
    for f in glob.glob(os.path.join(datadir,'*')):
        fil = os.path.split(f)[1]    
        if os.path.splitext(fil)[1].startswith('.htm'): continue
        fp.write(f'  <LI><A href="{fil}" download>{fil}</A></LI>\n')
    fp.write(f'''</UL>

<hr>
<address>created by {script}</address>
Last modified: {timestamp}
</body> </html>
''')
    fp.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('The location of the Tutorials repository must be supplied as an argument')
        sys.exit()
    TutorialsDir = sys.argv[1]
    if not os.path.exists(TutorialsDir):
        print(f'The specified Tutorials repository {TutorialsDir} does not exist')
        sys.exit()
    
    for url in '''
        https://anl.box.com/v/CalibrationofanareadetectorinG
        https://anl.box.com/v/CalibrationTutorial
        https://anl.box.com/v/CalibrationofaTOFpowderdiffrac
        https://anl.box.com/v/Combinedrefinement
        https://anl.box.com/v/TOFcombinedXNRietveldrefinemen
        https://anl.box.com/v/NeutronCWPowderData
        https://anl.box.com/v/FindProfParamCW
        https://anl.box.com/v/DeterminingWavelength
        https://anl.box.com/v/FitPeaks----
        https://anl.box.com/v/LaboratoryX-
        https://anl.box.com/v/FittingSmallAngleScatteringDat
        https://anl.box.com/v/FitBkgTut---
        https://anl.box.com/v/SmallAngleImageProcessing
        https://anl.box.com/v/Integrationofareadetectordatai
        https://anl.box.com/v/MerohedraltwinrefinementinGSAS
        https://anl.box.com/v/ParametricFitting
        https://anl.box.com/v/SequentialRefinementofSmallAng
        https://anl.box.com/v/SequentialTutorial
        https://anl.box.com/v/SimpleMagnetic
        https://anl.box.com/v/SimTutorial-
        https://anl.box.com/v/SmallAngleSizeDistribution
        https://anl.box.com/v/StackingFaults-I
        https://anl.box.com/v/StartingGSAS
        https://anl.box.com/v/Strainfittingof2DdatainGSAS-II
        https://anl.box.com/v/Textureanalysisof2DdatainGSAS-
        https://anl.box.com/v/TOFSequentialSinglePeakFit
        https://anl.box.com/v/RigidBodyRef
'''.split(): onlineVideos.append(url)
    
    tutURL = '' # URL of Tutorials directories, either absolute
                # or relative to the page being created here
    outname = os.path.join(TutorialsDir,'tutorials.html')

    dirList = [l[0] for l in G2G.tutorialIndex if len(l) >= 3]

    #import sys
    #out = sys.stdout
    out = open(outname,'w')
    print('<!-- Do not edit this file. It is created by makeGitTutorial.py from info in GSASIIctrlGUI.py --!>',file=out)
    print('''<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html><head>
<title>GSAS-II Tutorial Index</title>
</head><body>''',file=out)
    print('<img src="gsas2logo.png" align=right>',file=out)
    print('<h2>List of GSAS-II tutorials</H2><UL>',file=out)
    print('''
    <p> A list of available tutorials appears below. Each tutorial is a
    web page that can be opened using the link below, but most tutorials also need
    to have example data files downloaded. This can also be done with links included below, 
    but it can be easier to access tutorials using 
    <b>Help/Tutorials</b> menu item.
    When this menu entry is used from inside GSAS-II (unless "browse tutorial on web" is selected),
    the data files are downloaded to a local directory and GSAS-II will start from that directory
    for most file open commands. Most older tutorials have also been recorded as videos of the computer screen
    along with narration. Where videos are available, links are provided below. 
    </p>''',file=out)
    novideo = ''
    videocount = 0
    tutorialcount = 0
    videolist = '<UL>'
    for l in G2G.tutorialIndex:
        print('.', end='', flush=True)
        if len(l) == 1:
            print(f"</UL><h4>{l[0]}</H4><UL>",file=out)
        else:
            d = os.path.join(TutorialsDir,l[0])
            if not os.path.exists(d): continue
            tutorialcount += 1
            pageURL = tutURL+l[0]+'/'+l[1]
            dataURL = tutURL+l[0]+'/data'
            datadir = os.path.join(d,'data')
            suffix = ''
            if l[2][0] == ' ':
                suffix = ' <A href="#prereq">*</A>'
            if suffix: 
                print(f'<UL><LI><A href="{pageURL}">{l[2].strip()}</A>{suffix}',file=out)
            else:
                print(f'<LI><A href="{pageURL}">{l[2].strip()}</A>',file=out)
            
            # check for video tutorial
            videoName = f"{os.path.splitext(l[1])[0].replace(' ','')[:30]:-<12s}"
            vname = f'https://anl.box.com/v/{videoName}'
            if vname in onlineVideos:
                videocount += 1
                video = f'<A href="{vname}">video</A>'
                videolist += f'<LI><A href="{vname}">{l[2].strip()}</A></LI>\n'
            else:
                video =''
                novideo += f'\n{videoName:45s}{l[2]}'
            # check for data
            if os.path.exists(datadir):
                exampledata = f'<A href="{dataURL}" target="data">Exercise files</A>'
                makeDataIndex(datadir,l[2].strip())
            else:
                exampledata = ''
                #print(' [No exercise files].',file=out)
            if video and exampledata:
                print(f' [links: {video}, {exampledata}].',file=out)
            elif exampledata:
                print(f' [link: {exampledata}].',file=out)
            elif video:
                print(f' [link: {video}, no exercise files].',file=out)
            else:
                print(' [no example data or video].',file=out)
                
            if len(l) > 3:
                print("<blockquote><I>"+l[3]+"</I></blockquote>",file=out)
            if suffix: print('</UL>',file=out)
    #        if l[2][0] == ' ':
    #            print(' (Note that this tutorial requires previous as prerequisite)',file=out)

    videolist += '</UL>\n'
    print('</UL>\n<A name=prereq>* Indented tutorials require the previous unindented tutorial as a prerequisite',file=out)
    print('<h3>Tutorials with video-recorded examples</H3>', file=out)
    print(videolist, file=out)
    print("<P>The video tutorials are also <A href=https://pan.baidu.com/s/1C1jq1amfuVmcY2n91cQcsg> mirrored in China</A></P>",
                  file=out)
    print(f'''
<hr>
<address>created by {script}</address>
Last modified: {timestamp}
</body>
''',file=out)
    out.close()
    print(f"\nTutorials without videos {novideo}\n")

    for l in G2G.tutorialIndex:
        if len(l) != 1:
            if not os.path.exists(os.path.join(TutorialsDir,l[0])):
                print(f"Warning, directory {d} not found")
             
    # loop through directories in Tutorials repository
    for tutdir in glob.glob(os.path.join(TutorialsDir,'*')):
        if not os.path.isdir(tutdir): continue
        if tutdir in ['scripts','docs','webdocs','MDtutorials']:
            continue
        d = os.path.split(tutdir)[1]
        if d not in dirList: print(u"Tutorial directory not in GSASIIctrlGUI.tutorialIndex: "+d)
    print(f"\nStatistics: {tutorialcount} total tutorials, {videocount} with videos")
