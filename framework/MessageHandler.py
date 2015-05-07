'''
Created on Apr 20, 2015

@author: talbpaul
'''
#for future compatibility with Python 3--------------------------------------------------------------
from __future__ import division, print_function, unicode_literals, absolute_import
import warnings
warnings.simplefilter('default',DeprecationWarning)
if not 'xrange' in dir(__builtins__):
  xrange = range
#End compatibility block for Python 3----------------------------------------------------------------

#External Modules------------------------------------------------------------------------------------
import platform
import os
#External Modules End--------------------------------------------------------------------------------

#Internal Modules------------------------------------------------------------------------------------
import utils
#Internal Modules End--------------------------------------------------------------------------------

# set a global variable for backend default setting
if platform.system() == 'Windows': disAvail = True
else:
  if os.getenv('DISPLAY'): disAvail = True
  else:                    disAvail = False

class MessageUser(object):
  '''
    Inheriting from this class grants access to methods used by the message handler.
  '''
  def raiseAnError(self,etype,message,tag='ERROR',verbosity='silent'):
    self.messageHandler.error(self,etype,str(message),str(tag),verbosity)

  def raiseAWarning(self,message,tag='Warning',verbosity='quiet'):
    self.messageHandler.message(self,str(message),str(tag),verbosity)

  def raiseAMessage(self,message,tag='Message',verbosity='all'):
    self.messageHandler.message(self,str(message),str(tag),verbosity)

  def raiseADebug(self,message,tag='DEBUG',verbosity='debug'):
    self.messageHandler.message(self,str(message),str(tag),verbosity)

  def getLocalVerbosity(self,default=None):
    try: return self.verbosity
    except AttributeError: return default


class MessageHandler(MessageUser):
  """
  Class for handling messages, warnings, and errors in RAVEN.  One instance of this
  class should be created at the start of the Simulation and propagated through
  the readMoreXML function of the BaseClass.  The utils handlers for raiseAMessage,
  raiseAWarning, raiseAnError, and raiseDebug will access this handler.
  """
  def __init__(self):
    '''
      Init of class
      @In, None
      @Out, None
    '''
    self.printTag     = 'MESSAGE HANDLER'
    self.verbosity    = 'all'
    self.suppressErrs = False
    self.verbCode     = {'silent':0, 'quiet':1, 'all':2, 'debug':3}

  def initialize(self,initDict):
    self.verbosity     = initDict['verbosity'   ] if 'verbosity'    in initDict.keys() else 'all'
    self.callerLength  = initDict['callerLength'] if 'callerLength' in initDict.keys() else 25
    self.tagLength     = initDict['tagLength'   ] if 'tagLength'    in initDict.keys() else 15
    self.suppressErrs  = initDict['suppressErrs'] in utils.stringsThatMeanTrue() if 'suppressErrs' in initDict.keys() else False

  def getStringFromCaller(self,obj):
    if type(obj) in [str,unicode]: return obj
    try: obj.printTag
    except AttributeError: tag = str(obj)
    else: tag = str(obj.printTag)
    return tag

  def getDesiredVerbosity(self,caller):
    localVerb = caller.getLocalVerbosity(default=self.verbosity)
    if localVerb == None: localVerb = self.verbosity
    return self.checkVerbosity(localVerb) #self.verbCode[str(localVerb).strip().lower()]

  def checkVerbosity(self,verb):
    if str(verb).strip().lower() not in self.verbCode.keys():
      raise IOError('Verbosity key '+str(verb)+' not recognized!  Options are '+str(self.verbCode.keys()+[None]),'ERROR','silent')
    return self.verbCode[str(verb).strip().lower()]

  def error(self,caller,etype,message,tag='ERROR',verbosity='silent'):
    verbval = self.checkVerbosity(verbosity)
    okay,msg = self._printMessage(caller,message,tag,verbval)
    if okay:
      if not self.suppressErrs: raise etype(msg)
      else: print(msg)

  def message(self,caller,message,tag,verbosity):
    verbval = self.checkVerbosity(verbosity)
    okay,msg = self._printMessage(caller,message,tag,verbval)
    if okay: print(msg)

  def _printMessage(self,caller,message,tag,verbval):
    #allows raising standardized messages
    shouldIPrint = False
    desired = self.getDesiredVerbosity(caller)
    if verbval <= desired: shouldIPrint=True
    if not shouldIPrint: return False,''
    ctag = self.getStringFromCaller(caller)
    msg=self.stdMessage(ctag,tag,message)
    return shouldIPrint,msg

  def stdMessage(self,pre,tag,post):
    msg = ''
    msg+=pre.ljust(self.callerLength)[0:self.callerLength] + ': '
    msg+=tag.ljust(self.tagLength)[0:self.tagLength]+' -> '
    msg+=post
    return msg
