# 
#note
# adjust fontsize of axes label and ticks 
# ax.legend(loc=1,fontsize=fontsize)
# ax.set_xscale("log"）;ax.set_ylabel("$t^*_s$",fontsize=fontsize)
# ax.tick_params(axis='both', which='major', labelsize=fontsize)
#ax.set_xlabel('Time(s)')
#ax.xaxis.tick_top()
#ax.xaxis.set_label_position('top')
# set ticks    
# ax[row,col].set_yticks([0.0,0.05,0.08])
# https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure 
# set common label of x and y for sharex and sharey
#fig.text(-0.05, 0.5, "$t^*_s$",fontsize=fontsize+10, va='center', rotation='vertical')
#fig.text(0.5, -0.02, "Hypocentral distance (km)",fontsize=fontsize+10, ha='center')
#
# ax.annotate(staname, xy=(0.05, 0.9), xycoords='axes fraction',fontsize=fontsize,\
#                                bbox=dict(boxstyle='round,pad=0.5', fc='gray', ec='k',lw=1 ,alpha=0.4))

# np array sorted and find some elements in array
# index=np.nonzero( (dist<12) & (dist>10)) # <==> dist[np.where( (dist<11) & (dist<10))]  & is bit wise operation
# tt=tmp[:,0]
# tmp1=np.squeeze(tmp[index,:]) 
#  order by tstar value
# ind=np.lexsort(tmp1[:,::-1].T)
# tmp2=tmp1[ind];flag='sorted'


'''
import sys
sys.path.append("/home/hj/pythonModule/")
from utility import (readMOD,Qcolorbar,projectEvent,InterpolateNewGrid,Meshgrid_MOD,extractXYZPlane,
                     imshow_plot,Addshadow,AddContour)

'''
from matplotlib.colors import Normalize
from matplotlib import pyplot as plt
from obspy import UTCDateTime
import numpy as np
def readMOD(MODfile):
    with open(MODfile,"r") as f:
        MOD = f.read().splitlines()
        bld,nx,ny,nz = MOD[0].split()
        nx = int(nx); ny = int(ny); nz = int(nz) 
        X = MOD[1].split();X=np.array(list(map(float,X)))
        Y = MOD[2].split();Y=np.array(list(map(float,Y)))
        Z = MOD[3].split();Z=np.array(list(map(float,Z)))
    vpvs=[]
    for line in MOD[4:]:
        temp=list(map(float,line.split()))
        vpvs.append(temp)
    vpvs=np.array(vpvs)
    Vp=vpvs[0:ny*nz]
    if len(vpvs)-ny*nz>10:
        VpsRatio=vpvs[ny*nz:ny*nz+ny*nz]
    else:
        VpsRatio=np.ones((ny*nz,nx))*1.73
    return X,Y,Z,Vp,VpsRatio

def readSegTime(segTimefile):
    '''
    for tomoTDD, the segTimefile should be seg, UTCDate,UTCDate,duration.
    '''
    with open(segTimefile,'r') as f:
        temp=f.read().splitlines()
        period={}
        for line in temp:
            seg,t1,t2,dt=line.split()
            year1=str(UTCDateTime(t1).year);year2=str(UTCDateTime(t2).year)
            mon1=str(UTCDateTime(t1).month);mon2=str(UTCDateTime(t2).month)
            day1=str(UTCDateTime(t1).day);  day2=str(UTCDateTime(t2).day)
            period[seg]=["/".join([year1,mon1,day1]),"/".join([year2,mon2,day2])]
    return period

def Meshgrid_MOD(X,Y,Z,dx=0.1,dy=0.1,dz=0.1,plane='Z'):    
    xnew = np.arange(X[1], X[-2]+dx, dx)
    ynew = np.arange(Y[1], Y[-2]+dy, dy)
    znew = np.arange(Z[1], Z[-2]+dz, dz)
    # xxo==>xx_old; xxn==>xx_new
    if plane=='Y' or plane=='y':
        xxo, zzo = np.meshgrid(X[1:-1], Z[1:-1]) 
        xxn, zzn = np.meshgrid(xnew, znew)
        return xxo, zzo, xxn, zzn
    if plane=='X' or plane =='x':
        yyo, zzo = np.meshgrid(Y[1:-1], Z[1:-1]) 
        yyn, zzn = np.meshgrid(ynew, znew)
        return yyo,zzo,yyn,zzn
    if plane =='Z' or plane=='z':
        xxo, yyo = np.meshgrid(X[1:-1], Y[1:-1])
        xxn, yyn = np.meshgrid(xnew, ynew)
        return xxo,yyo,xxn,yyn

