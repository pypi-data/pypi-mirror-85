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

infilename = 'test.mat';
addpath('..')
in_table = Table();

try
    %% Test from_file(infilename):
    in_table = in_table.clear();
    in_table = in_table.from_file(infilename);
    names = in_table.column_names();
    assert(strcmp(names(1, :),'data1'))
    assert(strcmp(names(2, :),'data2'))

    %% Test clear():
    in_table = in_table.from_file(infilename);
    in_table = in_table.clear();
    names = in_table.column_names();
    assert(isempty(names))
    in_table = in_table.clear();

    %% Test column_names():
    in_table = in_table.clear();
    names = in_table.column_names();
    assert(isempty(names))
    in_table = in_table.from_file(infilename);
    names = in_table.column_names();
    assert(strcmp(names(1, :),'data1'))
    assert(strcmp(names(2, :),'data2'))

    %% Test column_type(column):
    in_table = in_table.clear();
    assert(strcmp(in_table.column_type('data1'), ''))
    in_table = in_table.from_file(infilename);
    assert(strcmp(in_table.column_type('data1'), 'double'))

    %% Test number_of_rows():
    in_table = in_table.clear();
    assert(in_table.number_of_rows() == 0)
    in_table = in_table.from_file(infilename);
    assert(in_table.number_of_rows() == 2)

    %% Test number_of_columns():
    in_table = in_table.clear();
    assert(in_table.number_of_columns() == 0)
    in_table = in_table.from_file(infilename);
    assert(in_table.number_of_columns() == 10)

    %% Test is_empty():
    in_table = in_table.clear();
    assert(in_table.is_empty())
    in_table = in_table.from_file(infilename);
    assert(~in_table.is_empty())

    %% Test to_file(filename):
    filename = 'test_filename.mat';
    in_table = in_table.clear();
    in_table = in_table.from_file(infilename);
    in_table.to_file(filename);
    test = in_table.from_file(filename);
    names = in_table.column_names();
    assert(strcmp(names(1, :),'data1'))
    assert(strcmp(names(2, :),'data2'))
    delete(filename)

    %% Test set_column_from_array(column, array, attributes):
    in_table = in_table.clear();
    test_array = 10:19;
    in_table = in_table.set_column_from_array('data3', test_array, {});
    names = in_table.column_names();
    assert(strcmp(names(1, :),'data3'))
    array = in_table.get_column_to_array('data3');
    for i=1:length(test_array)
        assert(array(i) == test_array(i))
    end
    in_table = in_table.clear();
    in_table = in_table.from_file(infilename);
    test_array = 10:19;
    in_table = in_table.set_column_from_array('data3', test_array, {});
    names = in_table.column_names();
    assert(strcmp(names(1, :),'data1'))
    assert(strcmp(names(2, :),'data2'))
    assert(strcmp(names(3, :),'data3'))
    array = in_table.get_column_to_array('data3');
    for i=1:length(test_array)
        assert(array(i) == test_array(i))
    end
    assert(isempty(in_table.get_column_attributes('data3')))
    assert(isempty(in_table.get_table_attributes()))
    attr = in_table.get_attributes();
    assert(isempty(attr{1}))

    %% Test get_column_to_array(column):
    in_table = in_table.clear();
    in_table = in_table.from_file(infilename);
    test_array = 0:9;
    array = in_table.get_column_to_array('data1');
    for i=1:length(test_array)
        assert(array(i) == test_array(i))
    end

    %% Test set_name(name) and get_name():
    in_table = in_table.clear();
    in_table = in_table.from_file(infilename);
    assert(strcmp(in_table.get_name(), ''))
    in_table = in_table.set_name('test');
    assert(strcmp(in_table.get_name(), 'test'))

    %% Test get_column_attributes(column) and set_column_attributes(column, attributes):
    in_table = in_table.clear();
    in_table = in_table.from_file(infilename);
    attr = in_table.get_column_attributes('data1');
    assert(~length(attr))
    test_attr = {'test_attr' 1};
    in_table = in_table.set_column_attributes('data1', test_attr);
    attr = in_table.get_column_attributes('data1');
    assert(strcmp(attr{1}, test_attr{1}))
    assert(attr{2} == test_attr{2})

    %% Test get_column_attributes(column) and get_column_attributes(column, attributes):
    in_table = in_table.clear();
    in_table = in_table.from_file(infilename);
    attr = in_table.get_table_attributes();
    assert(isempty(attr))
    test_attr = {'test_attr' 1};
    in_table = in_table.set_table_attributes(test_attr);
    attr = in_table.get_table_attributes();
    assert(~isempty(attr))
    assert(strcmp(attr{1}, test_attr{1}))
    assert(attr{2} == test_attr{2})

    %% Test get_attributes() and set_attributes():
    in_table = in_table.clear();
    in_table = in_table.from_file(infilename);
    attr = in_table.get_attributes();
    assert(isempty(attr{1}))
    test_attr = {{} {{'test_attr' 1}}};
    in_table = in_table.set_attributes(test_attr);
    attr = in_table.get_attributes();
    assert(isempty(attr{1}))

    assert(strcmp(attr{2}{1}{1}, test_attr{2}{1}{1}))
    assert(attr{2}{1}{2} == test_attr{2}{1}{2})

    %% Test has_column(key):
    in_table = in_table.clear();
    in_table = in_table.from_file(infilename);
    assert(in_table.has_column('data1'))
    assert(in_table.has_column('data2'))
    assert(~in_table.has_column('data3'))


    %% Test attrs()
    in_table = in_table.clear();
    in_table = in_table.from_file(infilename);
    attr = in_table.attrs();
    assert(isempty(attr{1}))
    test_attr = {{} {{'test_attr' 1}}};
    in_table = in_table.set_attributes(test_attr);
    attr = in_table.attrs();
    assert(isempty(attr{1}))

    assert(strcmp(attr{2}{1}{1}, test_attr{2}{1}{1}))
    assert(attr{2}{1}{2} == test_attr{2}{1}{2})

    %% Test attrs(name)
    in_table = in_table.clear();
    in_table = in_table.from_file(infilename);
    value = in_table.attr('TEST');
    assert(isempty(value))
    test_attr = {{'test' 2} {{'test_attr' 1}}};
    in_table = in_table.set_attributes(test_attr);

    value = in_table.attr('test');
    assert(value == 2)

    %% Test source(other_table)
    table = Table();
    names = table.column_names();
    assert(isempty(names))

    in_table = in_table.clear();
    in_table = in_table.from_file(infilename);
    table = table.source(in_table);
    names = in_table.column_names();
    assert(strcmp(names(1, :),'data1'))
    assert(strcmp(names(2, :),'data2'))

    test_array1 = in_table.get_column_to_array('data1');
    test_array2 = in_table.get_column_to_array('data2');

    array1 = table.get_column_to_array('data1');
    array2 = table.get_column_to_array('data2');

    for i=1:length(test_array1)
        assert(array1(i) == test_array1(i))
        assert(array2(i) == test_array2(i))
    end

    %% Test update(other_table)
    table = Table();
    names = table.column_names();
    assert(isempty(names))

    in_table = in_table.clear();
    in_table = in_table.from_file(infilename);

    table = table.update(in_table);
    names = in_table.column_names();
    assert(strcmp(names(1, :),'data1'))
    assert(strcmp(names(2, :),'data2'))

    test_array1 = in_table.get_column_to_array('data1');
    test_array2 = in_table.get_column_to_array('data2');

    array1 = table.get_column_to_array('data1');
    array2 = table.get_column_to_array('data2');

    for i=1:length(test_array1)
        assert(array1(i) == test_array1(i))
        assert(array2(i) == test_array2(i))
    end

    in_table = in_table.set_column_from_array('data1', 10:19, {});
    table = table.update(in_table);
    names = in_table.column_names();
    assert(strcmp(names(1, :),'data1'))
    assert(strcmp(names(2, :),'data2'))

    test_array1 = in_table.get_column_to_array('data1');
    test_array2 = in_table.get_column_to_array('data2');

    array1 = table.get_column_to_array('data1');
    array2 = table.get_column_to_array('data2');

    for i=1:length(test_array1)
        assert(array1(i) == test_array1(i))
        assert(array2(i) == test_array2(i))
    end

    %% Test update_column(column_name, other_table, other_name)
    table = Table();
    names = table.column_names();
    assert(isempty(names))

    in_table = in_table.clear();
    in_table = in_table.from_file(infilename);
    names = in_table.column_names();
    assert(strcmp(names(1, :),'data1'))

    table = table.update_column('test', in_table, 'data1');
    names = table.column_names();
    assert(strcmp(names(1, :),'test'))

    array = in_table.get_column_to_array('data1');
    test_array = table.get_column_to_array('test');
    for i=1:length(test_array)
        assert(array(i) == test_array(i))
    end

    %% Test hjoin(other_table)
    table = Table();
    names = table.column_names();
    assert(isempty(names))

    in_table = in_table.clear();
    in_table = in_table.from_file(infilename);

    table = table.hjoin(in_table);
    names = in_table.column_names();
    assert(strcmp(names(1, :),'data1'))
    assert(strcmp(names(2, :),'data2'))

    test_array1 = in_table.get_column_to_array('data1');
    test_array2 = in_table.get_column_to_array('data2');

    array1 = table.get_column_to_array('data1');
    array2 = table.get_column_to_array('data2');

    for i=1:length(test_array1)
        assert(array1(i) == test_array1(i))
        assert(array2(i) == test_array2(i))
    end

    in_table = in_table.set_column_from_array('data1', 10:19, {});
    table = table.hjoin(in_table);
    names = in_table.column_names();
    assert(strcmp(names(1, :),'data1'))
    assert(strcmp(names(2, :),'data2'))

    test_array1 = in_table.get_column_to_array('data1');
    test_array2 = in_table.get_column_to_array('data2');

    array1 = table.get_column_to_array('data1');
    array2 = table.get_column_to_array('data2');

    for i=1:length(test_array1)
        assert(array1(i) == test_array1(i))
        assert(array2(i) == test_array2(i))
    end
catch
    exit(1)
end
