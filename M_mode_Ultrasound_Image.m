%对每条数据线分别做寻峰处理
line=1;     %line为计数，第n条线
while line<sum(ROI_lines_info)+1  %对每条线分别做处理分析
    sig=RF_3D(:,:,line);
    fs=5e7;     %采样率为50MHz
    PRF=50;    %扫描线PRF数

    y=(abs(sig)/32767); %绝对值后强度归一
%     Sdata=y;
    Sdata=1.5*log(y+1)+0.02; %y为归一化信号强度.Sdata为亮度（0-255）
    if Sdata>255
        Sdata=255;
    end

%插值
    x0=1:1:RF_length;           %原始数据点数
    x1=1:(RF_length-1)/(fix(RF_line_samples/2-1)):RF_length;  %插值后数据点数

    for aa=1:1:RF_line_samples
        y0=Sdata(:,aa);  %单条线数据
        y2(:,aa)=interp1(x0,y0,x1,'linear');
   
    end
    ImageData=y2;
    figure()
    imshow(ImageData,[])
    line=line+1;
end