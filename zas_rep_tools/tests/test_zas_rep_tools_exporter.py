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


#import codecs
import sure
#import inspect
import copy
#from collections import defaultdict
from nose.plugins.attrib import attr
from testfixtures import tempdir, TempDirectory
from distutils.dir_util import copy_tree 
#import glob
import sys

from zas_rep_tools.src.classes.exporter import Exporter
from zas_rep_tools.src.classes.reader import Reader

from zas_rep_tools.src.classes.configer import Configer
from zas_rep_tools.src.utils.debugger import p, wipd, wipdn, wipdl, wipdo
from zas_rep_tools.src.utils.logger import *
#from zas_rep_tools.src.utils.recipes_test_db import *




class TestZAScorpusExporterExporter(unittest.TestCase):
    #_multiprocess_can_split_ = True
    _multiprocess_shared_  = True
    @classmethod 
    def setUp(self):
        #print "setup called" #called.append("setup")
        Configer(mode="test", rewrite=False).create_test_data(use_original_classes=True, corp_status_bar=True, corp_log_ignored=True,  corp_lang_classification=True)
        self.configer = Configer(mode="test")
        ######## Folders Creation ##############

        self.tempdir = TempDirectory()
        

        #####################
        #### Test DBs########
        #######Begin#########

        self.path_to_zas_rep_tools = self.configer.path_to_zas_rep_tools
        self.path_to_testdbs  =  self.configer.path_to_testdbs 
        self.db_blogger_plaintext_corp_en = self.configer.test_dbs["plaintext"]["blogger"]["en"]["corpus"]
        self.db_blogger_plaintext_corp_de = self.configer.test_dbs["plaintext"]["blogger"]["de"]["corpus"]
        self.db_blogger_plaintext_corp_test = self.configer.test_dbs["plaintext"]["blogger"]["test"]["corpus"]
        self.db_blogger_plaintext_stats_en = self.configer.test_dbs["plaintext"]["blogger"]["en"]["stats"]
        self.db_blogger_plaintext_stats_de = self.configer.test_dbs["plaintext"]["blogger"]["de"]["stats"]
        self.db_blogger_plaintext_stats_test = self.configer.test_dbs["plaintext"]["blogger"]["test"]["stats"]
          

        self.db_twitter_encrypted_corp_de = self.configer.test_dbs["encrypted"]["twitter"]["de"]["corpus"]
        self.db_twitter_encrypted_stats_de = self.configer.test_dbs["encrypted"]["twitter"]["de"]["stats"]


        ## TempDir
        self.tempdir.makedir('TestDBs')
        self.tempdir_testdbs  = self.tempdir.getpath('TestDBs')
        copy_tree(os.path.join(self.path_to_zas_rep_tools,self.path_to_testdbs ),self.tempdir_testdbs)

        #######End###########
        #### Test DBs########
        #####################



        #####################
        # Test Blogger Corpus#
        #######Begin#########

        self.path_to_test_sets_for_blogger_Corpus = "data/tests_data/Corpora/BloggerCorpus"
        
        #TXT
        self.txt_blogger_hightrepetativ_set = "txt/HighRepetativSubSet"
        self.txt_blogger_small_fake_set = "txt/SmallFakeSubset"
        #self.txt_blogger_small_sub_set = "txt/SmallSubset"

        #CSV
        self.csv_blogger_hightrepetativ_set = "csv/HighRepetativSubSet"
        self.csv_blogger_small_fake_set = "csv/SmallFakeSubset"
        # #self.csv_blogger_small_sub_set = "csv/SmallSubset"

        #XML
        self.xml_blogger_hightrepetativ_set = "xml/HighRepetativSubSet"
        self.xml_blogger_small_fake_set = "xml/SmallFakeSubset"
        #self.xml_blogger_small_sub_set = "xml/SmallSubset"

        #JSON
        self.json_blogger_hightrepetativ_set = "json/HighRepetativSubSet"
        self.json_blogger_small_fake_set = "json/SmallFakeSubset"
        # #self.json_blogger_small_sub_set = "json/SmallSubset"


        ## TempDir
        #self.path_to_test_corpora  = "data/tests_data/Corpora"
        self.tempdir.makedir('BloggerCorpus')
        self.tempdir_blogger_corp  = self.tempdir.getpath('BloggerCorpus')
        copy_tree(os.path.join(self.path_to_zas_rep_tools,self.path_to_test_sets_for_blogger_Corpus),self.tempdir_blogger_corp)

        #######End###########
        # Test Blogger Corpus#
        #####################



        #####################
        # Test Twitter Corpus#
        #######Begin#########

        self.path_to_test_sets_for_twitter_Corpus = "data/tests_data/Corpora/TwitterCorpus"
        self.json_twitter_set = "JSON/zas-rep-tool/"
        self.csv_twitter_set = "CSV/zas-rep-tool/"
        self.xml_twitter_set = "XML/zas-rep-tool/"

        ## TempDir
        #self.path_to_test_corpora  = "data/tests_data/Corpora"
        self.tempdir.makedir('TwitterCorpus')
        self.tempdir_twitter_corp  = self.tempdir.getpath('TwitterCorpus')
        copy_tree(os.path.join(self.path_to_zas_rep_tools,self.path_to_test_sets_for_twitter_Corpus),self.tempdir_twitter_corp)

        #######End###########
        # Test Twitter Corpus#
        #####################






        #####################
        #### Test Blogger ####
        #######Begin#########

        self.input_list_fake_blogger_corpus = [{'rowid':'1' ,'star_constellation': 'Capricorn', 'text': u'Well, the angel won. I went to work today....after alot of internal struggle with the facts. I calculated sick days left this year,', 'working_area': 'Consulting', 'age': '46', 'id': '324114', 'gender': 'female'}, {'rowid':'2' ,'star_constellation': 'Pisces', 'text': u"urlLink Drawing Game  It's PICTIONARY. It's very cool.", 'working_area': 'indUnk', 'age': '24', 'id': '416465', 'gender': 'male'}, {'rowid':'3' ,'star_constellation': 'Virgo', 'text': u'The mango said, "Hi there!!.... \n"Hi there!!.... \n"Hi there!!.... ', 'working_area': 'Non-Profit', 'age': '17', 'id': '322624', 'gender': 'female'}]
        self.input_list_blogger_corpus_high_repetativ_subset = [{'rowid':'1' ,'star_constellation': 'Capricorn', 'text': u'@lovelypig #direct_to_haven 67666 8997 -))) -) -P Neeeeeeeeeeeeeeeeiiiiiiinnnnn!!!!! Bitte nicht \U0001f602\U0001f602\U0001f602 \nTest Version von einem Tweeeeeeeeet=)))))))\nnoch einen Tweeeeeeeeet=))))))) \U0001f605\U0001f605', 'working_area': 'Consulting', 'age': '46', 'id': '324114', 'gender': 'female'}, {'rowid':'2' ,'star_constellation': 'Pisces', 'text': u'Einen weiteren Thread eingef\xfcgt!!! juHuuuuuuuu=) \U0001f49b\U0001f49b\U0001f49b\nden vierten Threadddddd!!! wooooowwwwww!!! \u263a\ufe0f \U0001f61c\U0001f61c\U0001f61c\nDas ist einnnneeeen Teeeeest Tweeeets, das als "extended" klassifiziert werden sollte!!! Weil es bis 280 Zeichen beinhalten sollte. \U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c Das ist einnnneeeen Teeeeest Tweeeets, das als "extended" klassifiziert werden sollte!!! Weil es bis 280 Zeichen \U0001f61c\U0001f61c\U0001f61c\U0001f61c\nDas ist einnnneeeen Teeeeest Quoted Tweet, das als "extended" klassifiziert werden sollte!!! Weil es bis 280 Zeichen beinhalten sollte. \U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c\U0001f61c Das ist einnnneeeen Teeeeest Tweeeets, das als "extended" klassifiziert werden sollte!!! Weil es bis 280 Zeichen \U0001f61c\U0001f61c h', 'working_area': 'indUnk', 'age': '24', 'id': '416465', 'gender': 'male'}, {'rowid':'3' ,'star_constellation': 'Virgo', 'text': u'Eine Teeeeeest Diskussion wird er\xf6ffnet!!! @zas-rep-tools \nEinen Test Retweet wird gepostet!!!!! Juhuuuuuu=) \U0001f600\U0001f600\U0001f600\U0001f600\nnoooooooch einen Tweeeeeeeeet=)))))))', 'working_area': 'Non-Profit', 'age': '17', 'id': '322624', 'gender': 'female'}]
        self.fieldnames = self.configer.columns_in_doc_table["blogger"] 

        #######End###########
        #### Test Blogger ####
        #####################


        #####################
        #### Test PrjFolder #
        #######Begin#########
        ## TempDir
        self.tempdir.makedir('ProjectFolder')
        self.tempdir_project_folder  = self.tempdir.getpath('ProjectFolder')

        #######End###########
       #### Test PrjFolder #
        #####################  

    @classmethod 
    def tearDown(self):
        #print "teardown called"# called.append(‘teardown’)
        self.tempdir.cleanup()




