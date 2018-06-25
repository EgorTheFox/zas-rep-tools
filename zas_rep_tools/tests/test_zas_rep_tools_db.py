#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# : Tests for XXX Module
# Author:
# c(Developer) ->     {'Egor Savin'}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

###Programm Info######
#
#
#
#
#

import unittest
import os
import logging


import codecs
import sure
import inspect
import copy
from collections import defaultdict
from nose.plugins.attrib import attr
from testfixtures import tempdir, TempDirectory
from distutils.dir_util import copy_tree 
import glob

from zas_rep_tools.src.classes.DB import DB

from zas_rep_tools.src.utils.debugger import p, wipd, wipdn, wipdl, wipdo
from zas_rep_tools.src.utils.logger import Logger





class TestZAScorpusDBDB(unittest.TestCase):
    def setUp(self):



        ######## Folders Creation ##############
        ########### Begin ######################
        abs_path_to_zas_rep_tools = os.path.dirname(os.path.dirname(os.path.dirname(inspect.getfile(DB))))
        #p(abs_path_to_zas_rep_tools)
        relativ_path_to_test_prjFolder = "data/tests_data/testDBs/prjFolder"
        self.abs_path_to_test_prjFolder = os.path.join(abs_path_to_zas_rep_tools,relativ_path_to_test_prjFolder)
        relativ_path_to_test_testFolder = "data/tests_data/testDBs/testFolder"
        self.abs_path_to_test_testFolder = os.path.join(abs_path_to_zas_rep_tools,relativ_path_to_test_testFolder)


        relativ_path_to_test_corpus = "data/tests_data/testDBs/test/corpus.db"
        relativ_path_to_test_stats = "data/tests_data/testDBs/test/stats.db"
        self.abs_path_to_test_corpus = os.path.join(abs_path_to_zas_rep_tools,relativ_path_to_test_corpus)
        self.abs_path_to_test_stats = os.path.join(abs_path_to_zas_rep_tools,relativ_path_to_test_stats)


        self.tempdir = TempDirectory()
        self.tempdir.makedir('PrjFolder')
        self.tempdir.makedir('TestFolder')
        self.path_to_temp_prjFolder  = self.tempdir.getpath('PrjFolder')
        self.path_to_temp_testFolder  = self.tempdir.getpath('TestFolder')
        copy_tree(self.abs_path_to_test_prjFolder,self.path_to_temp_prjFolder )
        copy_tree(self.abs_path_to_test_testFolder,self.path_to_temp_testFolder )

        self.path_to_temp_test_corpus = os.path.join(self.path_to_temp_testFolder, "corpus.db")
        self.path_to_temp_test_stats = os.path.join(self.path_to_temp_testFolder, "stats.db")
        self.path_to_temp_test_fakeDB = os.path.join(self.path_to_temp_testFolder, "fakeDB.db")
        ######## Folders Creation ##############
        ########### End #####################
        



    def tearDown(self):
        self.tempdir.cleanup()
        print ">>>TempDirectory was cleaned<<<"


####################################################################################################
####################################################################################################
###################### START STABLE TESTS #########################################################
####################################################################################################
####################################################################################################