def extractXYZPlane(model,X,Y,Z,x=None,y=None,z=None,plane='Y'):
    '''
    model: dimentsion (nx,ny*nz) 
    X: node position along x direction, 1-D array
    Y: node position along y direction, 1-D array
    Z: node position along z direction, 1-D array
    x,y,z: the selected plane whose poisiton along X/Y/Z direction is close x/y/z,respectively
    '''
    Xplane,Yplane,Zplane = [],[],[]
    nx=len(X);ny=len(Y);nz=len(Z)
    if plane=='Z' and z != None:
        for i in range(1,nz-1):
            if np.abs(Z[i]-z)<0.0001:
                index1 = i*ny+1; index2 = (i+1)*ny-1
                Zplane = model[index1:index2,1:nx-1]
    if plane=='Y' and y != None:
        for i in range(1,ny-1):
            if np.abs(Y[i]-y)<0.0001:
                Yplane= model[i+ny:-ny-1:ny,1:nx-1]
    if plane=='X' and x != None:
        for i in range(1,nx-1):
            if np.abs(X[i]-x)<0.0001:
                Xplane = model[:,i].reshape((nz,ny))
                Xplane = Xplane[1:-1,1:-1]
    return Xplane,Yplane,Zplane

def InterpolateNewGrid(ModelPlane,xxo=None,yyo=None,zzo=None,xxn=None,yyn=None,zzn=None,plane='Z',method='cubic'):
    '''
    ModelPlane: 2-D array, the plane would be XY, XZ, or YZ
    xxo,yyo,zzo: meshgrid for original X,Y,Z
    xxn,yyn,zzn: meshgrid for interpolated X,Y,Z
    xxo,yyo,zzo,xxn,yyn,zzn see meshgrid_MOD
    '''
    from scipy.interpolate import griddata,interp2d    
    temp_model = ModelPlane.flatten().T
    if method not in ['linear', 'nearest', 'cubic']:
        print('Interpolation method must be linear, nearest or cubic !!!!!!')
    if plane=='Y' or plane=='y':
        temp = np.array([xxo.flatten(),zzo.flatten()]).T
        ModelPlane_new=griddata(temp, temp_model,(xxn, zzn), method=method)
    if plane=='X' or plane == 'x':
        temp = np.array([yyo.flatten(),zzo.flatten()]).T
        ModelPlane_new=griddata(temp, temp_model,(yyn, zzn), method=method)
    if plane=='Z' or plane=='z':
        temp = np.array([xxo.flatten(),yyo.flatten()]).T
        ModelPlane_new=griddata(temp, temp_model,(xxn, yyn), method=method)
    return ModelPlane_new

def projectfun(evx,xi,evy,evz,mag,dist=2):
    '''
    events within dist km of a layer are selected for this layer
    '''
    index_store = []
    for ii in range(len(evx)):
        if evx[ii]<=xi+dist and evx[ii]>=xi-dist:  #within xx km of this layer
              index_store.append(ii)
        evy_pro = evy[index_store]
        evz_pro = evz[index_store]
        mag_pro=mag[index_store]
    return evy_pro,evz_pro,mag_pro
def readRelocFile(eventfile,flag="One",seg1="801",seg2="802"):
    '''
    tomodd reloc file would be read. (tomoDD or tomoTDD)
    '''
    import numpy as np
    reloc  = np.loadtxt(eventfile)
    evx = reloc[:,4]/1000
    evy = reloc[:,5]/1000
    evz = reloc[:,3]
    mag=reloc[:,16]
    if flag=="One":
        return evx,evy,evz,mag
    elif flag=="Two": # two periods
        seg_flag =np.array([c[0:3]  for c in list(map(str,reloc[:,0]))])
        mask_array1=np.where(seg_flag==seg1)
        mask_array2=np.where(seg_flag==seg2)
        evx1 = evx[mask_array1];evx2 = evx[mask_array2]
        evy1 = evy[mask_array1];evy2 = evy[mask_array2]
        evz1 = evz[mask_array1];evz2 = evz[mask_array2]
        mag1 = mag[mask_array1];mag2 = mag[mask_array2]
        return [evx1,evy1,evz1,mag1],[evx2,evy2,evz2,mag2]