####################################################################################################
####################################################################################################
###################### START STABLE TESTS #########################################################
####################################################################################################
####################################################################################################


###################INITIALISATION:000############################################



    ###### xxx: 000 ######




    ##### xx :0== ######


    @attr(status='stable')
    #@wipd
    def test_exporter_initialisation_with_list_000(self):
        exporter = Exporter(self.input_list_fake_blogger_corpus, mode="test")
        exporter.should.be.a(Exporter)

        

    @attr(status='stable')
    #@wipd
    def test_exporter_initialisation_with_reader_obj_001(self):
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_hightrepetativ_set), "txt", regex_template="blogger", mode="test")
        exporter = Exporter(reader.getlazy(), mode="test")
        exporter.should.be.a(Exporter)


    ##### throws_exceptions:050  ######




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
   

    @attr(status='stable')
    #@wipd
    def test_export_to_csv_from_list_000(self):
        #real_fold = os.path.join(self.path_to_zas_rep_tools, "data/tests_data/Corpora/BloggerCorpus/txt")
        exporter = Exporter(self.input_list_fake_blogger_corpus, mode="test")
        #exporter = Exporter(self.input_list_fake_blogger_corpus, mode="test")
        #exporter.should.be.a(Exporter)
        exporter.tocsv(self.tempdir_project_folder, "blogger_corpus",self.fieldnames, rows_limit_in_file=1)
        #exporter.tocsv(real_fold, "blogger_corpus",self.fieldnames, rows_limit_in_file=1)

        i=0
        for item in os.listdir(self.tempdir_project_folder):
            if ".csv" in item:
                i+=1

        #p((len(self.input_list_fake_blogger_corpus), i))
        if len(self.input_list_fake_blogger_corpus) != i:
            assert False


    @attr(status='stable')
    #@wipd
    def test_export_to_csv_from_reader_001(self):
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_hightrepetativ_set), "txt", regex_template="blogger", mode="test")
        exporter = Exporter(reader.getlazy(), mode="test")

        exporter.tocsv(self.tempdir_project_folder, "blogger_corpus",self.fieldnames, rows_limit_in_file=1)

        i=0
        for item in os.listdir(self.tempdir_project_folder):
            if ".csv" in item:
                i+=1

        if len(list(reader.getlazy())) != i:
            assert False




    @attr(status='stable')
    #@wipd
    def test_export_to_xml_from_list_002(self):
        #real_fold = os.path.join(self.path_to_zas_rep_tools, "data/tests_data/Corpora/BloggerCorpus/xml")
        exporter = Exporter(self.input_list_fake_blogger_corpus, mode="test")
        #exporter = Exporter(self.input_list_fake_blogger_corpus, mode="test")

        exporter.toxml(self.tempdir_project_folder, "blogger_corpus", rows_limit_in_file=1)
        #exporter.toxml(real_fold, "blogger_corpus", rows_limit_in_file=1)

        i=0
        for item in os.listdir(self.tempdir_project_folder):
            if ".xml" in item:
                i+=1

        if len(self.input_list_fake_blogger_corpus) != i:
            assert False


    @attr(status='stable')
    #@wipd
    def test_export_to_xml_from_reader_003(self):
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_hightrepetativ_set), "txt", regex_template="blogger", mode="test")
        exporter = Exporter(reader.getlazy(), mode="test")

        exporter.toxml(self.tempdir_project_folder, "blogger_corpus", rows_limit_in_file=1)

        i=0
        for item in os.listdir(self.tempdir_project_folder):
            if ".xml" in item:
                i+=1


        if len(list(reader.getlazy())) != i:
            assert False






    @attr(status='stable')
    #@wipd
    def test_export_to_json_from_list_004(self):
        #real_fold = os.path.join(self.path_to_zas_rep_tools, "data/tests_data/Corpora/BloggerCorpus/json")
        #exporter = Exporter( , mode="dev", rewrite=True)
        exporter = Exporter(self.input_list_fake_blogger_corpus, mode="test", rewrite=True, silent_ignore = True)
        exporter.tojson(self.tempdir_project_folder, "blogger_corpus", rows_limit_in_file=1)
        #exporter.tojson(real_fold, "blogger_corpus", rows_limit_in_file=1)
        i=0
        for item in os.listdir(self.tempdir_project_folder):
            if ".json" in item:
                i+=1

        #p((len(self.input_list_fake_blogger_corpus), i, j))
        if len(self.input_list_fake_blogger_corpus) != i:
            assert False




    @attr(status='stable')
    #@wipd
    def test_export_to_json_from_reader_005(self):
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_hightrepetativ_set), "txt", regex_template="blogger", mode="test")
        exporter = Exporter(reader.getlazy(), mode="test")

        exporter.tojson(self.tempdir_project_folder, "blogger_corpus", rows_limit_in_file=1)

        i=0
        for item in os.listdir(self.tempdir_project_folder):
            if ".json" in item:
                i+=1

        #p((len(self.input_list_fake_blogger_corpus), i))
        if len(list(reader.getlazy())) != i:
            assert False





    @attr(status='stable')
    #@wipd
    def test_export_to_sqlite_from_list_006(self):
        #real_fold = os.path.join(self.path_to_zas_rep_tools, "data/tests_data/Corpora/BloggerCorpus/")
        exporter = Exporter(self.input_list_fake_blogger_corpus, mode="test")

        dbname = "blogger_corpus"
        #p(self.fieldnames)
        exporter.tosqlite(self.tempdir_project_folder, dbname, self.fieldnames)
        #exporter.tosqlite(real_fold, dbname, self.fieldnames)

 
        for item in os.listdir(self.tempdir_project_folder):
            if ".db" in item:
                if dbname not in item:
                    assert False




    @attr(status='stable')
    #@wipd
    def test_export_to_sqlite_from_reader_007(self):
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_hightrepetativ_set), "txt", regex_template="blogger", mode="test")
        exporter = Exporter(reader.getlazy(), mode="test")
        dbname = "blogger_corpus"

        exporter.tosqlite(self.tempdir_project_folder, dbname, self.fieldnames)

 
        for item in os.listdir(self.tempdir_project_folder):
            if ".db" in item:
                if dbname not in item:
                    assert False



    # #@attr(status='stable')
    # @wipd
    # def test_export_to_json_from_reader_(self):
    #     real_fold = os.path.join(self.path_to_zas_rep_tools, "data/tests_data/Corpora/BloggerCorpus/xml")
    #     reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_hightrepetativ_set), "txt", regex_template="blogger", mode="test")
    #     exporter = Exporter(reader.getlazy())

    #     exporter.tojson(real_fold, "blogger_corpus", rows_limit_in_file=100)





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











####################################################################################################
####################################################################################################
###################### STOP WORK_IN_PROGRESS (wipd) TESTS #########################################
####################################################################################################
####################################################################################################







