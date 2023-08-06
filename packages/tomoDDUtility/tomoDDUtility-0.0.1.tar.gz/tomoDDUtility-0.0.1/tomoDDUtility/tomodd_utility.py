import numpy as np

'''
Goal: convert the synthetic data to the tomodd format 
Input: absolute.syn, dt.syn,dtcc.syn
Output: syn.absolute.dat, syn.dt.ct, syn.dt.cc 
HU JING
2018-08-11
'''
'''
I think this step is not necessary for checkerboard test. first it is not easy to extract real geometry.
second, tomodd do not drop a number of events during inversion. 
thus, you just need to convert the reloc file to the catalog file and use the real observation. 
this can keep most of raypaths for checkerboard test.

# convert tomoddres to real phase data
def tomoddres2RealGeometry(filename,path="./Input"):
    fid_out = open(path+"/tstar.dat",'w')
    evid_old = "#####################"
    try:
        fid_in  = open(filename,'r')
        for line in fid_in :
            tmp=line.split()
            if (tmp[0]=="Event-pair:"):
                continue
            if (tmp[0]=="Station-pair:"): 
                break
            staname,traveltime,evid,evid= tmp[0:4]
            weight="1";phase="P"
            
            if(evid==evid_old):
                fid_out.write("    ".join([staname,traveltime,weight,phase,"\n"]))
            else:
                evid_old = evid
                fid_out.write("#  "+evid+"\n")
                fid_out.write("    ".join([staname,traveltime,weight,phase,"\n"]))
        fid_in.close()
        print(evid)
    except:
        print(filename+" does not exist,but it is ok")
    finally:
        fid_out.close()
'''
def tomoddres2RealGeometry():
    pass

def reloc2Catalog(filename,new_file,fixloc=0):
    '''
	reloc file from tomodd_esdp to catalog of tomodd or hypodd	
	usage:
		  reloc2Catlog('tomodd.reloc','new_catalog')
		
    option: use  original awk commands to do this process.
			command="BEGIN{}\
			{ID=$1;\n lat=$2;lon=$3;dep=$4;\n ex=$8;ey=$9;ez=$10;\n yr=$11;mo=$12;dy=$13;hr=$14;min=$15;sec=$16;\n \
			mag=$17;rms=$23;  \n\
			dh=sqrt(ex*ex+ey*ey); \n\
			date=yr*10^4+mo*10^2+dy; \n\
			time=hr*10^6+min*10^4+sec; \n\
			print date,time,lat,lon,dep,mag,dh/1000,ez/1000,rms,ID, 0 > \"new_catalog.dat\"}END{}" 
			with open('loc2event_pyout.awk','w') as f:
				f.write(command)
    '''
    fid_out= open(new_file,'w')
    fid_in = open(filename,'r')
    for line in fid_in:
        tmp=line.split()
        ID,lat,lon,dep=tmp[0:4]
        errx,erry,errz = list(map(float,tmp[7:10]))
        yr,mon,day,hour,mint,sec = list(map(float,tmp[10:16]))
        mag,rms = tmp[16],tmp[22]
        date = yr*(10**4)+mon*(10**2) + day
        time = hour*(10**6) + mint*(10**4)+sec
        dh=np.sqrt(errx*errx+erry*erry);
        fid_out.write("{:<12.0f} {:<12.0f} {} {} {} {} {:.3f} {:.3f} {} {} {} \n".format(date,time,lat,lon,dep,mag,dh/1000,errz/1000,rms,ID,fixloc))
    fid_in.close()
    fid_out.close()

def abs2syn(filename,path):
    fid_out = open(path+"syn.absolute.dat",'w')
    evid_old = "#####################"
    try:
        fid_in  = open(filename,'r')
        for line in fid_in :
           evid,staname,traveltime,weight,phase = line.split()
           if(evid==evid_old):
               fid_out.write("    ".join([staname,traveltime,weight,phase,"\n"]))
           else:
               evid_old = evid
               fid_out.write("#  "+evid+"\n")
               fid_out.write("    ".join([staname,traveltime,weight,phase,"\n"]))
        fid_in.close()
    except:
        print(filename+" does not exist,but it is ok")
    finally:
        fid_out.close()

def dt2syn(filename,path):
    fid_out = open(path+"syn.dtct_evepr",'w')
    evid1_old = "#####################"
    evid2_old = "#####################"
    try:
        fid_in  = open(filename,"r") 
        for line in fid_in:
           evid1,evid2,staname,traveltime1,traveltime2,weight,phase = line.split()
           if(evid1==evid1_old and evid2==evid2_old):
               fid_out.write("    ".join([staname,traveltime1,traveltime2,weight,phase,"\n"]))
           else:
               evid1_old = evid1
               evid2_old = evid2
               fid_out.write("# "+evid1+"    "+evid2+"\n")
               fid_out.write("    ".join([staname,traveltime1,traveltime2,weight,phase,"\n"]))
        fid_in.close()
    except:
        print(filename+" does not exist,but it is ok")
    finally:
        fid_out.close()
def dt_stapr2syn(filename,path):
    fid_out = open(path+"syn.dt.ct_stapr",'w')
    evid_old = "#####################"
    try:
        fid_in  = open(filename,"r") 
        for line in fid_in:
           evid,sta1,sta2,traveltime1,traveltime2,weight,phase = line.split()
           if evid==evid_old:
               fid_out.write("    ".join([sta1,sta2,traveltime1,traveltime2,weight,phase,"\n"]))
           else:
               evid_old = evid
               fid_out.write("#  "+evid+"\n")
               fid_out.write("    ".join([sta1,sta2,traveltime1,traveltime2,weight,phase,"\n"]))
        fid_in.close()
    except:
        print(filename+" does not exist,but it is ok")
    finally:
        fid_out.close()

