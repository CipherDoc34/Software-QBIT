load("full_data.mat");

for person = 1:30
    for trial = 1:6
        A = full_data{person, 1}.FallingForw{trial,1}(1:3,:);
        B = full_data{person, 1}.FallingBack{trial,1}(1:3,:);
        C = full_data{person, 1}.FallingRight{trial,1}(1:3,:);
        D = full_data{person, 1}.FallingLeft{trial,1}(1:3,:);
        idxA = compute(A);
        idxB = compute(B);
        idxC = compute(C);
        idxD = compute(D);
        

        csvwrite("Person" + person + "-FallingForw-Trial" + trial + ".csv", A(:,left(idxA(1)):right(idxA(2), A)));
        csvwrite("Person" + person + "-FallingBack-Trial" + trial + ".csv", B(:,left(idxB(1)):right(idxB(2), B)));
        csvwrite("Person" + person + "-FallingRight-Trial" + trial + ".csv", C(:,left(idxC(1)):right(idxC(2), C)));
        csvwrite("Person" + person + "-FallingLeft-Trial" + trial + ".csv", D(:,left(idxD(1)):right(idxD(2), D)));
    end
end

function val = right(idx, A)
    [~, cols] = size(A);
    if idx + 5 >= cols
        val = cols;
    else 
        val = idx + 5;
    end
end

function val = left(idx)
    if idx - 5 <= 1
        val = 1;
    else 
        val = idx - 5;
    end
end

function index = compute(A)
    
    mins = zeros(1,3);
    maxs = zeros(1,3);
    for i = 1:3
        % Compute the difference between adjacent elements
        diffs = diff(A(i,:));
        
        % Compute the standard deviation of the differences
        std_diffs = std(diffs);
        
        % Find the indices where the absolute difference is greater than 3 times the standard deviation
        spike_idx = find(abs(diffs) > 3*std_diffs);
        
        % Compute the column indices where spikes occur
        spike_col_idx = spike_idx + 1;
        
        mins(i) = min(spike_col_idx);
        maxs(i) = max(spike_col_idx);
    end
    index = [min(mins) max(maxs)];
end