"""Test module for hpp2plantuml"""

# %% Imports


import os
import io
import sys
import re
import nose.tools as nt
import CppHeaderParser
import hpp2plantuml

test_fold = os.path.abspath(os.path.dirname(__file__))

# %% Helper functions


def get_parsed_element(input_str):
    return CppHeaderParser.CppHeader(input_str, argType='string')


@nt.nottest
def fix_test_list_def(test_list):
    test_list_out = []
    for test_entry in test_list:
        test_entry_out = []
        for test_str in test_entry:
            test_entry_out.append(re.sub(u'@', '|', test_str))
        test_list_out.append(test_entry_out)
    return test_list_out

# %% Test containers


class TestContainer:
    def test_init(self):
        c_type = "container_type"
        c_name = "container_name"
        c_obj = hpp2plantuml.hpp2plantuml.Container(c_type, c_name)
        nt.assert_equal(c_obj.get_name(), c_name)
        nt.assert_equal(c_obj.render(), 'container_type container_name {\n}\n')

    def test_comparison_keys(self):
        c_list = [
            ['class', 'ABD'],
            ['enum', 'ABDa'],
            ['class', 'abcd'],
        ]
        ref_sort_idx = [0, 2, 1]
        c_obj_list = []
        for c_type, c_name in c_list:
            c_obj_list.append(hpp2plantuml.hpp2plantuml.Container(
                c_type, c_name))
        c_obj_list.sort(key=lambda obj: obj.comparison_keys())

        for i in range(len(c_list)):
            nt.assert_equal(c_obj_list[i].get_name(),
                            c_list[ref_sort_idx[i]][1])

test_list_classvar=[["""class Test {
public:
int member; };""", "+member : int"], ["""class Test {
private:
int * member; };""", "-member : int*"], ["""class Test {
protected:
int &member; };""", "#member : int&"]]
# %% Test class variables


class TestClassVariable:
    def test_list_entries(self):
        for test_idx, (input_str, output_ref_str) in \
            enumerate(fix_test_list_def(test_list_classvar)):
            p = get_parsed_element(input_str)
            class_name = re.sub(r'.*(class|struct)\s*(\w+).*', r'\2',
                                input_str.replace('\n', ' '))
            class_input = [class_name, p.classes[class_name]]
            obj_c = hpp2plantuml.hpp2plantuml.Class(class_input)
            obj_m = obj_c._member_list[0]
            nt.assert_equal(output_ref_str, obj_m.render(),
                            'Test {0} failed [input: {1}]'.format(test_idx,
                                                                  input_str))

test_list_classmethod=[["""class Test {
public:
int & func(int * a); };""", "+func(int* a) : int&"], ["""class Test {
public:
static int func(int & a); };""", "+{static} func(int& a) : int"], ["""class Test {
private:
virtual int * func() const = 0; };""", "-{abstract} func() : int* {query}"], ["""class Test {
public:
~Test(); };""", "+~Test()"], ["""class Test {
protected:
template <typename T>int &func(string &) const; };""", "#func(string &) : int& {query}"]]
# %% Test class methods


class TestClassMethod:
    def test_list_entries(self):
        for test_idx, (input_str, output_ref_str) in \
            enumerate(fix_test_list_def(test_list_classmethod)):
            p = get_parsed_element(input_str)
            class_name = re.sub(r'.*(class|struct)\s*(\w+).*', r'\2',
                                input_str.replace('\n', ' '))
            class_input = [class_name, p.classes[class_name]]
            obj_c = hpp2plantuml.hpp2plantuml.Class(class_input)
            obj_m = obj_c._member_list[0]
            nt.assert_equal(output_ref_str, obj_m.render(),
                            'Test {0} failed [input: {1}]'.format(test_idx,
                                                                  input_str))

test_list_class=[["""class Test {
protected:
int & member; };""", """class Test {
	#member : int&
}
"""], ["""struct Test {
protected:
int & member; };""", """struct Test {
	#member : int&
}
"""], ["""class Test
{
public:
virtual int func() = 0; };""", """abstract class Test {
	+{abstract} func() : int
}
"""], ["""template <typename T> class Test{
T* func(T& arg); };""", """class Test <template<typename T>> {
	-func(T& arg) : T*
}
"""], ["""template <typename T> class Test{
virtual T* func(T& arg)=0; };""", """abstract class Test <template<typename T>> {
	-{abstract} func(T& arg) : T*
}
"""], ["""namespace Interface {
class Test {
protected:
int & member; };};""", """namespace Interface {
	class Test {
		#member : int&
	}
}
"""]]
# %% Test classes