def projectEvent(evx,evy,evz,mag,xi=1,yi=1,zi=1,dist=2,plane="Z"):
    '''
    projectEvent(evx,evy,evz,mag,xi=1,yi=1,zi=1,dist=2,plane="Z")
    
    '''
    evx_pro=[];evy_pro=[];evz_pro=[];mag_pro=[]
    if plane=="X":
        evy_pro,evz_pro,mag_pro=projectfun(evx,xi,evy,evz,mag,dist)
    if plane=="Y":
        evx_pro,evz_pro,mag_pro=projectfun(evy,yi,evx,evz,mag,dist)
    if plane=="Z":
        evx_pro,evy_pro,mag_pro=projectfun(evz,zi,evx,evy,mag,dist)
    return evx_pro,evy_pro,evz_pro,mag_pro

def readTomoDDCatalog(CatalogFile):
    '''
    read HypoDD Catalog file 
    
    return a EVE dictionary. event ID is the key
    
    EVE include lon lat dep mag time1 time2
    
    time1 and time2 is first entry and second entry of a row of Catalog file.
    
    '''
    with open(CatalogFile,"r") as f:
        EVE={}
        for line in f:
            para=line.split()
            time1,time2,evid,lon,lat,dep,mag=para[0],para[1],para[9],para[3],para[2],para[4],para[5]
            EVE[evid]=list(map(float,[lon,lat,dep,mag,time1,time2]))
    return EVE

def readTomoDDStations(StationFile):
    '''
    read a station file
    return STA dictionary including lon lat dep 
    '''
    with open(StationFile,"r") as f:
        STA={}
        for line in f:
            para=line.split()
            staname,lat,lon,dep=para
            STA[staname]=[float(lon),float(lat),-float(dep)/1000]
    return STA

def readTTime(filename):
#     '''
#     filename="./tstar_SMw2.0.dat"
#     timeInfo=readTTime(filename)
#     '''
    with open(filename,"r") as f:
        timeInfo={}
        for line in f:
            tmp=line.split()
            if tmp[0]=="#":
                evid=tmp[1]
            else:
                staname,dt,qual,phase=tmp[0],tmp[1],tmp[2],tmp[3]
                key="_".join([evid,staname])
                timeInfo[key]=[float(dt),float(qual),phase]
    return timeInfo

def calDistance(lon1,lat1,ele1,lon2,lat2,ele2):
    '''
    lon1: evlon; lat1: evlat
    lon2: stalon; lat2: stalat
    '''
    dlat=lat1-lat2
    dlon=lon1-lon2
    pi=3.1415926
    dist=np.sqrt((dlat*111)**2 + (dlon*(np.cos(lat1*pi/180)*111))**2 + (ele1-ele2)**2 ) #km
    return dist  

def readTTAndDistForOneStation(TomoDDAbsoluteFile,EVE,STA):
    '''
    read a tomodd absolute file and combine EVE and STA information to calculate distance and az 
    
    return a dictionary
        absTT_dist[staname]=[tt,dist,baz,stalat,stalon,stadep,evelon,evelat,evedep,mag,time1,time2,evid]
    '''
    from obspy.clients.iris import Client
    import obspy.geodetics.base as base 
    with open(TomoDDAbsoluteFile,"r") as f:
        absTT_dist={}
        for line in f:
            para=line.split()

            if para[0]=="#":
                evid=para[1]
                if evid not in EVE:
                    continue
                evelon,evelat,evedep,mag,time1,time2=EVE[evid]
                
            else:
                staname=para[0]
                if staname not in STA:
                    continue
                stalon,stalat,stadep=STA[staname]
                tt=float(para[1])
                fit=para[2]
                phase=para[3]

                dist =calDistance(evelon,evelat,evedep,stalon,stalat,stadep)
#                 result = Client().distaz(stalat,stalon,  evelat,evelon)
#                 baz=result['backazimuth'];
                dis,az,baz=base.gps2dist_azimuth(stalat,stalon,evelat,evelon)
#                 print(baz)
                if staname in absTT_dist:
                    absTT_dist[staname].append([tt,dist,baz,stalat,stalon,stadep,evelon,evelat,evedep,mag,time1,time2,int(evid)]) 
													# all elemets must be a numbers, not including string
                else:
                    absTT_dist[staname]=[]
                    absTT_dist[staname].append([tt,dist,baz,stalat,stalon,stadep,evelon,evelat,evedep,mag,time1,time2,int(evid)])
    return  absTT_dist

