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
