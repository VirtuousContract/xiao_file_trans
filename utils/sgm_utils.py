def census_transform_nxn(source,width,height,n):
    '''
    * \brief census变换
    * \param source	输入，影像数据
    * \param census	输出，census值数组
    * \param width		输入，影像宽,奇数
    * \param height	输入，影像高，奇数
    n 窗口大小
    '''
    if width%2==0 or height%2==0: raise Exception('窗口大小n应为奇数')
    if n>width or n>height: raise Exception('窗口大小n应当小于图像尺寸')
    # 逐像素计算census值
    ksize=n//2-1 # 窗口半径
    census=[0]*width*height #census与输入图像大小相等，外圈有几圈是全0
    for i in range(ksize,height-ksize):
        for j in range(ksize,width-ksize):
            # 中心像素值
            gray_center=source[i+width+j]
            # 遍历大小为nxn的窗口内邻域像素，逐一比较像素值与中心像素值的的大小，计算census值
            census_val=0
            for r in range(-ksize,ksize+1):
                for c in range(-ksize,ksize+1):
                    census_val<<=1
                    gray=source[(i+r)*width+j+c]
                    if(gray<gray_center): census_val+=1
            
            #
            census[i*width+j]=census_val

def Hamming32(x,y):
    '''
    @ 功能      计算两个字串的汉明距离:两个位串中不同的位的个数
    * return    不同的位的个数
    * x:        输入的字串
    * y：       输入的字串
    '''
    count=0 #计数
    val=x^y # 不同的位在val中保留为1
    while(val):
        count+=1
        val&=val-1 #减少一个'1'
    return count

def CostAggregateLeftRight(img_data,width,height,min_disparity,max_disparity,p1,p2_init,cost_init,cost_aggr,is_forward):   
    assert(width>0 and height>0 and min_disparity<=max_disparity),'width>0 and height>0 and min_disparity<=max_disparity'

    #视差范围
    disp_range = max_disparity - min_disparity

    P1=p1
    P2_Init=p2_init

    #正向(左->右) ：is_forward = true ; direction = 1
	#反向(右->左) ：is_forward = false; direction = -1
    direction=1 if is_forward else -1

    #聚合
     
