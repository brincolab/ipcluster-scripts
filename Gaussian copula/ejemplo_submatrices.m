N = 10;
k = 9;
int_list = arrayfun(@(x) num2cell(combnk(1:N,x),2),(2:k),'uni',0);
int_list = cat(1,int_list{:});