class TestClass:
    def test_list_entries(self):
        for test_idx, (input_str, output_ref_str) in \
            enumerate(fix_test_list_def(test_list_class)):
            p = get_parsed_element(input_str)
            class_name = re.sub(r'.*(class|struct)\s*(\w+).*', r'\2',
                                input_str.replace('\n', ' '))
            class_input = [class_name, p.classes[class_name]]
            obj_c = hpp2plantuml.hpp2plantuml.Class(class_input)
            nt.assert_equal(output_ref_str, obj_c.render(),
                            'Test {0} failed [input: {1}]'.format(test_idx,
                                                                  input_str))

test_list_enum=[["enum Test { A, B, CD, E };", """enum Test {
	A
	B
	CD
	E
}
"""], ["""enum Test
{
 A = 0, B = 12
 };""", """enum Test {
	A
	B
}
"""], ["enum { A, B };", """enum empty {
	A
	B
}
"""]]
# %% Test enum objects


class TestEnum:
    def test_list_entries(self):
        for test_idx, (input_str, output_ref_str) in \
            enumerate(fix_test_list_def(test_list_enum)):
            p = get_parsed_element(input_str)
            enum_name = re.sub(r'.*enum\s*(\w+).*', r'\1',
                               input_str.replace('\n', ' '))
            enum_input = p.enums[0]
            obj_c = hpp2plantuml.hpp2plantuml.Enum(enum_input)
            nt.assert_equal(output_ref_str, obj_c.render(),
                            'Test {0} failed [input: {1}]'.format(test_idx,
                                                                  input_str))

test_list_link=[["""class A{};
class B : A{};""", """A <@-- B
"""], ["""class A{};
class B : public A{};""", """A <@-- B
"""], ["""class B{};
class A{B obj;};""", """A *-- B
"""], ["""class B{};
class A{B* obj;};""", """A o-- B
"""], ["""class B{};
class A{B * obj_ptr; B* ptr;};""", """A \"2\" o-- B
"""], ["""class A{};
class B{void Method(A* obj);};""", """A <.. B
"""], ["namespace T {class A{}; class B: A{};};", """namespace T {
	A <@-- B
}
"""], ["""namespace T {
class A{};};
class B{T::A* _obj;};""", """.B o-- T.A
"""]]
class TestLink:
    def test_list_entries(self):
        for test_idx, (input_str, output_ref_str) in \
            enumerate(fix_test_list_def(test_list_link)):
            obj_d = hpp2plantuml.Diagram(flag_dep=True)
            # Not very unittest-y
            obj_d.create_from_string(input_str)
            if len(obj_d._inheritance_list) > 0:
                obj_l = obj_d._inheritance_list[0]
            elif len(obj_d._aggregation_list) > 0:
                obj_l = obj_d._aggregation_list[0]
            elif len(obj_d._dependency_list) > 0:
                obj_l = obj_d._dependency_list[0]
            nt.assert_equal(output_ref_str, obj_l.render(),
                            'Test {0} failed [input: {1}]'.format(test_idx,
                                                                  input_str))

# %% Test overall system


