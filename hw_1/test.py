from data import *
from unittest import TestCase
from unittest.mock import patch
from unittest import mock
from main import (
    add_new_doc,
    delete_doc,
    add_new_shelf,
    append_doc_to_shelf,
    get_doc_shelf,
    get_all_doc_owners_names,
    check_document_existance,
    remove_doc_from_shelf,
    move_doc_to_shelf,
    show_document_info,
    show_all_docs_info,
    get_doc_owner_name,
)


class TestAppUnitTest(TestCase):
    def test_check_document_existance(self):
        self.assertEqual(check_document_existance('10006', documents), True)
        self.assertEqual(check_document_existance('', documents), False)

    def test_get_doc_owner_name(self):
        self.assertEqual(get_doc_owner_name('10006', documents), 'Аристарх Павлов')

    def test_get_all_doc_owners_names(self):
        all_owners_names = {'Геннадий Покемонов', 'Василий Гупкин', 'Аристарх Павлов'}
        self.assertEqual(get_all_doc_owners_names(documents), all_owners_names)

    def test_remove_doc_from_shelf(self):
        remove_doc_from_shelf('10006', directories)
        self.assertEqual(get_doc_shelf('10006', directories), None)

    def test_add_new_shelf(self):
        self.assertEqual(add_new_shelf('4'), ('4', True))
        self.assertEqual(add_new_shelf('2'), ('2', False))

    def test_append_doc_to_shelf(self):
        append_doc_to_shelf('123', '3', directories)
        self.assertEqual(directories['3'], ['123'])

    @patch('main.check_document_existance', return_value=True)
    @patch('main.remove_doc_from_shelf', return_value=None)
    def test_delete_doc(self, remove_mock, check_mock):
        self.assertEqual(delete_doc('10006', documents_2, directories_2), ('10006', True))
        remove_mock.assert_called_once_with('10006', directories_2)
        check_mock.assert_called_once_with('10006', documents_2)

    def test_get_doc_shelf(self):
        self.assertEqual(get_doc_shelf('10006', directories), '2')

    @patch('main.print', return_value=None)
    @patch('main.remove_doc_from_shelf', return_value=None)
    @patch('main.append_doc_to_shelf', return_value=None)
    def test_move_doc_to_shelf(self, append_mock, remove_mock, print_mock):
        move_doc_to_shelf('10006', '3', directories)
        remove_mock.assert_called_once_with('10006', directories)
        append_mock.assert_called_once_with('10006', '3', directories)
        print_mock.assert_called_once_with('Документ номер "10006" был перемещен на полку номер "3"')

    @patch('main.print', return_value=None)
    def test_show_document_info(self, print_mock):
        show_document_info(document)
        print_mock.assert_called_once_with('insurance "10006" "Аристарх Павлов"')

    @patch('main.show_document_info', return_value=None)
    def test_show_all_docs_info(self, show_mock):
        show_all_docs_info(documents)
        test_calls = [
            mock.call({'type': 'passport', 'number': '2207 876234', 'name': 'Василий Гупкин'}),
            mock.call({'type': 'invoice', 'number': '11-2', 'name': 'Геннадий Покемонов'}),
            mock.call({'type': 'insurance', 'number': '10006', 'name': 'Аристарх Павлов'}),
        ]
        show_mock.assert_has_calls(test_calls)

    @patch('main.append_doc_to_shelf', return_value=None)
    def test_add_new_doc(self, append_mock):
        add_new_doc('123', 'test', 'Test', '3', documents_2, directories)
        append_mock.assert_called_once_with('123', '3', directories)
        self.assertEqual(check_document_existance('123', documents_2), True)
        self.assertEqual(documents_2[3], {'name': 'Test', 'number': '123', 'type': 'test'})