def readTrace(filename):
    import obspy
    trace=obspy.read(filename)[0].taper(max_percentage=0.05).detrend().filter("bandpass",freqmin=0.5,freqmax=23)
    sacHeader=trace.stats.sac
    origtime=sacHeader.o
    ptime=sacHeader.a
    stime=sacHeader.t0
    baz=sacHeader.baz
    staname=sacHeader.kstnm
    beginTime=sacHeader.b
    npts=trace.stats.npts
    delta=trace.stats.delta
    timeaxis=np.arange(0,int(npts/3))*delta
    data= trace.data[0:int(npts/3)]
    data=data/np.max(np.absolute(data))
    time=[beginTime,origtime,ptime,stime]
    return timeaxis,data,time
def plotFittingSpectraAndWaveform(evid,staName,Waveform,SpectraInfo,FittingInfo):
    '''
for key in RayTstarInfo:
    print(key)
    evid,staName=key.split('_')
    tmp=RayTstarInfo[key]
    FittingInfo=tmp[0]
    Waveform=tmp[1]
    SpectraInfo=tmp[2]
    plotFittingSpectraAndWaveform(evid,staName,Waveform,SpectraInfo,FittingInfo)

    '''
    import matplotlib.pyplot as plt
    import matplotlib.ticker
    timeaxis=Waveform[0]
    data = Waveform[1]
    time=Waveform[2]
    Freqs=SpectraInfo[0]
    Spectra=SpectraInfo[1]
    tstar=FittingInfo[0]
    fc=FittingInfo[1]
    omega=FittingInfo[2]
    fit1,fit2=FittingInfo[3]
    
    
    fontsize=20
    plt.figure(10,figsize=(6,7),clear=True)
    ax=plt.subplot2grid((4,1),loc=(0,0),colspan=1,rowspan=1)
    plt.plot(timeaxis,data,'-k')
    plt.plot([time[3],time[3]],[-0.5,0.5],'-',color='orange',linewidth=2,label='S pick')
    plt.plot([time[3]-0.2,time[3]+1.28-0.2],[0.8,0.8],'-r',linewidth=2,label='Signal')
    plt.plot([time[3]-1.5,time[3]+1.28-1.5],[0.8,0.8],'-b',linewidth=2,label='Noise')
    ax.set_xlabel('Time(s)',fontsize=fontsize)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.set_yticks([-1,0,1])
    ax.annotate("{}".format(staName),(0.1,0.6), bbox=dict(boxstyle='round,pad=0.5', fc='gray', ec='k',lw=1 ,alpha=0.4),fontsize=fontsize)
    ax.annotate("{}".format(evid),(0.1,-0.6), bbox=dict(boxstyle='round,pad=0.5', fc='gray', ec='k',lw=1 ,alpha=0.1),fontsize=fontsize)
    ax.tick_params(axis='both', which='major', labelsize=fontsize)
    plt.legend(fontsize=fontsize-2)

    ax.set_ylabel('Amplitude',fontsize=fontsize)
    # plt.legend()
    # ax.set_position([0.0,0.5,0.2,0.9])
    ax=plt.subplot2grid((4,1),loc=(1,0),colspan=1,rowspan=3)
    plt.plot(Freqs,Spectra[:,0],'.',color='blue',markersize=5,label='Noise')
    plt.plot(Freqs,Spectra[:,1],'--',color='black',linewidth=2,label='Obs')
    plt.plot(Freqs,Spectra[:,2],'-',color='red',linewidth=2,label='Syn')
    plt.legend(fontsize=fontsize-2,loc=4)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylabel("Spectra",fontsize=fontsize)
    ax.set_xlabel("Frequency (Hz)",fontsize=fontsize)
    ax.set_xticks([1,2,5,10,20])
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    # text station name
    ax.annotate("$t^*$={:.4f}\n$f_c$={:.1f}\n$\Omega_0$={:.0f}\nfit={}\nrms={:.3f}".format(tstar,fc,omega,fit1,float(fit2)),(0.01,0.06),xycoords='axes fraction',fontsize=fontsize)
    ax.tick_params(axis='both', which='major', labelsize=fontsize)

    plt.tight_layout(pad=-0.8)
    plt.savefig('./Figure_Fitting/{}_{}'.format(evid,staName),dpi=300,bbox_inches='tight')
#     plt.pause(0.1)
    plt.clf()
    # plt.show()


def keyToPath(key):
    ev1,ev2,sta1,sta2=key.split('_')
    path1=ev1+"_"+sta1
    path2=ev1+"_"+sta2
    path3=ev2+"_"+sta1
    path4=ev2+"_"+sta2
    return path1,path2,path3,path4