class TestFullDiagram():

    def __init__(self):
        self._input_files = ['simple_classes_1_2.hpp', 'simple_classes_3.hpp']
        self._input_files_w = ['simple_classes_*.hpp', 'simple_classes_3.hpp']
        self._diag_saved_ref = ''
        with open(os.path.join(test_fold, 'simple_classes.puml'), 'rt') as fid:
            self._diag_saved_ref = fid.read()
        self._diag_saved_ref_nodep = ''
        with open(os.path.join(test_fold,
                               'simple_classes_nodep.puml'), 'rt') as fid:
            self._diag_saved_ref_nodep = fid.read()

    def test_full_files(self):
        self._test_full_files_helper(False)
        self._test_full_files_helper(True)

    def _test_full_files_helper(self, flag_dep=False):
        # Create first version
        file_list_ref = list(set(hpp2plantuml.hpp2plantuml.expand_file_list(
            [os.path.join(test_fold, f) for f in self._input_files])))
        diag_ref = hpp2plantuml.Diagram(flag_dep=flag_dep)
        diag_ref.create_from_file_list(file_list_ref)
        diag_render_ref = diag_ref.render()

        # Compare to saved reference
        if flag_dep:
            saved_ref = self._diag_saved_ref
        else:
            saved_ref = self._diag_saved_ref_nodep
        nt.assert_equal(saved_ref, diag_render_ref)

        # # Validate equivalent inputs

        # File expansion
        for file_list in [self._input_files, self._input_files_w]:
            file_list_c = list(set(hpp2plantuml.hpp2plantuml.expand_file_list(
                [os.path.join(test_fold, f) for f in file_list])))

            # Create from file list
            diag_c = hpp2plantuml.Diagram(flag_dep=flag_dep)
            diag_c.create_from_file_list(file_list_c)
            nt.assert_equal(diag_render_ref, diag_c.render())

            # Add from file list
            diag_c_add = hpp2plantuml.Diagram(flag_dep=flag_dep)
            diag_c_add.add_from_file_list(file_list_c)
            diag_c_add.build_relationship_lists()
            diag_c_add.sort_elements()
            nt.assert_equal(diag_render_ref, diag_c_add.render())

            # Create from first file, add from rest of the list
            diag_c_file = hpp2plantuml.Diagram(flag_dep=flag_dep)
            diag_c_file.create_from_file(file_list_c[0])
            for file_c in file_list_c[1:]:
                diag_c_file.add_from_file(file_c)
            diag_c_file.build_relationship_lists()
            diag_c_file.sort_elements()
            nt.assert_equal(diag_render_ref, diag_c_file.render())

        # String inputs
        input_str_list = []
        for file_c in file_list_ref:
            with open(file_c, 'rt') as fid:
                input_str_list.append(fid.read())

        # Create from string list
        diag_str_list = hpp2plantuml.Diagram(flag_dep=flag_dep)
        diag_str_list.create_from_string_list(input_str_list)
        nt.assert_equal(diag_render_ref, diag_str_list.render())

        # Add from string list
        diag_str_list_add = hpp2plantuml.Diagram(flag_dep=flag_dep)
        diag_str_list_add.add_from_string_list(input_str_list)
        diag_str_list_add.build_relationship_lists()
        diag_str_list_add.sort_elements()
        nt.assert_equal(diag_render_ref, diag_str_list_add.render())

        # Create from string
        diag_str = hpp2plantuml.Diagram(flag_dep=flag_dep)
        diag_str.create_from_string('\n'.join(input_str_list))
        nt.assert_equal(diag_render_ref, diag_str.render())
        # Reset and parse
        diag_str.clear()
        diag_str.create_from_string('\n'.join(input_str_list))
        nt.assert_equal(diag_render_ref, diag_str.render())

        # Manually build object
        diag_manual_add = hpp2plantuml.Diagram(flag_dep=flag_dep)
        for idx, (file_c, string_c) in enumerate(zip(file_list_ref,
                                                     input_str_list)):
            if idx == 0:
                diag_manual_add.add_from_file(file_c)
            else:
                diag_manual_add.add_from_string(string_c)
        diag_manual_add.build_relationship_lists()
        diag_manual_add.sort_elements()
        nt.assert_equal(diag_render_ref, diag_manual_add.render())

    def test_main_function(self):
        #self._test_main_function_helper(False)
        self._test_main_function_helper(True)

    def _test_main_function_helper(self, flag_dep=False):

        # List files
        file_list = [os.path.join(test_fold, f) for f in self._input_files]

        # Output to string
        with io.StringIO() as io_stream:
            sys.stdout = io_stream
            hpp2plantuml.CreatePlantUMLFile(file_list, flag_dep=flag_dep)
            io_stream.seek(0)
            # Read string output, exclude final line return
            output_str = io_stream.read()[:-1]
        sys.stdout = sys.__stdout__
        if flag_dep:
            saved_ref = self._diag_saved_ref
        else:
            saved_ref = self._diag_saved_ref_nodep
        nt.assert_equal(saved_ref, output_str)

        # Output to file
        output_fname = 'output.puml'
        for template in [None, os.path.join(test_fold,
                                            'custom_template.puml')]:
            hpp2plantuml.CreatePlantUMLFile(file_list, output_fname,
                                            template_file=template,
                                            flag_dep=flag_dep)
            output_fcontent = ''
            with open(output_fname, 'rt') as fid:
                output_fcontent = fid.read()
            if template is None:
                # Default template check
                nt.assert_equal(saved_ref, output_fcontent)
            else:
                # Check that all lines of reference are in the output
                ref_re = re.search('(@startuml)\s*(.*)', saved_ref, re.DOTALL)
                assert ref_re
                # Build regular expression: allow arbitrary text between
                # @startuml and the rest of the string
                ref_groups = ref_re.groups()
                match_re = re.compile('\n'.join([
                    re.escape(ref_groups[0]),    # @startuml line
                    '.*',                        # preamble
                    re.escape(ref_groups[1])]),  # main output
                                      re.DOTALL)
                nt.assert_true(match_re.search(output_fcontent))
        os.unlink(output_fname)
