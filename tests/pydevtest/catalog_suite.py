import unittest
from resource_suite import ResourceBase
from pydevtest_common import assertiCmd, assertiCmdFail, interruptiCmd
import pydevtest_sessions as s
import commands
import os
import shlex
import datetime
import time

class Test_CatalogSuite(ResourceBase):

    def setUp(self):
        s.twousers_up()
        self.run_resource_setup()

    def tearDown(self):
        self.run_resource_teardown()
        s.twousers_down()

    ###################
    # icd
    ###################

    def test_empty_icd(self):
        # assertions
        assertiCmd(s.adminsession,"ils -L", "LIST","test") # whatever
        assertiCmd(s.adminsession,"icd "+self.testdir) # get into subdir
        assertiCmd(s.adminsession,"icd") # just go home
        assertiCmd(s.adminsession,"ils","LIST","/"+s.adminsession.getZoneName()+"/home/"+s.adminsession.getUserName()+":") # listing

    def test_empty_icd_verbose(self):
        # assertions
        assertiCmd(s.adminsession,"icd "+self.testdir) # get into subdir
        assertiCmd(s.adminsession,"icd -v","LIST","Deleting (if it exists) session envFile:") # home, verbose
        assertiCmd(s.adminsession,"ils","LIST","/"+s.adminsession.getZoneName()+"/home/"+s.adminsession.getUserName()+":") # listing

    def test_icd_to_subdir(self):
        # assertions
        assertiCmd(s.adminsession,"icd "+self.testdir) # get into subdir
        assertiCmd(s.adminsession,"ils","LIST","/"+s.adminsession.getZoneName()+"/home/"+s.adminsession.getUserName()+"/"+s.adminsession.sessionId+"/"+self.testdir+":") # listing

    def test_icd_to_parentdir(self):
        # assertions
        assertiCmd(s.adminsession,"icd ..") # go to parent
        assertiCmd(s.adminsession,"ils","LIST","/"+s.adminsession.getZoneName()+"/home/"+s.adminsession.getUserName()+":") # listing

    def test_icd_to_root(self):
        # assertions
        assertiCmd(s.adminsession,"icd /") # go to root
        assertiCmd(s.adminsession,"ils","LIST","/:") # listing

    def test_icd_to_root_with_badpath(self):
        # assertions
        assertiCmd(s.adminsession,"icd /doesnotexist","LIST","No such directory (collection):") # go to root with bad path

    ###################
    # iexit
    ###################

    def test_iexit(self):
        # assertions
        assertiCmd(s.adminsession,"iexit") # just go home

    def test_iexit_verbose(self):
        # assertions
        assertiCmd(s.adminsession,"iexit -v","LIST","Deleting (if it exists) session envFile:") # home, verbose

    def test_iexit_with_bad_option(self):
        # assertions
        assertiCmdFail(s.adminsession,"iexit -z") # run iexit with bad option

    def test_iexit_with_bad_parameter(self):
        # assertions
        assertiCmdFail(s.adminsession,"iexit badparameter") # run iexit with bad parameter

    ###################
    # ihelp
    ###################

    def test_local_ihelp(self):
        # assertions
        assertiCmd(s.adminsession,"ihelp","LIST","The following is a list of the icommands") # run ihelp

    def test_local_ihelp_with_help(self):
        # assertions
        assertiCmd(s.adminsession,"ihelp -h","LIST","Display i-commands synopsis") # run ihelp with help

    def test_local_ihelp_all(self):
        # assertions
        assertiCmd(s.adminsession,"ihelp -a","LIST","Usage") # run ihelp on all icommands

    def test_local_ihelp_with_good_icommand(self):
        # assertions
        assertiCmd(s.adminsession,"ihelp ils","LIST","Usage") # run ihelp with good icommand

    def test_local_ihelp_with_bad_icommand(self):
        # assertions
        assertiCmdFail(s.adminsession,"ihelp idoesnotexist") # run ihelp with bad icommand

    def test_local_ihelp_with_bad_option(self):
        # assertions
        assertiCmdFail(s.adminsession,"ihelp -z") # run ihelp with bad option

    ###################
    # imkdir
    ###################

    def test_local_imkdir(self):
        # local setup
        mytestdir = "testingimkdir"
        # assertions
        assertiCmdFail(s.adminsession,"ils -L "+mytestdir,"LIST",mytestdir) # should not be listed
        assertiCmd(s.adminsession,"imkdir "+mytestdir) # imkdir
        assertiCmd(s.adminsession,"ils -L "+mytestdir,"LIST",mytestdir) # should be listed

    def test_local_imkdir_with_trailing_slash(self):
        # local setup
        mytestdir = "testingimkdirwithslash"
        # assertions
        assertiCmdFail(s.adminsession,"ils -L "+mytestdir+"/","LIST",mytestdir) # should not be listed
        assertiCmd(s.adminsession,"imkdir "+mytestdir+"/") # imkdir
        assertiCmd(s.adminsession,"ils -L "+mytestdir,"LIST",mytestdir) # should be listed

    def test_local_imkdir_with_trailing_slash_already_exists(self):
        # local setup
        mytestdir = "testingimkdirwithslash"
        # assertions
        assertiCmd(s.adminsession,"imkdir "+mytestdir+"/") # imkdir
        assertiCmdFail(s.adminsession,"imkdir "+mytestdir) # should fail, already exists
        assertiCmdFail(s.adminsession,"imkdir "+mytestdir+"/") # should fail, already exists

    def test_local_imkdir_when_dir_already_exists(self):
        # local setup
        mytestdir = "testingimkdiralreadyexists"
        # assertions
        assertiCmd(s.adminsession,"imkdir "+mytestdir) # imkdir
        assertiCmdFail(s.adminsession,"imkdir "+mytestdir) # should fail, already exists

    def test_local_imkdir_when_file_already_exists(self):
        # local setup
        # assertions
        assertiCmdFail(s.adminsession,"imkdir "+self.testfile) # should fail, filename already exists

    def test_local_imkdir_with_parent(self):
        # local setup
        mytestdir = "parent/testingimkdirwithparent"
        # assertions
        assertiCmdFail(s.adminsession,"ils -L "+mytestdir,"LIST",mytestdir) # should not be listed
        assertiCmd(s.adminsession,"imkdir -p "+mytestdir) # imkdir with parent
        assertiCmd(s.adminsession,"ils -L "+mytestdir,"LIST",mytestdir) # should be listed

    def test_local_imkdir_with_bad_option(self):
        # assertions
        assertiCmdFail(s.adminsession,"imkdir -z") # run imkdir with bad option

    ###################
    # iquest
    ###################

    def test_iquest_totaldatasize(self):
        assertiCmd(s.adminsession,"iquest \"select sum(DATA_SIZE) where COLL_NAME like '/tempZone/home/%'\"","LIST","DATA_SIZE") # selects total data size

    def test_iquest_bad_format(self):
        assertiCmd(s.adminsession,"iquest \"bad formatting\"","ERROR","INPUT_ARG_NOT_WELL_FORMED_ERR") # bad request