def readDtstar(filename,threshold=0.7):
    dtInfo=[]
    count=1
    key_total=[]
    qual_total={}
    raypath=[]
    RayPathCount={}
    with open(filename,"r") as f:
        for line in f:
            _,ev1,ev2,sta1,sta2,dt,qual,_=line.split()
            key="_".join([ev1,ev2,sta1,sta2])
            dt=float(dt);qual=float(qual)
            path1,path2,path3,path4 = keyToPath(key)
            if qual>threshold:
                key_total.append(key)
                qual_total[key]=qual
                dtInfo.append([key,float(dt),float(qual)])
                if path1 not in raypath:
                    raypath.append(path1)
                    RayPathCount[path1]=1
                else:
                    RayPathCount[path1]+=1
                
                if path2 not in raypath:
                    raypath.append(path2)
                    RayPathCount[path2]=1
                else:
                    RayPathCount[path2]+=1
                
                if path3 not in raypath:
                    raypath.append(path3)
                    RayPathCount[path3]=1
                else:
                    RayPathCount[path3]+=1
                
                if path4 not in raypath:
                    raypath.append(path4)
                    RayPathCount[path4]=1
                else:
                    RayPathCount[path4]+=1
                
            count=count+1
    print(count,filename)
    return dtInfo,key_total,qual_total,raypath,RayPathCount



def extractEachIterationInformation(filename,ny,nz,path):
    '''
    filename: tomodd.vel file format
    ny, nx: the number of nodes for x and y direction, respectively. 
    path:  the path you choosed to store files.
    extractEachIterationInformation('tomodd.vel.seg.803',ny=19,nz=9,path='./')
    #button P velocioty
            if tmp[0]=="P-wave" and tmp[1] =="velocity" and tmp[2]=="at" and tmp[3]== "iteration:":
                print(line)
                itVel_P+=1;start=1;countline=0
                fid=open("vel_p"+str(itVel_P),"w")
                fid_total.append(fid)             
                
    #button for S velocity     
            if tmp[0]=="S-wave" and tmp[1] =="velocity" and tmp[2]=="at" and tmp[3]== "iteration:":
                print(line)
                itVel_S+=1; start=1;countline=0
                fid=open("vel_s"+str(itVel_S),"w")
                fid_total.append(fid)
    Because different versions of tomoDD, the velocity output is not a single line for x direction. 
    this code block requires that the velocity values for x direction in one line, instead of multiple lines.
    Now, for the new version of tomoDD_ESDP tomoDD_ESDP_Q tomoDD_ESDP_TD program, this code block can be used 
    to extract velocity values for each iteration.
BEGIN{
  iter = 8;
  ny =19 ;
  nz =9;
  i = 0;
  start = 0;
}
{
  if(start==1 && i==iter){
     j=j+1;
#     print(j)

     if(j>=1 && j<=ny*nz){
        print $0 >name;
     }
     else{
        start=0;
     }
  }

  if($3=="DWS" && $2=="P-wave"){
     start=1;
     i=i+1;
     name="DWS_P";
     j=0;
     # output the next ny*nz lines.
  }
#  if($3=="DWS" && $2=="S-wave"){
#     start=1;
#     #i=i+1;
#     name="DWS_S";
#     j=0;
#     # output the next ny*nz lines.
#  }
}
END{

}
    '''  
    with open(filename,'r') as f:
        itDWS_P=0;itDWS_S=0;itVel_P=0;itVel_S=0
        fid_total=[];start=0
        for line in f:
            tmp=line.split()
            if len(tmp)>3:
                if start==1:
                    if countline>=0 and countline<ny*nz:
                        fid.write(line)
                        countline=countline+1
                    else:
                        start=0
                # button for P DWS    
                if tmp[0]=="Output" and tmp[1] =="P-wave" and tmp[2]=="DWS" and tmp[3]== "values":
                    print(line)
                    itDWS_P+=1;start=1;countline=0
                    fid=open(path+"DWS_P"+str(itDWS_P),"w")
                    fid_total.append(fid)
                    print(path+"DWS_S"+str(itDWS_P))
                # button for S DWS  
                if tmp[0]=="Output" and tmp[1] =="S-wave" and tmp[2]=="DWS" and tmp[3]== "values":
                    print(line)
                    itDWS_S+=1;start=1;countline=0
                    fid=open(path+"DWS_S"+str(itDWS_S),"w")
                    fid_total.append(fid)
        for fid in fid_total:
            fid.close()