# for hypodd cc_format  
def cc2syn(filename,path):
    fid_out = open(path+"syn.dt.cc",'w')
    evid1_old = "#####################"
    evid2_old = "#####################"
    try:
        fid_in  = open(filename,"r") 
        for line in fid_in:
           evid1,evid2,staname,traveltime1,traveltime2,weight,phase = line.split()
           if(evid1==evid1_old and evid2==evid2_old):
               fid_out.write("    ".join([staname,traveltime1,traveltime2,weight,phase,"\n"]))
           else:
               evid1_old = evid1
               evid2_old = evid2
               fid_out.write("# "+evid1+"    "+evid2+"  0.0\n")
               fid_out.write("    ".join([staname,traveltime1,traveltime2,weight,phase,"\n"]))
        fid_in.close()
    except:
        print(filename+" does not exist,but it is ok")
    finally:
        fid_out.close()

def create_chkboard(model,nx,ny,nz,perturbation=0.05,anomaly_x=1,anomaly_y=1,anomaly_z=1):
    '''
    algorithm from zhangxin 
    '''
    model_new = np.zeros_like(model)

    model_new[:] =model
    stepz = 0
    ano_z = perturbation
    for jz in range(1,nz-1):
        stepz = stepz+1
        if(stepz == anomaly_z ):
            stepz = 0
            ano_z = -ano_z
        stepy = 0
        ano_y = ano_z
        for jy in range(1,ny-1):
            stepy = stepy+1
            if(stepy == anomaly_y):
                stepy = 0
                ano_y = -ano_y
            stepx = 0
            ano_x = ano_y
            row = jz*ny + jy
            for col in range(1,nx-1):
                stepx = stepx +1
                model_new[row,col] = model[row,col]*(1+ano_x)
                if(stepx == anomaly_x):
                    ano_x = -ano_x
                    stepx =0
    return model_new

def create_chkboard_sparse(model,nx,ny,nz,perturbation=0.05,anomaly_x=1,anomaly_y=1,anomaly_z=1):
    '''
    algorithm 
    '''
    pass

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







###### ReadWaveforms ####################
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

def get_resolvebility(X,Y,Z,m_rec,m_true,radius=2):
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
    
    
### plot residuals
#file_res_ini  = "./3D_VpVs/Output/tomodd_initial.res"
#file_res_final= "./3D_VpVs/Output/tomodd.res"
#Swave_flag=True

def extract_res_info(file_res):
    with open(file_res,'r') as f:
        temp = f.read().splitlines()
        res_info=temp[1:]
        P_abs = []
        P_dtct = []
        S_abs = []
        S_dtct = []
        for line in res_info:
            if int(line.split()[4])==3:
                if float(line.split()[8])>0.:
                    P_dtct.append(float(line.split()[6])/1000)
                else:
                    P_abs.append(float(line.split()[6])/1000)
                    
            elif  int(line.split()[4])==4:
                if float(line.split()[8])>0.:
                    S_dtct.append(float(line.split()[6])/1000)
                else:
                    S_abs.append(float(line.split()[6])/1000)
    return P_dtct,P_abs,S_dtct,S_abs
def plot(file_res_ini,file_res_final):
	P_dtct_ini  ,  P_abs_ini,  S_dtct_ini,  S_abs_ini = extract_res_info(file_res_ini);
	P_dtct_final,P_abs_final,S_dtct_final,S_abs_final = extract_res_info(file_res_final);
	bins=np.linspace(-1.5,1.0,100)
	plt.figure(1,figsize=(12,4))
	plt.subplot(1,2,1)
	plt.hist(P_abs_ini,bins,alpha=0.8,color='grey', label='initial residual')
	plt.hist(P_abs_final,bins,alpha=0.8,color='green',label='final residual')
	#plt.axis([-400,400,0,10000])
	plt.title('P wave absolute data',fontsize=18)
	plt.ylabel('Frequency',fontsize=18)
	plt.xlabel('Residual(s)',fontsize=18)
	plt.xlim([-2,2])
	plt.xticks(fontsize=16)
	plt.yticks(fontsize=16)
	plt.legend(loc='upper right',fontsize=14)
	plt.subplot(1,2,2)
	bins=np.linspace(-0.8,0.8,100)
	plt.hist(P_dtct_ini,bins,alpha=0.8,color='grey', label='initial residual')
	plt.hist(P_dtct_final,bins,alpha=0.8,color='green',label='final residual')
	plt.title('P wave differential data',fontsize=18)
	plt.ylabel('Frequency',fontsize=18)
	plt.xticks(fontsize=16)
	plt.yticks(fontsize=16)
	plt.xlabel('Residual(s)',fontsize=18)
	plt.xlim([-0.75,0.75])
	plt.legend(loc='upper right',fontsize=14)
	plt.tight_layout()
	plt.savefig('Residual_Pwave.png',dpi=300)
	print(len(P_abs_ini),len(P_abs_final),(len(P_abs_ini)-len(P_abs_final))/len(P_abs_ini))
	print(len(P_dtct_ini),len(P_dtct_final),(len(P_dtct_ini)-len(P_dtct_final))/len(P_dtct_ini))



