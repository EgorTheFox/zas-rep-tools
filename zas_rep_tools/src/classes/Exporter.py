#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# : XXX{Information about this code}XXX
# Author:
# c(Developer) ->     {'Egor Savin'}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

###Programm Info######
#
#
#
#
#
from __future__ import absolute_import


import os
#import copy
import sys
#import regex
import logging
#import collections
#import types
import csv
#import unicodecsv as csv
import codecs
from lxml import etree as ET
import json
import inspect
import traceback


from collections import defaultdict
from raven import Client
#from cached_property import cached_property

#from zas_rep_tools.src.classes.configer import Configer

from zas_rep_tools.src.utils.helpers import set_class_mode, print_mode_name, LenGen, path_to_zas_rep_tools
from zas_rep_tools.src.classes.dbhandler import DBHandler

from zas_rep_tools.src.utils.logger import *
from zas_rep_tools.src.utils.debugger import p
from zas_rep_tools.src.utils.error_tracking import initialisation
from zas_rep_tools.src.utils.traceback_helpers import print_exc_plus



import platform
if platform.uname()[0].lower() !="windows":
    import colored_traceback
    colored_traceback.add_hook()
else:
    import colorama


class Exporter(object):

    supported_file_formats = ["csv", "json", "csv", "txt", "xml"]

    def __init__(self, inpdata, rewrite=False, silent_ignore=False,
                logger_folder_to_save=False,  logger_usage=True, logger_level=logging.INFO,
                logger_save_logs=True, logger_num_buffered=5, error_tracking=True,
                ext_tb=False, logger_traceback=False, mode="prod"):

        
        ## Set Mode: Part 1
        self._mode = mode
        if mode != "free":
            _logger_level, _logger_traceback, _logger_save_logs = set_class_mode(self._mode)
            logger_level = _logger_level if _logger_level!=None else logger_level
            logger_traceback = _logger_traceback if _logger_traceback!=None else logger_traceback
            logger_save_logs = _logger_save_logs if _logger_save_logs!=None else logger_save_logs

    
    
        ## Logger Initialisation
        self._logger_level = logger_level
        self._logger_traceback =logger_traceback
        self._logger_folder_to_save = logger_folder_to_save
        self._logger_usage = logger_usage
        self._logger_save_logs = logger_save_logs
        self.logger = main_logger(self.__class__.__name__, level=self._logger_level, folder_for_log=self._logger_folder_to_save, use_logger=self._logger_usage, save_logs=self._logger_save_logs)

        ## Set Mode: Part 2:
        print_mode_name(self._mode, self.logger)


        self.logger.debug('Beginn of creating an instance of {}()'.format(self.__class__.__name__))



        #Input: Incaplusation:
        self._inpdata = inpdata
        self._numbers_of_alredy_created_files = defaultdict(lambda: defaultdict(int))
        self._number_of_inserts_in_the_current_file = 0
        self._ext_tb = ext_tb
        #self._fieldnames = fieldnames
        self.sqlite_db = False
        self._rewrite = rewrite
        self._silent_ignore = silent_ignore

        self._error_tracking = error_tracking

        #p(inpdata)

        #InstanceAttributes: Initialization
        self._used_fnames = {}



        ## Error-Tracking:Initialization #1
        if self._error_tracking:
            self.client = initialisation()
            self.client.context.merge({'InstanceAttributes': self.__dict__})


        self.logger.debug('Intern InstanceAttributes was initialized')


        if not self._eval_input_data():
            sys.exit()


        self.logger.debug('An instance of Exporter() was created ')

        ############################################################
        ####################__init__end#############################
        ############################################################

    # def __del__(self):
    #     self.logger.newline(1)

####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
######################################Extern########################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################