def get_resolvebility_new(X,Y,Z,m_rec,m_true,radius=2):
    # + + + + +  
    # + - - - +
    # + - + - +   -s are selected nodes for radius equal to 1
    # + - - - +
    # + + + + + 
    # we select two neighbouring nodes in each direction centring the calculated node
    chk_rec=  m_rec
    chk_true= m_true
    nz=len(Z);ny=len(Y);nx=len(X)
    resolvebility=np.zeros((ny*nz,nx))
    for k in range(1,nz-1): 
        for j in range(1,ny-1):
            index1=k*ny+j
            for i in range(1,nx-1):
                index2=i
                temp1=[]
                temp2=[]
                for jj in range(1,ny-1):
                    index11 = k*ny+jj
                    dy=np.absolute(jj-j)
                    for ii in range(1,nx-1):
                        index22=ii
                        dx=np.absolute(ii-i)
                        if dx <=radius and dy <=radius:
                            temp1.append((chk_rec[index11,index22]+chk_true[index11,index22])**2)
                            temp2.append(chk_rec[index11,index22]**2+chk_true[index11,index22]**2)
                temp1=np.array(temp1).sum()
                temp2=2*np.array(temp2).sum()
                resolvebility[index1,index2]=temp1/temp2
    return resolvebility

def get_resolvebility(vp_rec_file,MODfile_Inv,MODfile_Syn,radius=2):
    # + + + + +  
    # + - - - +
    # + - + - +   -s are selected nodes for radius equal to 1
    # + - - - +
    # + + + + + 
    # we select two neighbouring nodes in each direction centring the calculated node
    import numpy as np
    import sys
    sys.path.append("/home/hj/pythonModule")
    from utility import readMOD
    X,Y,Z,Vp,VpsRatio=readMOD(MODfile_Inv) # Vp is initial model used for inversion
    vp_rec = np.loadtxt(vp_rec_file)   # vp_rec is the recovered model  
    X,Y,Z,vp_true,VpsRatio=readMOD(MODfile_Syn)  # vp_true is the model to synthetize data
    chk_rec= vp_rec-Vp
    chk_true=vp_true-Vp 
    nz=len(Z);ny=len(Y);nx=len(X)
    resolvebility=np.zeros((ny*nz,nx))
    for k in range(1,nz-1): 
        for j in range(1,ny-1):
            index1=k*ny+j
            for i in range(1,nx-1):
                index2=i
                temp1=[]
                temp2=[]
                for jj in range(1,ny-1):
                    index11 = k*ny+jj
                    dy=np.absolute(jj-j)
                    for ii in range(1,nx-1):
                        index22=ii
                        dx=np.absolute(ii-i)
                        if dx <=radius and dy <=radius:
                            temp1.append((chk_rec[index11,index22]+chk_true[index11,index22])**2)
                            temp2.append(chk_rec[index11,index22]**2+chk_true[index11,index22]**2)
                temp1=np.array(temp1).sum()
                temp2=2*np.array(temp2).sum()
                resolvebility[index1,index2]=temp1/temp2
    return resolvebility

def get_resolvebilityTD(vp_rec,vp_true,X,Y,Z,radius=2):
    # + + + + +  
    # + - - - +
    # + - + - +   -s are selected nodes for radius equal to 1
    # + - - - +
    # + + + + + 
    # we select two neighbouring nodes in each direction centring the calculated node
    import numpy as np
    chk_rec= vp_rec
    chk_true=vp_true
    nz=len(Z);ny=len(Y);nx=len(X)
    resolvebility=np.zeros((ny*nz,nx))
    for k in range(1,nz-1): 
        for j in range(1,ny-1):
            index1=k*ny+j
            for i in range(1,nx-1):
                index2=i
                temp1=[]
                temp2=[]
                for jj in range(1,ny-1):
                    index11 = k*ny+jj
                    dy=np.absolute(jj-j)
                    for ii in range(1,nx-1):
                        index22=ii
                        dx=np.absolute(ii-i)
                        if dx <=radius and dy <=radius:
                            temp1.append((chk_rec[index11,index22]+chk_true[index11,index22])**2)
                            temp2.append(chk_rec[index11,index22]**2+chk_true[index11,index22]**2)
                temp1=np.array(temp1).sum()
                temp2=2*np.array(temp2).sum()
                resolvebility[index1,index2]=temp1/temp2
    return resolvebility


def velcolorbar(ax,axim,ticks,cbwidth="5%",pad=0.05,format="%2.1f",orientation='vertical'):
    from matplotlib import pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size=cbwidth, pad=0.05)
    cb=plt.colorbar(axim,cax=cax,ticks=ticks,format=format, orientation=orientation ) 
    cb.ax.set_title('Vp(km/s)',fontsize=18,pad=16,fontweight='bold')
    cb.ax.tick_params(axis='both', which='major', labelsize=18)              
