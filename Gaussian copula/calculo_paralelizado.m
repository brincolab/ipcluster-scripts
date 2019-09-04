
parse_results = @(x) double(py.array.array('d',x));
N = 10 ;x = rand(N);x = 0.5 * (x + x'); 
x(1:N+1:end) = N; x_flat = reshape(x.',1,[]);

res = py.determinantes.get_all_determinants(x_flat,N);

dets = parse_results(res{1});
ents = parse_results(res{2});
idxs = res{3};