###################INITIALISATION:000############################################



    # ###### xxx: 000 ######
    # #@attr(status='stable')True
    # #@wipd
    # def test_initialisation_000(self):
    #     db = DB( developingMode = True)
    #     #db = DB()
    #     #db.init_corpus(self.path_to_temp_prjFolder, "twitter_streamed_de", "de", "twitter", "intern")
    #     #db.init_corpus(self.abs_path_to_test_prjFolder, "twitter_streamed_de", "de", "twitter", "intern")
    #     #p(db.rowsNumber("info"))
    #     # p(db.tables())
    #     # p(db.tableColumns("info"))
    #     #p(db.tableColumnsTypes("info"))
    #     #p(db.tableColumns("info"))
    #     #p(db.get_attribut(u"visibility"))
    #     # p(db.rowsNumber("info"))

        
    #     #db = DB( )
    #     db = DB( developingMode = True)
    #     db.init_stats(self.path_to_temp_prjFolder,  "twitter_streamed", "de", "intern","twrd")
    #     #db.init_stats(self.abs_path_to_test_prjFolder,  "twitter_streamed", "de", "intern","twrd")
    #     #p(db.tables())
    #     #p(db.tableColumns("info"))
    #     #p(db.get_all_attributs())
    #     #db.update_attribut("version","7")
    #     #p(db.get_all_attributs())


 
    @wipd
    def test_initialisation_corpus_001(self):
        db = DB(developingMode = True)
        #db = DB()
        #p(self.path_to_temp_test_corpus)
        
        #db.connect(self.path_to_temp_test_corpus)
        #p(db.tables())
        #p(db.tables())
        #db.connect(self.path_to_temp_test_fakeDB)
        db.init_corpus(self.path_to_temp_testFolder, "twitter_streamed", "de", "intern", "twitter" )
        #db.init_corpus(self.path_to_temp_prjFolder, "twitter_streamed", "de", "intern", "twitter", template_name="twitter")
        #db.init_corpus(self.path_to_temp_prjFolder, "twitter_streamed_de",
        #    "de", "intern", "twitter",
        #    template_name="twitter",
        #    additional_columns_with_types_for_documents=[("kaka","TEXT"), ("koko","BLOB")])
        #additional_columns_with_types
        db.attach(self.path_to_temp_test_stats)
        # p(db.tables("stats"))
        #p(db.tables())
        # p(db.tableColumns("documents"))
        # # p(db.get_all_attributs(), c="m")
        # # p(db.tableColumns("documents"), c="r")
        # db.insertCV("documents", [u'docs_id', u'text'], ["1","h😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀jk"])
        # # db.insert_row("documents", [u'docs_id', u'text'], ["2","hjk"])
        # # db.insert_row("documents", [u'docs_id', u'text'], ["3","hj😀😀😀😀😀😀k"])
        # # db.insert_row("documents", [u'docs_id', u'text'], ["4","h😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀jk"])
        # #db.insert_values("documents", [None,"ghj"])
        # #db.insert_values("documents", [None,"ghj"])
        # p(db.rowsNumber("documents"))
        p(db.rowsNumber("documents"))
        db.lazy_writer("documents", "cv", [ u'text'], ["h😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀jk"])
        db.lazy_writer("documents", "v", values= [None,"h😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀jk"])
        db.lazy_writer("documents", "v", values= [None,"h😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀jk"])
        db.lazy_writer("documents", "v", values= [None,"h😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀jk"])
        p(db.rowsNumber("documents"))
        #db.commit()
        db.rollback()
        p(db.rowsNumber("documents"))

        db.encrypte("new")
        # #db.lazy_writer("documents", "v", values= ["hjk","h😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀jk"])
        
        # #db.update("documents", ["text"], ["xxx"], "docs_id=3")
        # #db.commit()
        
        # # p(db.lazy_getter("documents", size_to_get=6))

        # # for item in db.lazy_getter("documents"):
        # #     p(item)


        # # for item in db.getlimit(3,"documents"):
        # #     p(item)

        # # #db.drop_table("info", "stats")
        # # p(db.tables(,"stats"))
        # # p(db.tables("stats"))
        # # p(db.rowsNumber("info"))
        # # p(db.rowsNumber("info", "stats"))
        # # p(db.tableColumnsTypes("info"))
        # # p(db.tableColumnsTypes("info", "stats"))
        # # p(db.tableColumns("info"))
        # # p(db.tableColumns("info","stats"))
        # # p(db.path("main"))
        # # p(db.fname("stats"))
        # # p(db.fname())
        # # p(db.path())
        # # p(db.attachedDBs())
        # # p(db.attachedDBs())
        # # p(db.fnameAttachedDBs())
        # # p(db.pathAttachedDBs())
        # # p(db.dbsNames())




    # #@wipd
    # def test_initialisation_stats_001(self):
    #     db = DB( developingMode = True)
    #     #p(db.tables())
    #     db.init_stats(self.path_to_temp_prjFolder, "fghj", "twitter_streamed", "intern", "de")
    #     p(db.get_all_attributs(), c="m")
    #     p(db.tableColumns("baseline"), c="r")
    #     p(db.tableColumns("reduplications"), c="r")
    #     db.commit()





