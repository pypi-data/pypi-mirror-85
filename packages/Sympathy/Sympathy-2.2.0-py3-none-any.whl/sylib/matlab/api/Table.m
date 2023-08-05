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

classdef Table
    properties
        data
    end

    methods (Access = private )
        function index = name_to_index(self, column)
            % Finds the index of the column name
            index = -1;
            if isfield(self.data, 'names')
                s = size(self.data.names);
                for i=1:s(1)
                    if self.data.names(i, :) == column
                        index = i;
                        break;
                    end
                end
            end
        end
    end

    methods
        function self = Table()
            self.data = struct();
            self.data.names = char;
            self.data.col = [];
            self.data.col_attr = {};
            self.data.col_attr_values = {};
            self.data.table_attr = {};
            self.data.name = '';
        end

        function self = clear(self)
        %Clear the table. All columns and attributes will be removed.
              self = Table();
        end

        function names = column_names(self)
            % Return a list with the names of the table columns.
            names = self.data.names();
        end

        function type = column_type(self, column)
            %Return the type of column named ``column``.
            index = self.name_to_index(column);
            type = '';
            if index > 0
                type = class(self.data.col(index, :));
            end
        end

        function len = number_of_rows(self)
            %Return the number of rows in the table.
            s = size(self.data.col);
            len = s(1);
        end

        function len = number_of_columns(self)
            %Return the number of columns in the table.
            s = size(self.data.col);
            len = s(2);
        end

        function status = is_empty(self)
            %Returns ``True`` if the table is empty.
            if isempty(self.data.col)
                status = true;
            else
                status = false;
            end
        end

        function self = from_file(self, filename)
            %Load data from file.
            self.data = load(filename);
        end

        function to_file(self, filename)
            %Write data to file.
            data = self.data;
            save(filename, '-struct', 'data')
        end

        function self = set_column_from_array(self, column, array, attributes)
            % Write an array to column named by column_name.
            % If the column already exists it will be replaced.
            index = self.name_to_index(column);
            if index < 0
                index = 1;
                if isfield(self.data, 'names')
                    s = size(self.data.names);
                    index = s(1) + 1;
                end
                self.data.names(index, :) = char(column);
            end

            self.data.col(index, :) = array;

            if ~isempty(attributes)
                self.data.col_attr(index, :) = attributes{1};
                self.data.col_attr_values(index, :) = attributes{2};
            end
        end

        function array = get_column_to_array(self, column)
            %Return named column as a array.
            index = self.name_to_index(column);
            array = [];
            if index > 0
                array = self.data.col(index, :);
            end
        end

        function self = set_name(self, name)
            %Set table name. Use '' to unset the name.
            self.data.name = name;
        end

        function name = get_name(self)
            %Return table name or '' if name is not set.
            if isfield(self.data, 'name') == 1
                name = self.data.name;
            else
                name = '';
            end
        end

        function attrs = get_column_attributes(self, column)
            %Return dictionary of attributes for column_name.
            attrs = [];
            index = self.name_to_index(column);
            if ~isempty(self.data.col_attr)
                attr = self.data.col_attr{index};
                value = self.data.col_attr_values{index};
                attrs = {attr, value};
            end
        end

        function self = set_column_attributes(self, column, attributes)
            % Set dictionary of scalar attributes for column_name.
            % Attribute values can be any numbers or strings but attributes
            % must be cell array.
            index = self.name_to_index(column);
            self.data.col_attr{index} = attributes{1};
            self.data.col_attr_values{index} = attributes{2};
        end

        function attr = get_table_attributes(self)
            % Return dictionary of attributes for table.
            attr = self.data.table_attr';
        end

        function self = set_table_attributes(self, attributes)
            % Set table attributes to those in dictionary attributes.
            self.data.table_attr = attributes';
        end

        function attrs = get_attributes(self)
            % Get all table attributes and all column attributes.

            attrs = {};

            table_attr = self.get_table_attributes();

            attrs(1) = {table_attr};
            col_attr = cell(length(self.data.col_attr));
            i = 1;

            for j = 1:length(self.data.col_attr)
                col_attr{i} = {char(self.data.col_attr{j}), self.data.col_attr_values{j}};
                i = i + 1;
            end
            attrs(2) = {col_attr};
        end

        function self = set_attributes(self, attributes)
            %Set table attributes and column attributes at the same time.

            self.data.table_attr = attributes{1};
            for i=1:length(attributes{2})
                self.data.col_attr{i} = char(attributes{2}{i}{1});
                self.data.col_attr_values{i} = attributes{2}{i}{2};
            end
        end

        function status = has_column(self, key)
            % Return True if table contains a column named key.

            status = false;
            if self.name_to_index(key) > 0
                status = true;
            end
        end

        function self = update(self, other_table)
            % Updates the columns in the table with columns from other
            % table keeping the old ones.
            %
            % If a column exists in both tables the one from other_table
            % is used.

            other_names = other_table.column_names();
            len = size(other_names);
            for i=1:len(1)
                column = other_names(i, :);
                array = other_table.get_column_to_array(column);
                attr = other_table.get_column_attributes(column);
                self = self.set_column_from_array(column, array, attr);
            end
        end

        function self = update_column(self, column_name, other_table, other_name)
            % Updates a column from a column in another table.
            %
            % The column other_name from other_table will be copied into
            % column_name.
            % If column_name already exists it will be replaced.
            %
            % When other_name is not used, then column_name will be used
            % instead.

            array = other_table.get_column_to_array(other_name);
            attr = other_table.get_column_attributes(other_name);
            self = self.set_column_from_array(column_name, array, attr);
        end

        function self = hjoin(self, other_table)
            % Add the columns from other_table.
            % Analoguous to :meth:`update`.

            self = self.update(other_table);
        end

        function self = source(self, other_table)
            self.data = other_table.data;
            self.set_name(other_table.get_name());
        end

        function value = attr(self, name)
            % Get the tables attribute with `name`.
            value = '';
            attributes = self.get_table_attributes();
            for i = 1:length(attributes)
                if attributes{1} == name
                    value = attributes{2};
                end
            end
        end

        function attr = attrs(self)
            % Return dictionary of attributes for table.
            attr = self.get_attributes();

        end
    end
end
