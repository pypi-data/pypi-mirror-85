# *-* coding=utf8
import numpy as np
import netCDF4 as nc
import datetime
import traceback
from dateutil.relativedelta import relativedelta

class envelope():
	def __init__(self,n,s,w,e):
		self.n,self.s,self.w,self.e=n,s,w,e
	def __str__(self):
		return ("n:%s,s:%s,w:%s,e:%s"%(self.n,self.s,self.w,self.e))


areaNameDict = {"NEC": "东北","NCN": "华北","CCN": "华中","SCN": "华南","NWC": "西北","SWC": "西南","XJ": "新疆", "XZ": "西藏"}        
areaIdxDict = {"NEC": 0,"NCN": 1,"CCN": 2,"SCN": 3,"NWC": 4,"SWC": 5,"XJ": 6, "XZ": 7}
LeftTopCornerCHN = np.asarray([{"area":"CHN", "evn":envelope(60, 0,70, 140)}])


LeftTopCornerPairArr = np.asarray([
#   //东北
    {"area":"NEC", "evn":envelope(55, 38,109, 136), "CHarea":"东北"},
#   //华北
    {"area":"NCN", "evn":envelope(43,31, 109,124), "CHarea":"华北"},
#     //华中
    {"area":"CCN", "evn":envelope(36,22, 108, 124), "CHarea":"华中"},
#     //华南
    {"area":"SCN", "evn":envelope(27, 15,104, 124), "CHarea":"华南"},
#     //西北
    {"area":"NWC", "evn":envelope(44,31, 88, 114), "CHarea":"西北"},
#     //西南
    {"area":"SWC", "evn":envelope(35, 20,96, 111), "CHarea":"西南"},
#     //新疆
    {"area":"XJ", "evn":envelope(50, 34,72, 97), "CHarea":"新疆"},
#     //西藏
    {"area":"XZ", "evn":envelope(37,25, 77, 101), "CHarea":"西藏"}])
'''

LeftTopCornerPairArrClip = np.asarray([
#   //东北
    {"area":"NEC", "evn":envelope(55+10e-5, 38+10e-5, 109+10e-5, 136+10e-5), "CHarea":"东北"},
#   //华北
    {"area":"NCN", "evn":envelope(43+10e-5, 31+10e-5, 109+10e-5, 124+10e-5), "CHarea":"华北"},
#     //华中
    {"area":"CCN", "evn":envelope(36+10e-5, 22+10e-5, 108+10e-5, 124+10e-5), "CHarea":"华中"},
#     //华南
    {"area":"SCN", "evn":envelope(27+10e-5, 15+10e-5, 104+10e-5, 124+10e-5), "CHarea":"华南"},
#     //西北
    {"area":"NWC", "evn":envelope(44+10e-5, 31+10e-5, 88+10e-5, 114+10e-5), "CHarea":"西北"},
#     //西南
    {"area":"SWC", "evn":envelope(35+10e-5, 20+10e-5, 96+10e-5, 111+10e-5), "CHarea":"西南"},
#     //新疆
    {"area":"XJ", "evn":envelope(50+10e-5, 34+10e-5, 72+10e-5, 97+10e-5), "CHarea":"新疆"},
#     //西藏
    {"area":"XZ", "evn":envelope(37+10e-5,25+10e-5, 77+10e-5, 101+10e-5), "CHarea":"西藏"}])
'''

LeftTopCornerPairArrSLL = np.asarray([
#   //大渡河
    {"area":"DDH", "evn":envelope(30.96, 28.96,101.21, 103.21)},
#   //贵阳
    {"area":"GY", "evn":envelope(27.08,26.08, 106.23,107.23)},
#     //长春
    {"area":"CC", "evn":envelope(44.4,43.4, 124.72, 125.72)},
#     //深圳
    {"area":"SZ", "evn":envelope(22.86, 22.38,113.76, 114.63)},
#     //天津
    {"area":"TJ", "evn":envelope(40.26,38.56, 116.69, 118.06)},
#     //黄山
    {"area":"HS", "evn":envelope(35, 25,113, 123)},
#     //华山
    {"area":"HUAS", "evn":envelope(36, 30,105, 115)},
#     //武汉
    {"area":"WH", "evn":envelope(31.37, 29.96,113.69, 115.08)},
#     //潍坊
    {"area":"WF", "evn":envelope(37.31, 35.70,118.17,120.0 )},
#     //川藏
    {"area":"CZ", "evn":envelope(33,28, 90, 105)}])
