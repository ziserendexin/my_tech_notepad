## 编程

`octave`我不评价是否好用，总之不是很爽。

http://jinpf.github.io/2016/04/19/Octave-Tutorial/

```octave
%%  向量和矩阵
A = [1 2; 3 4; 5 6]

v = [1 2 3]
v = [1; 2; 3]
v = [1:0.1:2]  % 从1到2（包含）步长为0.1 绘制坐标轴时非常有用
v = 1:6        % 从1到6,步长为1

C = 2*ones(2,3)  % 同 C = [2 2 2; 2 2 2]
w = ones(1,3)    % 1x3 全1向量
w = zeros(1,3)   % 1x3 全0向量
w = rand(1,3)    % 矩阵的所有值服从[0,1]均匀分布(uniform distribution)
w = randn(1,3)   % 矩阵的所有值服从均值为0，方差为1的正态分布(normal distribution)，注意加分号
w = -6 + sqrt(10)*(randn(1,10000));  % (均值 = -6, 方差 = 10)
hist(w)     % 绘制10个方块的直方图(histogram) (默认)
hist(w,50)  % 绘制50个方块的直方图
% 注意: 如果 hist() 一直未响应, 尝试使用 "graphics_toolkit('gnu_plot')" 

I = eye(4)    % 4x4 单位矩阵(identity matrix)

% help 帮助
help eye
help rand
help help    
```

```octave
%% 维数显示
sz = size(A) % 结果为1x2 矩阵: [(行数) (列数)]
size(A,1)  % A的行数
size(A,2)  % A的列数
length(v)  % 行、列最长的那个维数
```

```octave
%% 绘制灰度图
 A = magic(5)
 imagesc(A)	% 绘制一个用不同颜色标注的图片
 imagesc(A),colorbar,colormap gray % 增加一个色条，同时使用灰度图

```

```octave
v = zeros(10,1);
for i=1:10, 
    v(i) = 2^i;     % 缩进仅为美观 不影响程序
end;

% Can use "break" "continue" inside for while loops to control execution.

i = 1;
while i <= 5,
  v(i) = 100; 
  i = i+1;
end

i = 1;
while true, 
  v(i) = 999; 
  i = i+1;
  if i == 6,
    break;
  end;
end

if v(1)==1,
  disp('The value is one!');
elseif v(1)==2,
  disp('The value is two!');
else
  disp('The value is not one or two!');
end
```

每个函数定义在一个文件中，文件名为 “functionName.m”，其中文件名和定义函数名需要保持一致，以便调用。

如定义 “squareThisNumber.m”：

```octave
function y = squareThisNumber(x)
y = x^2;
```

在Octave中调用需要将函数定义放到Octave运行Path中。

- 方案一：

```octave
cd /path/to/function
```

- 方案二：

```octave
addpath('/path/to/function/')
savepath       % 方便以后使用
```

之后调用函数：

```octave
functionName(args)
```

Octave函数可以返回多个值：

```octave
%% 定义
function [y1, y2] = squareandCubeThisNo(x)
y1 = x^2
y2 = x^3
%% 调用
[a,b] = squareandCubeThisNo(x)
```

