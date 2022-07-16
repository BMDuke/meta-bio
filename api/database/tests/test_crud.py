import unittest

from fastapi import HTTPException
from sqlalchemy.exc import DataError, DatabaseError, \
                            OperationalError, \
                            StatementError, \
                            TimeoutError

from database.crud import handle_database_errors

'''
This file contains the unit tests which we will run against the database
connection decorator to ensure that it handles exceptions appropriately. 

'''

class TestStringMethods(unittest.TestCase):

    '''
    Test suite designed to test the error handling decorator used in
    the crud.py file.
    '''

    def test_data_error(self):
        '''
        Test for data errors
        '''

        @handle_database_errors
        def test():
            raise DataError('','','')

        with self.assertRaises(HTTPException) as exc: 
            test()


    def test_database_error(self):
        '''
        Test for database errors
        '''

        @handle_database_errors
        def test():
            raise DatabaseError('','','')

        with self.assertRaises(HTTPException) as exc: 
            test()   


    def test_operational_error(self):
        '''
        Test for operational errors
        '''

        @handle_database_errors
        def test():
            raise OperationalError('','','')

        with self.assertRaises(HTTPException) as exc: 
            test()                        
      

    def test_statement_error(self):
        '''
        Test for statement errors
        '''

        @handle_database_errors
        def test():
            raise StatementError('','','','')

        with self.assertRaises(HTTPException) as exc: 
            test()       


    def test_timeout_error(self):
        '''
        Test for timeout errors
        '''

        @handle_database_errors
        def test():
            raise TimeoutError('','','')

        with self.assertRaises(HTTPException) as exc: 
            test()     
                  

if __name__ == '__main__':
    unittest.main()