###########################+++++++++############################





    def tocsv(self, path_to_export_dir , fname, fieldnames,  rows_limit_in_file=50000, encoding="utf-8"):
        self.current_csvfile = False
        rows_was_exported = 0
        for row in self._inpdata:
            #p(row)
            try:
                if not self._write_to_csv_files(row, fieldnames, path_to_export_dir, fname, rows_limit_in_file=rows_limit_in_file, encoding=encoding):
                    if self._silent_ignore:
                        self.logger.debug("toCSV: File is already exist and extraction was stopped. ('silent_ignore' is 'on')")
                    else:    
                        self.logger.info("toCSV: Test Files are already exist. Extraction to_json was stopped. Please remove those files or use 'rewrite' option. ")
                    return False
                
                rows_was_exported += 1
            except Exception, e:
                print_exc_plus() if self._ext_tb else ""
                self.logger.error("CSVWriterError: Not possible to Export into CSV. Following Exception was throw: '{}'.".format(e), exc_info=self._logger_traceback)
                return False
        self.current_csvfile.close()
        self.logger.info("CSVWriter: '{}' rows  was exported into CSV File(s) in '{}'.".format(rows_was_exported,path_to_export_dir))
        return True





    def toxml(self, path_to_export_dir , fname, rows_limit_in_file=50000, encoding="utf-8", root_elem_name="Docs", row_elem_name="Doc"):
        self.current_xmlfile = False
        rows_was_exported = 0
        for row in self._inpdata:
            try:
                if not self._write_to_xml_files(row,  path_to_export_dir, fname, rows_limit_in_file=rows_limit_in_file, encoding=encoding, root_elem_name=root_elem_name, row_elem_name=row_elem_name):
                    if self._silent_ignore:
                        self.logger.debug("toXML: File is already exist and extraction was stopped. ('silent_ignore' is 'on')")
                    else:    
                        self.logger.info("toXML: Test Files are already exist. Extraction to_json was stopped. Please remove those files or use 'rewrite' option. ")
                    #p("ghjkl")
                    return False
                rows_was_exported += 1
            except Exception, e:
                print_exc_plus() if self._ext_tb else ""
                self.logger.error("XMLWriterError: Not possible to Export into XML. Following Exception was throw: '{}'.".format(e), exc_info=self._logger_traceback)
                return False
        #to save all last data
        self._save_output_into_current_xml_file()
        self.logger.info("XMLWriter: '{}' rows  was exported into XML File(s) in '{}'.".format(rows_was_exported,path_to_export_dir))
        return True




    # def tojson(self, path_to_export_dir , fname, rows_limit_in_file=50000, encoding="utf-8", unicode_encode=True):
    #     self.current_jsonfile = False
    #     rows_was_exported = 0
    #     for row in self._inpdata:
    #         #p(row)
    #         try:
    #         #p((row,  path_to_export_dir, fname))
    #             if not self._write_to_json_files(row,  path_to_export_dir, fname, rows_limit_in_file=rows_limit_in_file, encoding=encoding, unicode_encode=unicode_encode):
    #                 self.logger.info("toJSON: Test Files are already exist. Extraction to_json was stopped. Please remove those files or use 'rewrite' option. ")
    #                 return False
    #             rows_was_exported += 1

    #         except Exception, e:
    #             print_exc_plus() if self._ext_tb else ""
    #             self.logger.error("JSONWriterError: Not possible to Export into JSON. Following Exception was throw: '{}'.".format(e), exc_info=self._logger_traceback)
    #             return False

    #     self.current_jsonfile.seek(-1, os.SEEK_END)
    #     #self.current_jsonfile.truncate()
    #     #self.current_jsonfile.write("test")
    #     self.current_jsonfile.write("\n\n ]")
    #     self.current_jsonfile.close()
    #     #self._save_output_into_current_xml_file()
    #     self.logger.info("JSONWriter: '{}' rows  was exported into JSONS File(s) in '{}'.".format(rows_was_exported,path_to_export_dir))


    def tojson(self, path_to_export_dir , fname, rows_limit_in_file=50000, encoding="utf-8", unicode_encode=True):
        self.current_jsonfile = False
        rows_was_exported = 0
        for row in self._inpdata:
            #p(row)
            try:
            #p((row,  path_to_export_dir, fname))
                if not self._write_to_json_files(row,  path_to_export_dir, fname, rows_limit_in_file=rows_limit_in_file, encoding=encoding, unicode_encode=unicode_encode):
                    if self._silent_ignore:
                        self.logger.debug("toJSON: File is already exist and extraction was stopped. ('silent_ignore' is 'on')")
                    else:    
                        self.logger.info("toJSON: Test Files are already exist. Extraction to_json was stopped. Please remove those files or use 'rewrite' option. ")
                    return False
                rows_was_exported += 1

            except Exception, e:
                print_exc_plus() if self._ext_tb else ""
                self.logger.error("JSONWriterError: Not possible to Export into JSON. Following Exception was throw: '{}'.".format(e), exc_info=self._logger_traceback)
                return False

        self.current_jsonfile.seek(-1, os.SEEK_END)
        self.current_jsonfile.write("\n\n ]")
        self.current_jsonfile.close()
        self.logger.info("JSONWriter: '{}' rows  was exported into JSONS File(s) in '{}'.".format(rows_was_exported,path_to_export_dir))
        return True





    def tosqlite(self, path_to_export_dir, dbname, fieldnames,  encoding="utf-8", encryption_key=False, table_name= "Documents", attributs_names_with_types_as_str=False):
        self.current_jsonfile = False
        rows_was_exported = 0

        if not  attributs_names_with_types_as_str:
            attributs_names_with_types_as_str = self._create_list_with_columns_and_types_for_sqlite(fieldnames)
            #p(attributs_names_with_types_as_str)

        if not self.sqlite_db: 
            self.sqlite_db = DBHandler( rewrite=self._rewrite, stop_if_db_already_exist=True, logger_level= self._logger_level,logger_traceback=self._logger_traceback, logger_folder_to_save=self._logger_folder_to_save,logger_usage=self._logger_usage, logger_save_logs= self._logger_save_logs, mode=self._mode ,  error_tracking=self._error_tracking,  ext_tb= self._ext_tb) 
            
            if not self.sqlite_db.initempty(path_to_export_dir, dbname, encryption_key=encryption_key):
                if self._silent_ignore:
                    self.logger.debug("toSQLLITE: File is already exist and extraction was stopped. ('silent_ignore' is 'on')")
                else:    
                    self.logger.info("toSQLITE: Test Files are already exist. Extraction to_json was stopped. Please remove those files or use 'rewrite' option. ")
                return False

            self.sqlite_db.addtable(table_name, attributs_names_with_types_as_str)

        for row in self._inpdata:
            #p(row)
            #try:
            self._write_to_sqliteDB(row,  path_to_export_dir, table_name,  encoding=encoding)
            rows_was_exported += 1

            # except Exception, e:
            #    self.logger.error("SQLITEWriterError: Not possible to Export into SQLITE-DB. Following Exception was throw: '{}'.".format(e), exc_info=self._logger_traceback)
            #    return False

        try:
            self.sqlite_db.close()
        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("SQLITEWriterError: Following Exception was throw: '{}'. ".format(e), exc_info=self._logger_traceback)

        self.logger.info("SQLITEWriter: '{}' rows  was exported into SQLITE-DB in '{}'.".format(rows_was_exported,path_to_export_dir))
        return True






    def totxt(self):
        self.logger.error("TXTReader is not implemented!", exc_info=self._logger_traceback)
        sys.exit()



