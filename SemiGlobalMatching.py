import numpy as np 
import cv2
from utils import sgm_utils

class SGMOption(object):
    '''
    brief SGM参数结构体
    '''
    num_paths=8 #聚合路径
    min_disparity=0 #最小视差
    max_disparity=640 #最大视差
    p1=10 #惩罚项参数
    p2_int=150 #惩罚项参数

class SemiGlobalMatching(object):
    #私有变量
    # SGMOption __option

    # 公有函数
    def __init__(self,width,height,option):
        '''
        * brief 类的初始化，完成一些内存的预分配、参数的预设置等
        * param width		输入，核线像对影像宽
        * param height	输入，核线像对影像高
        * param option	输入，SemiGlobalMatching参数
        '''
        self.__width=width
        self.__height=height
        self.__option=option
        
        if(width==0 or height==0): raise Exception('Error:读入错误，图像尺寸必须大于0')

        # census值（左右影像）
        self.__census_left=[]
        self.__census_right=[]

        #匹配代价（初始/聚合）
        disp_range=option.max_disparity-option.min_disparity
        if(disp_range<=0): raise Exception('Error:max_disparity应该大于min_disparity')

        self.__cost_init=[]
        self.__cost_aggr=[]
        self.__disp_left=[]

        self.__img_left=[]
        self.__img_right=[]


    def Match(self,img_left,img_right,disp_left): 
        '''
        * brief 执行匹配
        * param img_left		输入，左影像数据指针 
        * param img_right		输入，右影像数据指针
        * param disp_left		输出，左影像视差图指针，预先分配和影像等尺寸的内存空间
        '''
        if(img_left.size==0 or img_right.size==0): raise Exception('Error:输入图像矩阵为空')
        
        # census变换
        CensusTransform()

        #代价计算
        ComputeCost()

        #代价聚合
        CostAggregation()

        #视差计算
        ComputeDisparity()

        #输出视差图
        memcpy(disp_left,self.__disp_left,self.__width*self.__height*)

     
    def Reset(self,width,height,option):
        '''
        * \brief 重设
        * \param width		输入，核线像对影像宽
        * \param height	输入，核线像对影像高
        * \param option	输入，SemiGlobalMatching参数
        '''
        self.__width=width
        self.__height=height
        self.__option=option
        
        if(width==0 or height==0): raise Exception('Error:读入错误，图像尺寸必须大于0')

        # census值（左右影像）
        self.__census_left=[]
        self.__census_right=[]

        #匹配代价（初始/聚合）
        disp_range=option.max_disparity-option.min_disparity
        if(disp_range<=0): raise Exception('Error:max_disparity应该大于min_disparity')

    def __CensusTransform():
        utils.census_transform_nxn(self.__img_left,self.__census_left,self.__width,self.__height)
        utils.census_transform_nxn(self.__img_right,self.__census_right,self.__width,self.__height)
    

    def ComputeCost():
        min_disparity=self.__option.min_disparity
        max_disparity=self.__option.max_disparity
        disp_range=max_disparity-min_disparity
        if disp_range<=0: return 0

        #计算代价（基于Hamming距离）
        for i in range(self.__height):
            for j in range(self.__width):                              
                #逐视差计算代价值
                for d in range(min_disparity,max_disparity):
                    # cost=self.__cost_init[i*self.__width*disp_range+j*disp_range+(d-min_disparity)] #__cost_init是“三维”的矩阵，所以要多乘一个
                    index=i*self.__width*disp_range+j*disp_range+(d-min_disparity) #当前计算的代价在代价卷中的位置
                    #第三维度disp_range，d-min_disparity是第三维度的坐标
                    
                    #越界判断
                    if j-d<0 or j-d>=self.__width:
                        cost=255//2
                        continue
                    #根据左右图中对应点的census编码计算汉明距离（代价）
                    census_val_l=self.__census_left[i*self.__width+j]
                    census_val_r=self.__census_right[i*self.__width+j-d]
                    self.__cost_init[index]=utils.Hamming32(census_val_l,census_val_r)
    
    def CostAggregation():
        min_disparity=self.__option.min_disparity
        max_disparity=self.__option.max_disparity
        assert max_disparity>min_disparity , "应该是：max_disparity>min_disparity"

        size=self.__width*self.__height*(max_disparity-min_disparity) #代价矩阵的三个维度的总长度
        if size<=0:
             return

        P1=self.__option.p1
        P2_Int=self.__option.p2_int

        if self.__option.num_paths==4 or self.__option.num_paths==8:
            #左右聚合
            sgm_utils

                 
                    

    


