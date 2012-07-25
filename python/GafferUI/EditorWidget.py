##########################################################################
#  
#  Copyright (c) 2011-2012, John Haddon. All rights reserved.
#  Copyright (c) 2012, Image Engine Design Inc. All rights reserved.
#  
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#  
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#  
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#  
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  
##########################################################################

import types

import Gaffer
import GafferUI

## The EditorWidget is a base class for all Widgets which somehow display or
# manipulate a ScriptNode or its children.
class EditorWidget( GafferUI.Widget ) :

	def __init__( self, topLevelWidget, scriptNode, **kw ) :
	
		GafferUI.Widget.__init__( self, topLevelWidget, **kw )
		
		assert( isinstance( scriptNode, Gaffer.ScriptNode ) )
		
		self.__scriptNode = scriptNode
		self.__context = None
		self.__setContextInternal( scriptNode.context(), callUpdate=False )
				
	def scriptNode( self ) :
	
		return self.__scriptNode
	
	## By default Editors operate in the main context held by the script node. This function
	# allows an alternative context to be provided, making it possible for an editor to 
	# display itself at a custom frame (or with any other context modification).
	def setContext( self, context ) :
	
		self.__setContextInternal( context, callUpdate=True )
	
	def getContext( self ) :
	
		return self.__context
			
	def __setContextInternal( self, context, callUpdate ) :
	
		assert( isinstance( context, ( Gaffer.Context, types.NoneType ) ) )
	
		self.__context = context
		if self.__context is not None :
			self.__contextChangedConnection = self.__context.changedSignal().connect( Gaffer.WeakMethod( self.__contextChanged ) )
		else :
			self.__contextChangedConnection = None
	
		if callUpdate :
			self._updateFromContext()
		
	## May be implemented by derived classes to update state based on a change of context.
	# To temporarily suspend calls to this function, use Gaffer.BlockedConnection( self._contextChangedConnection() ).
	def _updateFromContext( self ) :
	
		pass
		
	def _contextChangedConnection( self ) :
	
		return self.__contextChangedConnection
	
	## This must be implemented by all derived classes as it is used for serialisation of layouts.
	# It is not expected that the script being edited is also serialised as part of this operation - 
	# instead the new script will be provided later as a variable named scriptNode. So a suitable
	# serialisation will look like "GafferUI.EditorWidget( scriptNode )".
	def __repr__( self ) :
	
		raise NotImplementedError
		
	def __contextChanged( self, context, key ) :
		
		assert( context.isSame( self.getContext() ) )
		
		self._updateFromContext()
	
	@classmethod
	def types( cls ) :
	
		return cls.__namesToCreators.keys()
	
	@classmethod
	def create( cls, name, scriptNode ) :
	
		return cls.__namesToCreators[name]( scriptNode = scriptNode )
	
	@classmethod
	def registerType( cls, name, creator ) :
	
		cls.__namesToCreators[name] = creator
		
	__namesToCreators = {}