####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
######################################INTERN########################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################




    def _write_to_json_files(self,row_as_dict, path_to_dir, fname, rows_limit_in_file=50000, encoding="utf-8",unicode_encode=True):
        # check if current file has not more row as given rows limits
        

        if self.current_jsonfile:
            if self._number_of_inserts_in_the_current_file >= rows_limit_in_file:
                self.current_jsonfile.seek(-1, os.SEEK_END)
                self.current_jsonfile.write("\n\n ]")
                self.current_jsonfile.close()
                self._number_of_inserts_in_the_current_file = 0
                self.current_jsonfile = self._get_new_file(path_to_dir , fname, "json", encoding=encoding, file_flag="a+", open_file_with_codecs=unicode_encode)
                if not self.current_jsonfile:
                    return False
                self.current_jsonfile.write("[ \n\n")
        
        else:
            self.current_jsonfile = self._get_new_file(path_to_dir , fname, "json", encoding=encoding, file_flag="a+", open_file_with_codecs=unicode_encode)
            #p(self.current_jsonfile, c="m")
            if not self.current_jsonfile:
                return False
            self.current_jsonfile.write("[ \n\n")


        #json.dump(row_as_dict, self.current_jsonfile,indent=4)
        json.dump(row_as_dict, self.current_jsonfile,indent=4, ensure_ascii=False)
        self.current_jsonfile.write(",")
        self._number_of_inserts_in_the_current_file += 1
        return True





    def _get_new_file(self, path_to_dir, fname, file_extention, encoding="utf-8", file_flag="w", open_file_with_codecs=False):
        if file_extention not in Exporter.supported_file_formats:
            self.logger.error("NewFileGetterError: Given file_format '{}' is not supported. Please use one of the following file formats: '{}'. ".format(file_extention,Exporter.supported_file_formats ), exc_info=self._logger_traceback)
            sys.exit()

        count_of_existing_files = self._numbers_of_alredy_created_files[path_to_dir][fname]
        new_fname_without_extention = fname+ "_{}".format(count_of_existing_files)
        new_fname_with_extention =new_fname_without_extention+ "." + file_extention
        path_to_file = os.path.join(path_to_dir, new_fname_with_extention)
        #p(count_of_existing_files, c="r")
        if count_of_existing_files ==0:
            if os.path.isfile(path_to_file):
                if self._rewrite:
                    exist_fnames_in_dir = os.listdir(path_to_dir)
                    #p(exist_fnames_in_dir )
                    for exist_fname in  exist_fnames_in_dir:
                        if fname in exist_fname:
                            #p(exist_fname)
                            os.remove(os.path.join(path_to_dir, exist_fname))
                            self.logger.debug("NewFileRewriter: '{}' File is already exist and  was removed from '{}'.  ('rewrite'-option is enabled.)".format(exist_fname, path_to_file))
                else:
                    if not self._silent_ignore:
                        self.logger.debug("NewFileGetterProblem: '{}' File is already exist in '{}'.  Please delete it before you can start extraction.".format(new_fname_with_extention, path_to_file))
                    else:
                        self.logger.debug("NewFileGetter: '{}' File is already exist in '{}' and was silent ignored.".format(new_fname_with_extention, path_to_file))
                    return False

        if open_file_with_codecs:
            current_file = codecs.open(path_to_file, 'w', encoding)
        else:
            current_file = open(path_to_file, file_flag)
        #p(current_file,  c="r")
        self._numbers_of_alredy_created_files[path_to_dir][fname] += 1
        self.logger.debug("NewFileGetter: New File  '{}' was created in '{}'.".format(new_fname_with_extention, path_to_dir))
        return current_file




    
    def _write_to_csv_files(self, row_as_dict, fieldnames, path_to_dir , fname,  rows_limit_in_file=50000, encoding="utf-8"):
        # check if current file has not more row as given rows limits
        
        if self.current_csvfile:
            if self._number_of_inserts_in_the_current_file >= rows_limit_in_file:
                self.current_csvfile.close()
                self._number_of_inserts_in_the_current_file = 0
                self.current_csvfile = self._get_new_file(path_to_dir , fname, "csv", encoding=encoding)
                if not self.current_csvfile:
                    return False
                #p((self.current_csvfile, fieldnames))
                #self.current_csv_writer = csv.DictWriter(self.current_csvfile, fieldnames=fieldnames, encoding=encoding)
                self.current_csv_writer = csv.DictWriter(self.current_csvfile, fieldnames=fieldnames)
                self.current_csv_writer.writeheader()
        else:
            self.current_csvfile = self._get_new_file(path_to_dir , fname, "csv", encoding=encoding)
            if not self.current_csvfile:
                return False
            #self.current_csv_writer = csv.DictWriter(self.current_csvfile, fieldnames=fieldnames, encoding=encoding)
            self.current_csv_writer = csv.DictWriter(self.current_csvfile, fieldnames=fieldnames)
            self.current_csv_writer.writeheader()


        encoded_into_str = {}
        for k,v in row_as_dict.iteritems():
            if isinstance(k, unicode):
                k = k.encode(encoding)
            if isinstance(v, unicode):
                v = v.encode(encoding)
            encoded_into_str[k] = v
        #encoded_into_str = {k.encode(encoding): v.encode(encoding) for k,v in row_as_dict.iteritems()}
        #p(encoded_into_str)
        self.current_csv_writer.writerow(encoded_into_str)
        #self.current_csv_writer.writerow(row_as_dict)
        self._number_of_inserts_in_the_current_file += 1
        return True


    # def _write_to_json_files(self,row_as_dict, path_to_dir, fname, rows_limit_in_file=50000, encoding="utf-8",unicode_encode=True):
    #     # check if current file has not more row as given rows limits
        

    #     if self.current_jsonfile:
    #         if self._number_of_inserts_in_the_current_file >= rows_limit_in_file:
    #             self.current_jsonfile.seek(-1, os.SEEK_END)
    #             self.current_jsonfile.write("\n\n ]")
    #             self.current_jsonfile.close()
    #             self._number_of_inserts_in_the_current_file = 0
    #             self.current_jsonfile = self._get_new_file(path_to_dir , fname, "json", encoding=encoding, file_flag="a+", open_file_with_codecs=unicode_encode)
    #             if not self.current_jsonfile:
    #                 return False
    #             self.current_jsonfile.write("[ \n\n")
        
    #     else:
    #         self.current_jsonfile = self._get_new_file(path_to_dir , fname, "json", encoding=encoding, file_flag="a+", open_file_with_codecs=unicode_encode)
    #         if not self.current_jsonfile:
    #             return False
    #         self.current_jsonfile.write("[ \n\n")


    #     #json.dump(row_as_dict, self.current_jsonfile,indent=4)
    #     json.dump(row_as_dict, self.current_jsonfile,indent=4, ensure_ascii=False)
    #     self.current_jsonfile.write(",")
    #     self._number_of_inserts_in_the_current_file += 1


    def _write_row_to_xml(self,root_elem, row_as_dict, row_elem_name="Doc"):
        try:
            row_element = ET.SubElement(root_elem, row_elem_name)
            for col_name, value in row_as_dict.iteritems():
                # if "324114" in str(value):
                #     p((repr(value),col_name), c="r")
                tag = ET.SubElement(row_element, col_name)
                tag.text = unicode(value)
        except Exception as e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("WriterRowIntoXMLError: Following Exception was throw: '{}'. ".format(repr(e)), exc_info=self._logger_traceback)
            return False

        return True


    def _save_output_into_current_xml_file(self):
        if self.current_xmlfile:
            tree = ET.ElementTree(self.current_xml_root_elem)
            output_xml = ET.tostring(tree, pretty_print=True, xml_declaration=True,  encoding="utf-8")
            #p(output_xml)
            self.current_xmlfile.write(output_xml)
            self.current_xmlfile.close()
            self.current_xmlfile = False
        else:
            self.logger.error("SaveOutputIntoXMLError: There is not activ XML-Files", exc_info=self._logger_traceback)
            return False
        return True


    def _write_to_xml_files(self,row_as_dict, path_to_dir, fname, rows_limit_in_file=50000, encoding="utf-8", root_elem_name="Docs", row_elem_name="Doc"):
        # check if current file has not more row as given rows limits
        #p(self.current_xmlfile)
        if self.current_xmlfile:
            if self._number_of_inserts_in_the_current_file >= rows_limit_in_file:
                self._save_output_into_current_xml_file()
                self._number_of_inserts_in_the_current_file = 0
                self.current_xmlfile = self._get_new_file(path_to_dir , fname, "xml", encoding=encoding)
                if not self.current_xmlfile:
                    return False
        
                self.current_xml_root_elem = ET.Element(root_elem_name)

        else:
            self.current_xmlfile = self._get_new_file(path_to_dir , fname, "xml", encoding=encoding)
            if not self.current_xmlfile:
                return False
            self.current_xml_root_elem = ET.Element(root_elem_name)

        self._write_row_to_xml(self.current_xml_root_elem, row_as_dict,row_elem_name=row_elem_name)
        #self.current_xml_root_elem.writerow(row_as_dict)
        self._number_of_inserts_in_the_current_file += 1
        return True




    def _write_to_sqliteDB(self,row_as_dict, path_to_export_dir, tablename,  encoding="utf-8"):
        if not self.sqlite_db:
            self.logger.error("SQLITEWriterError: No Active DB to write in exist! Please Initialize first an Empty DB.", exc_info=self._logger_traceback)
            sys.exit()

        # col=[]
        # val=[]

        # for k, v in row_as_dict.iteritems():
        #     col.append(k)
        #     val.append(v)

        self.sqlite_db.lazyinsert(tablename,  row_as_dict)
        return True



    def _create_list_with_columns_and_types_for_sqlite(self, fieldnames):
        outputlist = []
        if isinstance(fieldnames, list):
            for colname in fieldnames:
                outputlist.append((colname,"TEXT"))
            return outputlist
        else:
            self.logger.error("SQLITECreaterError: Given Fieldnames are not from List Type.", exc_info=self._logger_traceback)
            return False




    def _eval_input_data(self):
        #p((isinstance(self._inpdata, list), isinstance(self._inpdata, types.GeneratorType)))

        check = (isinstance(self._inpdata, list), isinstance(self._inpdata, LenGen))

        if True not in check:
            self.logger.error("InputValidationError: Given 'inpdata' is not iterable. ", exc_info=self._logger_traceback)
            return False


        return True







