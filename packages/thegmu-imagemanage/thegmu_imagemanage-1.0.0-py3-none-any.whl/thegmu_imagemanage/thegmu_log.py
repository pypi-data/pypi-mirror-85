#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    thegmu_log.py
    ~~~~~~~~~~~~~

    Standard Python Logging extension.

    #. Interleave dependent package messages using a unique
       three letter acronym name.
    #. Configure logging to taste.
    #. Default configuration resolves all method names to four characters.
       this prevents wavy indent where 'warning' being 6 characters and 'debug'
       is five and 'info' is 4.
    #. If you prefer the standard Python logging names then just
       create a context as such and pass that in.
    #. GLOBAL class variables are used because the logging module is global state.

"""

import copy
import importlib
import inspect
import logging
import pprint
import os
import sys
import time
import yaml


class TheGMULogException(Exception):
    """TheGMULog class exception."""


class TheGMULog():
    """
    TheGMULog builds on Python logging which is a
    quasi singleton design pattern with context switching.
    YAML configuration is provided.
    """

    CLITLA = 'cli'
    LOG_FRAME_DEPTH = 2
    DEFAULT_CONTEXT_YAML = r'''
context: null
default_context: null
default_level: PROGRESS
default_level_environment_variable: GMUPYLOGLEVEL
message_format: '[%(asctime)s] %(name)s.%(levelname)s.%(message)s'
date_format: '%m/%d/%Y %H:%M:%S'
level:
  DEBUG:
    method: debu
    order: 10
  TEMP:
    method: temp
    order: 15
  TEST:
    method: test
    order: 20
  PROGRESS:
    method: prog
    order: 30
  WARNING:
    method: warn
    order: 40
  CRITICAL:
    method: crit
    order: 50
level_name_level: null
level_name: null
log_formatter: null
method_name: null
method_name_level_name: null
tla: cli
timestamp: null
    '''

    STDOUT_STREAMHANDLER = logging.StreamHandler(sys.__stdout__)
    CURRENT_CONTEXT = {}
    TLA_CONTEXT = {}

    def __init__(self, tla=None, context=None):
        """
        :param tla:
             An package wide designator for you application as a three letter acronym.
             Pass this in to override the CLI package tla of 'cli'.
             All log messages will start with this tla as a log name space.

        :param context:
             Pass a Python dictionary to override the default context above: DEFAULT_CONTEXT_YAML.
             Use the 'get_default_context_copy()' to get a dictionary and
             then override the defaults.
        """
        if (tla is None):
            tla = TheGMULog.CLITLA

        assert(len(tla) == 3)

        self.context = None
        self.tla = tla
        self._init_class_attrs()

        self.logger = logging.getLogger(self.tla)

        self.context_switch(context)
        self.log_method_name = None

    def __getattr__(self, attrname):
        """Fake inheritance by first checking our object and then
        delegating to the logger module itself.
        """
        if (attrname in self.context['method_name_level_name']):
            self.context['method_name'] = attrname
            return getattr(self, 'log_by_level_name')
        if (attrname in ('debug', 'info', 'critical', 'warning', 'error')):
            raise AttributeError(
                "'Logger' object has no attribute '%s'" %
                attrname)
        if (attrname in self.context):
            return self.context[attrname]
        return getattr(self.logger, attrname)

    @classmethod
    def _init_class_attrs(cls):
        """Initialize any global class attributes."""
        if (not cls.STDOUT_STREAMHANDLER):
            cls.STDOUT_STREAMHANDLER = logging.StreamHandler(
                sys.__stdout__)
        if (not cls.TLA_CONTEXT):
            cls.TLA_CONTEXT = {}

    def _init_tla_context(self, context):

        default_context = TheGMULog.get_default_context_copy()
        if (context is None):
            context = default_context

        """Set the default logging level from the shell environment if available."""
        default_level_name = os.getenv(
            context['default_level_environment_variable'], '')

        if default_level_name:
            if (default_level_name not in context['level']):
                raise (
                    TheGMULogException(
                        "'%s=%s', unrecognized log level, valid levels are: %s%s" %
                        (context['default_level_environment_variable'],
                         default_level_name,
                         os.linesep,
                         pprint.pformat(
                             context['level']))))
        else:
            default_level_name = context['default_level']

        context['level_name'] = default_level_name
        context['method_name'] = context['level'][default_level_name]['method']

        """Map the method name such as 'debu' to the method's integer level, i.e. 'debu' => 10"""
        context['method_name_level_name'] = dict(
            (context['level'][x]['method'], x) for x in context['level'])
        context['level_name_level'] = dict(
            (x, context['level'][x]['order']) for x in context['level'])
        context['log_formatter'] = logging.Formatter(
            context['message_format'], datefmt=context['date_format'])
        context['timestmap'] = int(time.time())

        TheGMULog.TLA_CONTEXT[self.tla] = context

    def context_check(self, context):
        """Validate the state of the context passed in."""
        if (context is None):
            return

        if (not isinstance(context, (dict,))):
            raise TheGMULogException(
                "%s.context expected Python dictionary: possible YAML string detected, use yaml.load." %
                (self.__class__.__name__))
        default_context = self.get_default_context_copy()
        if (any(x for x in default_context if x not in context)):
            raise TheGMULogException(
                "Programmer error: TheGMULog passed invalid context: %s" %
                (context, ))

    def context_switch(self, context):
        """Set up the logging.

        :param context: is a Python dictionary initially copied from DEFAULT_CONTEXT_YAML.
        """

        """Check if self.tla and passed context match TheGMULog.CURRENT_CONTEXT."""
        self.context_check(context)

        if (self.is_current_context(context)):
            self.set_current_context(TheGMULog.CURRENT_CONTEXT)
            return

        if ((context is not None) or (self.tla not in TheGMULog.TLA_CONTEXT)):
            self._init_tla_context(context)

        self.set_current_context(TheGMULog.TLA_CONTEXT[self.tla])

        """addLevelName updates/overrides any existing level name."""
        for log_type in self.context['level']:
            logging.addLevelName(
                self.context['level'][log_type]['order'],
                self.context['level'][log_type]['method'])

        """
        The logger module holds global state.
        Remove all handlers that are logging.
        """
        self.remove_existing_logger_handlers()

        """Set up the new handler"""
        TheGMULog.STDOUT_STREAMHANDLER.setFormatter(
            self.context['log_formatter'])
        self.logger.addHandler(TheGMULog.STDOUT_STREAMHANDLER)

        self.logger.setLevel(
            self.context['level'][self.context['level_name']]['order'])

    def is_current_context(self, context):
        """Timestamp is checked in case the context for the tla has been updated."""
        if (not TheGMULog.CURRENT_CONTEXT):
            return False
        if (self.tla not in TheGMULog.TLA_CONTEXT):
            return False
        if (self.tla != TheGMULog.CURRENT_CONTEXT['tla']):
            return False

        tla_timestamp = TheGMULog.TLA_CONTEXT[self.tla]['timestamp']

        if ((context is not None) and ((context['timestamp'] is None) or (
                tla_timestamp != context['timestamp']))):
            return False

        if (tla_timestamp != TheGMULog.CURRENT_CONTEXT['timestamp']):
            return False

        return True

    def log_by_level_name(self, msg):
        """logging level output using a string instead of constant.

        :param msg: Typically a one line log message.

        """
        level_name = self.context['method_name_level_name'][self.context['method_name']]
        level_order = self.context['level_name_level'][level_name]
        if ((self.logger.getEffectiveLevel() is None) or (
                level_order >= self.logger.getEffectiveLevel())):
            log_frame = self.get_log_frame()
            self.log(level_order, "%s.%s %% %s" %
                     (log_frame[0], log_frame[1], msg))

    @staticmethod
    def get_default_context_copy():
        """copy.deepcopy the DEFAULT_CONTEXT_YAML."""
        return copy.deepcopy(
            yaml.load(
                TheGMULog.DEFAULT_CONTEXT_YAML,
                Loader=yaml.SafeLoader))

    def get_level_name_method_name(self, level_name):
        """Map level name string to a class method.

        :param level_name: The level name to map.
            It is an exception to pass an unconfigured level.
        """
        if (level_name in self.context['level']):
            return self.context['level'][level_name]['method']
        raise TheGMULogException("%s level not found" % (level_name, ))

    def get_level_name(self):
        """Return the current level name as string, i.e "DEBUG"."""
        return self.context['level_name']

    def get_level_name_for_method_name(self, method_name):
        """Map a method name to its level string.

        :param method_name: the name to map.
            It is an exception to pass an unregistered method_name.

        """
        if (method_name in self.context['method_name_level_name']):
            return self.context['method_name_level_name'][method_name]
        raise TheGMULogException(
            "%s unrecognized method name not found" %
            (method_name, ))

    @classmethod
    def get_log_frame(cls):
        """Stack trace log frame of current function."""

        callee_frame_list = inspect.getouterframes(inspect.currentframe())
        if len(callee_frame_list) > TheGMULog.LOG_FRAME_DEPTH:
            frame = callee_frame_list[TheGMULog.LOG_FRAME_DEPTH]
        else:
            frame = callee_frame_list.pop()
        function_name = frame[TheGMULog.LOG_FRAME_DEPTH]
        if function_name == '<module>':
            function_name = '__main__'

        log_frame = [os.path.basename(frame[1]), function_name, frame[2]]
        return log_frame

    def remove_existing_logger_handlers(self):
        """Sets up the logging Stream handler for the current TLA"""
        for tla_handler in self.logger.handlers:
            self.logger.removeHandler(tla_handler)

    @classmethod
    def remove_all_loggers(cls):
        """Update the global state in the Python package 'logging'"""
        importlib.reload(logging)

    def set_current_context(self, current_context):
        """Update the class global state with the passed on state.

        :param current_context: The new context information to copy verbatim.

        """
        TheGMULog.CURRENT_CONTEXT = current_context
        self.context = current_context

    def set_level_from_string(self, level_name):
        """Python logging uses integers, set the integer value mapped to this string.

        :param level_name: A previously configured level_name mapped to a level integer.
            It is an exception to pass an unregistered level_name.
        """
        if (level_name in self.context['level_name_level']):
            self.logger.setLevel(self.context['level_name_level'][level_name])
            self.context['level_name'] = level_name
            return
        raise TheGMULogException(
            "TheGMULog unrecognized log level: %s" %
            level_name)
