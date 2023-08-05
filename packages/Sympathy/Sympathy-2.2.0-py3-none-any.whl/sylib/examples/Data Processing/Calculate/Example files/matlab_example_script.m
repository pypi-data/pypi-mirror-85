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
    names = arg.column_names();
    price = names(1, :);
    price_value = arg.get_column_to_array(price);

    out_table = Table();
    out_table = out_table.set_column_from_array(...
        'MAX_PRICE',  max(price_value), [[], []]);
    out_table = out_table.set_column_from_array(...
        'MIN_PRICE',  min(price_value), [[], []]);
    out_table = out_table.set_table_attributes([]);
    res = out_table;
catch err
    err.message
end