# cb=plt.colorbar(im, ticks=np.linspace(vmin,vmax,5),shrink=scale,pad=0.02,format="%2.1f")
# cb.ax.get_yaxis().labelpad = pad
# cb.ax.set_yticklabels(["{:.1f}".format(i) for i in np.linspace(vmin,vmax,5)])
# cb.set_label('Vp(km/s)', rotation=270,fontsize=fontsize)
    return cb


def Qcolorbar(ax,axim,ticks=None,name='1000/Qp',cbwidth="5%",pad=0.05,format="%2.1f",orientation='vertical'):
    from matplotlib import pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    if name[0:2] in ["Vp","Vs"]:
        format="%2.1f" 
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size=cbwidth, pad=0.05)
    cb=plt.colorbar(axim,cax=cax,ticks=ticks,format=format, orientation=orientation ) 
    #cb.ax.set_title(name,pad=16)#,fontweight='bold')#,fontsize=18)
    #cb.set_label(name)
    cb.ax.set_ylabel(name,labelpad=None)
    cb.ax.tick_params(axis='both', which='major')#, labelsize=18)              
# cb=plt.colorbar(im, ticks=np.linspace(vmin,vmax,5),shrink=scale,pad=0.02,format="%2.1f")
# cb.ax.get_yaxis().labelpad = pad
# cb.ax.set_yticklabels(["{:.1f}".format(i) for i in np.linspace(vmin,vmax,5)])
# cb.set_label('Vp(km/s)', rotation=270,fontsize=fontsize)
    return cb

def Addshadow(ModelSlice,ResSlice,cmin,cmax,MinReso=100,shadow_par=0.8,cmap=plt.cm.jet):
# default colormap:jet

    alphas = np.nan_to_num(ResSlice)
    alphas[alphas<MinReso]= shadow_par
    alphas[alphas>=MinReso]=1
    colors = Normalize(cmin,cmax,clip=True)(ModelSlice)
    colors = cmap(colors)
    colors[..., -1] = alphas
    ModelSlice=colors
    return ModelSlice

def AddContour(ax,xx,yy,ModelSlice,ctrline=None,colors='w',linewidth=4):
    ax.contour(xx,yy,ModelSlice,ctrline,colors=colors,linewidths=linewidth)
    return ax

def imshow_plot(ax,ModelSlice,xmin,xmax,ymin,ymax,region,
                plotev=None,ticks=None,clim=None,colormap='jet',label=None):
 
    im=plt.imshow(ModelSlice,cmap=colormap,interpolation="bilinear", origin="lower", extent=[xmin,xmax,ymin,ymax])
    if clim!=None:
        plt.clim(clim)
    if label!=None:
        if label['title']!="":
            plt.title(label['title'])
        if label['xlabel']!=None:
            plt.xlabel(label['xlabel'])
        if label['ylabel']!=None:
            plt.ylabel(label['ylabel'])
        clabel=label['clabel']
    else:
        clabel=None
    if plotev!=None:
        plt.scatter(plotev['x'],plotev['y'],s=5,c="gray",marker="o")
#     if depthSlice:
#         plt.gca().invert_yaxis()
    if ticks!=None:
        ax.set_yticks(ticks['yticks'])
        ax.set_xticks(ticks['xticks'])
    if clim !=None:
        cticks=np.linspace(clim[0],clim[1],5)
    else:
        cticks=None
    plt.axis('image')
    plt.axis(region)
#     cb=Qcolorbar(ax,im,ticks=cticks,name=label['clabel'],cbwidth="5%",pad=0.05,format="%2.0f",orientation='vertical')
    cb=Qcolorbar(ax,im,ticks=cticks,name=clabel,cbwidth="5%",pad=0.05,format="%2.0f",orientation='vertical')

#def velchangescolorbar(ax,axim,ticks,cbwidth="5%",pad=0.05,format="%2.1f",orientation='vertical'):
def velchangescolorbar(ax,im,ticks,cbwidth="5%",pad=0.05,format="%2.1f",orientation='vertical',title='dV/V(%)'):
    from matplotlib import pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size=cbwidth, pad=0.05)
    cb=plt.colorbar(im,cax=cax,ticks=ticks,format=format, orientation=orientation )
  #  cb=plt.colorbar(axim,cax=cax,ticks=ticks,format=format, orientation=orientation )
    cb.ax.set_title(title,fontsize=18,pad=16,fontweight='bold')
    cb.ax.tick_params(axis='both', which='major', labelsize=18)    
    return cb
