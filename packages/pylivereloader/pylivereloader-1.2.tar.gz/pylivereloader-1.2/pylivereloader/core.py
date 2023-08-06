#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    LiveReloader implementation script
"""

import os #Importing os for file stats
import importlib #Importing the importlib to dynamic imports
import time #Importing time for time operations

__all__ = ['LiveReloader']

class LiveReloaderScriptNotFound (Exception) :
    """Exception raised for a script not found by the LiveReloader

            Attributes:
                script -- the name of the script causing the error
                message -- explanation of the error
    """

    def __init__ (self,
                      script,
                      message = "Can't find script named -> ") : #Initialization of the class
        """Init the LiveReloaderScriptNotFound with the script and message attributes"""

        self.script = script #The script causing the error
        self.message = message #The message showed for the error

        super().__init__(self.script,
                             self.message) #Reinit the exception with the message

    def __str__ (self) : #Showed on raise
        return f"{self.message}{self.script}" #Return the message error

class LiveReloaderCallbackNotAFunction (Exception) :
    """Exception raised for an unknow callback passed

            Attributes:
                callback_type -- the type of callback passed
                message -- explanation of the error
    """

    def __init__ (self,
                      callback_type,
                      message = "Callback type passed not a function or a class -> ") : #Initialization of the class
        """Init the LiveReloaderCallbackNotAFunction with the callback_type and message attributes"""

        self.callback_type = callback_type #The script causing the error
        self.message = message #The message showed for the error

        super().__init__(self.callback_type,
                             self.message) #Reinit the exception with the message

    def __str__ (self) : #Showed on raise
        return f"{self.message}{self.callback_type}" #Return the message error

class LiveReloader : #Class creating a live script reloader
    """LiveReloader class stands for maintaining a given script live

            Attributes:
                __script_name (str): the script name to keep live passed on __init__
                __safe_reload (bool): if the script need to be reloaded safely
                __logging (bool): print on script reloading
                __watching (bool): if the script is currently maintained live
                __last_file_time (int): unix time containing the last modification time of the script

            Methods:
                reload (on_reload_callback):
                    function reloading the class script, on_reload_callback is called after the completion of the reload
                stop ():
                    stop the live script reload
                keep_live (on_reload_callback):
                    running loop verifying if the last imported script is the live one or if it's need to be reloaded

            Exceptions:
                LiveReloaderScriptNotFound: exception raised when the script passed cannot be found
                LiveReloaderCallbackNotAFunction: exception raised for an unknow type of on_reload_callback passed


    """

    def __init__ (self,
                    script_name,
                    safe_reload = True,
                    logging = True) : #Initialization of the class
        """Initialization of the LiveReloader class with the script_name attribute"""

        self.__script_name = script_name #Script to restart when modified
        self.__safe_reload = safe_reload #If the reload is protected
        self.__logging = logging #Log on script reload

        self.__watching = True #If the reloader keep watching the script
        self.__last_file_time = None #The last modification time of the script

    def __do_reload (self,
                         on_reload_callback) :
        """Init the script reloading with the callback passed"""

        if self.__safe_reload : #If the script is safelly reloaded
            try : #Try to call the callback
                self.reload(on_reload_callback) #Reload the script
            except Exception as error : #If an exception occured
                if self.__logging :
                    print(f"[{time.strftime('%H:%M:%S')}]: LiveReloader catched exception on script: \n\t\t> {error}")

    def reload (self,
                    on_reload_callback) : #Function to reload the script
        """Reload the script and call the on_reload_callback function/class when the reload is over"""

        if self.__script_name in globals() : #If the script is in the globals
            script = globals()[self.__script_name] #Get the script reference
            globals()[self.__script_name] =  importlib.reload(script) #Reload the script and set it in the globals
        else : #If the script is not in the globals
            globals()[self.__script_name] = importlib.import_module(self.__script_name) #Import the given live script

        if self.__logging : #If logging is enabled
            print(f"[{time.strftime('%H:%M:%S')}]: LiveReloader successfully reloaded script") #Log the time

        if on_reload_callback : #If a callback was passed
            on_reload_callback() #Call the callback

    def stop (self) : #Stop the live reloader
        """Stop the live reloader"""

        self.__watching = False #Set the value to continue watching the script as False

    def keep_live (self,
                       on_reload_callback = None) : #Keep the running script as the live script
        """Maintain the running script as the last modified script based on his modification time, on_reload_callback is a function called when the script reload is over"""

        if on_reload_callback : #If a callback for the reload was passed
            if not callable(on_reload_callback) : #If the on_reload_callback param passed is not a function or a class
                raise LiveReloaderCallbackNotAFunction(on_reload_callback.__class__.__name__) #Raise not a function error

        script_name = f"{self.__script_name}.py" #Get the script name with it's extension
        while self.__watching : #While the script need to be watched
            try : #Try to get the last modification time of the file
                current_file_time = os.path.getmtime(script_name) #Get the last modification time of the script
            except : #If except == os error == file not found
                raise LiveReloaderScriptNotFound(script_name) from None #Raise the script not found error

            if self.__last_file_time == None : #If the script was not initialized
                self.__do_reload(on_reload_callback) #Reload the script == load it for the first time
                self.__last_file_time = current_file_time #Set the new modification time as the current
            elif current_file_time != self.__last_file_time : #If the script was modified
                self.__do_reload(on_reload_callback) #Reload the script
                self.__last_file_time = current_file_time #Set the new modification time as the current