LeftTopCornerPairArrSLLnew = np.asarray([
#   //四川
    {"area":"SC", "evn":envelope(36,25,95,110)},
#     //吉林
    {"area":"JL", "evn":envelope(49,38,121,132)},
#     //广东
    {"area":"GD", "evn":envelope(27,19,109,118)},
#     //京津冀
    {"area":"JJJ", "evn":envelope(44,34,112,121)},
#     //安徽
    {"area":"AH", "evn":envelope(36,29,114,120)},
#     //陕西
    {"area":"SAX", "evn":envelope(41,31,104,113)},
#     //湖北
    {"area":"HB", "evn":envelope(35,28,108,117)},
#     //山东
    {"area":"SD", "evn":envelope(40,33,114,124)}])

class dataClass():
	data_ = None
	name_ = None
	type_ = np.float32
	coordinate_ = None
	unit_ = None
	valid_range_ = [-999,999]
	missing_value_ = np.NAN
	scale_factor_ = np.float32(1.0)
	add_offset_ = np.float32(0.0)

	def __init__(self,data, name, type_,coordinate, unit,missing_value=np.NAN, scale_factor=np.float32(1.0), add_offset=np.float32(0.0),valid_range=[-999,999]):
		self.data_, self.name_, self.type_, self.coordinate_, self.unit_ ,self.missing_value_ ,self.scale_factor_,self.add_offset_,self.valid_range_= data, name,type_, coordinate, unit,missing_value, scale_factor, add_offset, valid_range

	def print(self):
		print(self.data_, self.name_, self.type_, self.coordinate_, self.unit_,self.missing_value_,self.scale_factor_,self.add_offset_,self.valid_range_)
		
def mkNCCommonUni(output,dateTimeStart,dateTimeArr,isoArr,latArr,lonArr,dataClass4D=[],dataClass3D=[],dataClass2D=[],formate='NETCDF4'):
    dataset = nc.Dataset(output,'w',format=formate) #'NETCDF4_CLASSIC')
    
    try:
        if not dateTimeArr is None and not dateTimeStart is None: 
            dataset.createDimension("time", len(dateTimeArr))
        if not isoArr is None:
            dataset.createDimension("isobaric", len(isoArr))
        
        dataset.createDimension("lat", len(latArr))
        dataset.createDimension("lon", len(lonArr))
    
        if not dateTimeArr is None and not dateTimeStart is None:
            dataset.createVariable("time", np.float32, ("time"), zlib=True)
        if not isoArr is None:
            dataset.createVariable("isobaric", np.float32, ("isobaric"), zlib=True)
        dataset.createVariable("lat", np.float32, ("lat"), zlib=True)
        dataset.createVariable("lon", np.float32, ("lon"), zlib=True)

        for e in dataClass2D:
            dataset.createVariable(e.name_, e.type_, tuple(["lat","lon"]), zlib=True)    

        for e in dataClass3D:
            dataset.createVariable(e.name_, e.type_, tuple(["time","lat","lon"]), zlib=True)

        for e in dataClass4D:
            dataset.createVariable(e.name_, e.type_, tuple(["time","isobaric","lat","lon"]), zlib=True)
        if not dateTimeArr is None and not dateTimeStart is None:
            dataset.variables["time"][:] = dateTimeArr
            dataset.variables["time"].units = 'minutes since %s'%(dateTimeStart.strftime("%Y-%m-%d %H:%M:%S"))
            dataset.variables["time"].calendar = 'gregorian'

        if not isoArr is None:
            dataset.variables["isobaric"][:] = isoArr
            dataset.variables["isobaric"].units="hPa"
            dataset.variables["isobaric"].positive="up"
        
        dataset.variables["lat"][:] = latArr
        dataset.variables['lat'].units = 'degrees_north'
    
        dataset.variables["lon"][:] = lonArr
        dataset.variables['lon'].units = 'degrees_east'
        
        for e in dataClass2D:
            dataset.variables[e.name_][:] = e.data_
            dataset.variables[e.name_].units = e.unit_
            dataset.variables[e.name_].valid_range = e.valid_range_
            dataset.variables[e.name_].coordinate = e.coordinate_
            dataset.variables[e.name_].missing_value = e.missing_value_
            dataset.variables[e.name_].scale_factor = e.scale_factor_
            dataset.variables[e.name_].add_offset = e.add_offset_
    
        for e in dataClass3D:
            dataset.variables[e.name_][:] = e.data_
            dataset.variables[e.name_].units = e.unit_
            dataset.variables[e.name_].valid_range = e.valid_range_
            dataset.variables[e.name_].coordinate = e.coordinate_
            dataset.variables[e.name_].missing_value = e.missing_value_
            dataset.variables[e.name_].scale_factor = e.scale_factor_
            dataset.variables[e.name_].add_offset = e.add_offset_

        for e in dataClass4D:
            dataset.variables[e.name_][:] = e.data_
            dataset.variables[e.name_].units = e.unit_
            dataset.variables[e.name_].valid_range = e.valid_range_
            dataset.variables[e.name_].coordinate = e.coordinate_
            dataset.variables[e.name_].missing_value = e.missing_value_
            dataset.variables[e.name_].scale_factor = e.scale_factor_
            dataset.variables[e.name_].add_offset = e.add_offset_

        #dataset.close()
    except Exception as ex:
        print(ex)
        print(latArr.shape,lonArr.shape,e.data_.shape)
        print(traceback.format_exc())
        #dataset.close()
    finally:
        dataset.close()

