% This file is part of Sympathy for Data.
% Copyright (c) 2016-2017 Combine Control Systems AB
%
% Sympathy for Data is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, version 3 of the License.
%
% Sympathy for Data is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with Sympathy for Data.  If not, see <http://www.gnu.org/licenses/>.

function result = calc(input, s)
% Try to evaluate the input expression and create error message if the
% calculation can't be performed.
% input: string with a calculation
% s, size of the data
try
    
    result = evalin('base', input);
    if min(size(result)) > 1
        s = size(input);
        result = cellstr(char(ones(max(s), 1)*'Only scalars and vectors supported'));
    end
catch err
  result = cellstr(char(ones(s)*err.message));
end