#################################Beginn##############################################
############################INTERN METHODS###########################################
#####################################################################################

###################    :100############################################ 

    ###### ***** ######

    #@attr(status='stable')
    #@wipd
    #def test_XXX_name_100(self):
    ##self.logger_initialisation()
    #   pass

    ###### ***** ######


    ###### ***** ######






#################################END#################################################
############################INTERN METHODS###########################################
#####################################################################################








#################################Beginn##############################################
############################EXTERN METHODS###########################################
#####################################################################################


###################    :500############################################ 
    ###### ***** ######
   

   



#################################END##################################################
############################EXTERN METHODS############################################
######################################################################################





####################################################################################################
####################################################################################################
###################### STOP STABLE TESTS #########################################################
####################################################################################################
####################################################################################################


























####################################################################################################
####################################################################################################
###################### START WORK_IN_PROGRESS (wipd) TESTS #########################################
####################################################################################################
####################################################################################################


    # #@attr(status='stable')True
    # @oldwipd
    # def test_025(self):
    #     additional_dbs = [

    #             "/Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/data/DB/testDBs/additionalDBs/bloggerDB.db", 
    #             "/Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/data/DB/testDBs/additionalDBs/twitterDB.db",
    #             "/Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/data/DB/testDBs/additionalDBs/facebookDB.db",
    #             "/Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/data/DB/testDBs/additionalDBs/fakeDB.db",
    #             ]

    #     #database = DB("/Users/egoruni/Desktop/BA/Code/test/PrjData", developingMode = True)
    #     database = DB("/Users/egoruni/Desktop/BA/Code/test/PrjData", additional_DBs=additional_dbs,  developingMode = True)
    #     #database.del_mainDB()
    #     database.create_project("twitter", "/Users/egoruni/Desktop/BA/Code/test/PrjData")
    #     database.create_project("blogger", "/Users/egoruni/Desktop/BA/Code/test/PrjData")
    #     database.create_project("facebook", "/Users/egoruni/Desktop/BA/Code/test/PrjData",
    #             documents_columns={
    #                 "age":"INTEGER",
    #                 "gender":"TEXT",
    #                 "post_data":"TEXT",
    #             })
    #     # p(database.get_attached_dbs("paths"), c="m")
    #     # p(database.get_attached_dbs("names"), c="m")
    #     # p(database.tables("main"), c="r")
    #     # p(database.tables("twitter"), c="r")
    #     # p(database.tables("blogger"), c="r")
    #     # #p(database.get_tableInfo("Projects"), c="r")
    #     # #p(database.get_tableInfo("Corpora", "blogger"), c="r") 
    #     # #p(database.get_fk("Corpora", "blogger"), c="r")
    #     # #p(database.get_ix_list("Corpora", "blogger"), c="r")
    #     # #p(database.get_ix_info("ix_corpora_template_corpus", "blogger"), c="r")
    #     # p(database._get_all_prjDBs_paths(), c="m")
        

    #     database._attach_all_existing_prjDBs()
    #     # p(database.get_tableInfo("Projects"), c="r")
    #     # p(database.supported_projects())
    #     # p(database.supported_projects_with_ids())
    #     # database.add_language_into_mainDB("german", "de")
    #     # database.add_language_into_mainDB("english", "en")
    #     # p(database.supported_lang())
    #     # p(database.supported_lang_with_ids())
    # ##### throws_exceptions:050  ######











####################################################################################################
####################################################################################################
###################### STOP WORK_IN_PROGRESS (wipd) TESTS #########################################
####################################################################################################
####################################################################################################







