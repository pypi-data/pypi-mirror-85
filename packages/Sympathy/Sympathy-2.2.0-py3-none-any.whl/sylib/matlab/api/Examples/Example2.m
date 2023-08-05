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

try
    out_table = Table();
    in_attrs = arg.get_table_attributes();
    out_table = out_table.set_table_attributes(in_attrs);
    in_col_attr = arg.get_column_attributes('data1');
    col_0 = arg.get_column_to_array('data1');
    col_1 = arg.get_column_to_array('data2');

    % Do the calculation and add to out_table
    output = col_0 .* col_1;

    out_table = out_table.set_column_from_array('s', output, in_col_attr);
    out_table = out_table.set_column_from_array('a', output, in_col_attr);
    res = out_table;
catch err
    err.message
    exit(1)
end