#def textlocationkey(ax,fontsize=20,color="black"):
#    ax.text(-95,0,'CP',color=color,fontsize=fontsize)
#    ax.text(-55,5,'SGP',color=color,fontsize=fontsize)
#    ax.text(15,45,'SAF',color=color,fontsize=fontsize)
#    ax.text(10,-10,'SJFZ',color=color,fontsize=fontsize)
#    ax.text(35,-45,'EF',color=color,fontsize=fontsize)
#    ax.text(65,20,'ST',color=color,fontsize=fontsize)
#    ax.text(120,5,'IF',color=color,fontsize=fontsize)
#    dx=10 
#    dy=dx/np.tan(43/180*np.pi)
#    ax.arrow(140,70,-dx,dy,width=1.5, fc='k', ec='k')
#    ax.text(135,80,"N",fontsize=fontsize-2,rotation=43)
##ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5),arrowprops=dict(facecolor='black', shrink=0.05)
##bbox_props = dict(boxstyle="rarrow,pad=0.3", fc="b", ec="b", lw=2)
##ax.text(130, 80, "  N   ", ha="center", va="center", rotation=43+90,size=15,bbox=bbox_props)
##plt.tick_params(axis='both', which='major', labelsize=fontsize)
#    return ax
def textlocationkey(ax,fontsize=20,color="black",alpha=0.8):
    ax.annotate('CP',(-95,0),color=color,alpha=alpha,fontsize=fontsize,annotation_clip=True)
    ax.annotate('SGP',(-55,5),color=color,alpha=alpha,fontsize=fontsize,annotation_clip=True)
    ax.annotate('SAF',(15,45),color=color,alpha=alpha,fontsize=fontsize,annotation_clip=True)
    ax.annotate('SJFZ',(10,-10),color=color,alpha=alpha,fontsize=fontsize,annotation_clip=True)
    ax.annotate('EF',(35,-45),color=color,alpha=alpha,fontsize=fontsize,annotation_clip=True)
    ax.annotate('ST',(65,20),color=color,alpha=alpha,fontsize=fontsize,annotation_clip=True)
    ax.annotate('IF',(120,5),color=color,alpha=alpha,fontsize=fontsize,annotation_clip=True)
    dx=10 
    dy=dx/np.tan(43/180*np.pi)
    ax.arrow(140,70,-dx,dy,width=1.5, fc='k', ec='k')
    ax.annotate("N",(135,80),fontsize=fontsize-2,rotation=43,annotation_clip=True)
#ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5),arrowprops=dict(facecolor='black', shrink=0.05)
#bbox_props = dict(boxstyle="rarrow,pad=0.3", fc="b", ec="b", lw=2)
#ax.text(130, 80, "  N   ", ha="center", va="center", rotation=43+90,size=15,bbox=bbox_props)
#plt.tick_params(axis='both', which='major', labelsize=fontsize)
    return ax

def textlocationkeySmallRegion(ax,fontsize=20,color="black"):
    #ax.annotate('CP',(-95,0),color=color,fontsize=fontsize,annotation_clip=True)
    #ax.annotate('SGP',(-55,5),color=color,fontsize=fontsize,annotation_clip=True)
    #ax.annotate('SAF',(15,45),color=color,fontsize=fontsize,annotation_clip=True)
    ax.annotate('SJFZ',(10,-10),color=color,fontsize=fontsize,annotation_clip=True)
    #ax.annotate('EF',(35,-45),color=color,fontsize=fontsize,annotation_clip=True)
    #ax.annotate('ST',(65,20),color=color,fontsize=fontsize,annotation_clip=True)
    #ax.annotate('IF',(120,5),color=color,fontsize=fontsize,annotation_clip=True)
    dx=2
    dy=dx/np.tan(43/180*np.pi)
    ax.arrow(45,15,-dx,dy,width=0.5, fc='k', ec='k')
    ax.annotate("N",(45,18),fontsize=fontsize,rotation=43,annotation_clip=True)
#ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5),arrowprops=dict(facecolor='black', shrink=0.05)
#bbox_props = dict(boxstyle="rarrow,pad=0.3", fc="b", ec="b", lw=2)
#ax.text(130, 80, "  N   ", ha="center", va="center", rotation=43+90,size=15,bbox=bbox_props)
#plt.tick_params(axis='both', which='major', labelsize=fontsize)
    return ax