def clip(data, ltc, lat0, lon0, step):
    latIdx0 = int((lat0 - ltc.n) / step+ 0.5)
    latIdx1 = int((lat0 - ltc.s) / step+ 0.5)
    lonIdx0 = int((ltc.w - lon0) / step+ 0.5)
    lonIdx1 = int((ltc.e - lon0) / step+ 0.5)
    data = data[...,latIdx0:latIdx1+1, lonIdx0:lonIdx1+1]
    return data

def clipLat(data, ltc, step):
    latIdx0 = int((data[0] - ltc.n) / step+ 0.5)
    latIdx1 = int((data[0] - ltc.s) / step+ 0.5)
    data = data[latIdx0:latIdx1+1]
    return data

def clipLon(data, ltc, step):
    lonIdx0 = int((ltc.w - data[0]) / step+ 0.5)
    lonIdx1 = int((ltc.e - data[0]) / step+ 0.5)
    data = data[lonIdx0:lonIdx1+1]
    return data

def totalTimes(delta,second):
    return (delta.days*24*3600+delta.seconds)//second

def timeSeq(start,end,secInter):
    times=totalTimes((end-start),secInter)
    return list(map(lambda x:start+relativedelta(seconds=x*secInter),range(times)))

def UV2WSWD(U,V):
    ws = np.sqrt(np.square(U) + np.square(V))
    wd = (np.degrees(np.arctan2(-U, -V))+ 360)%360
    return ws,wd

def WSWD2UV(ws,wd):
    u=- ws*np.sin(np.radians(wd))
    v=- ws*np.cos(np.radians(wd))
    return u,v

def test():
    print("test")

def normalNC(data):
    mx=np.nanmax(data)
    mn = np.nanmin(data)
    rangeV=mx-mn
    scale = rangeV/254
    offset = (mx+mn)/2
    data1=(data - offset)/scale
    data1[np.isnan(data1)] = -128
    return data1,scale,offset


class clip_and_mosaic():
    def __init__(self,mat,patch,overlap):
        self.mat = mat
        self.patch = patch
        self.overlap = overlap
        center = patch - 2 * overlap
        self.center = center
        self.latRange = int(np.ceil(mat.shape[0]/center))
        lastPaddingLat = self.latRange*center-mat.shape[0]
        self.lonRange = int(np.ceil(mat.shape[1] / center))
        lastPaddingLon = self.lonRange * center - mat.shape[1]
        self.padMat =np.pad(mat,((overlap,lastPaddingLat+overlap),(overlap,lastPaddingLon+overlap)),'constant', constant_values=(0,0))
        self.outMat = np.zeros(self.padMat.shape)

    def clip(self):
        imgList = []
        for i in range(self.latRange):
            for j in range(self.lonRange):
                clipMat = self.padMat[self.center*i:self.center*(i+1)+2*overlap,self.center*j:self.center*(j+1)+2*overlap]
                imgList.append(clipMat)
                # plt.subplot(self.latRange,self.lonRange,j+self.lonRange*i+1)
                # plt.imshow(clipMat)
        return imgList

    def mosaic(self,imgList):
        for i in range(self.latRange):
            for j in range(self.lonRange):
                self.outMat[self.center*i:self.center*(i+1)+2*overlap,self.center*j:self.center*(j+1)+2*overlap] = imgList[j+self.lonRange*i]
        finalMat = self.outMat[overlap:overlap+self.mat.shape[0],overlap:overlap+self.mat.shape[1]]
        return finalMat

