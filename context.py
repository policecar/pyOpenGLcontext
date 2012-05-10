#!/usr/bin/env python
# -*- coding: utf-8 -*-

# adapted from http://www.seethroughskin.com/blog/?p=771
# which modified http://www.pygame.org/wiki/GLSLExample

# import OpenGL 
# OpenGL.ERROR_ON_COPY = True 

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGL.GL import shaders

import time, sys

class Context( object ):
	'''Context with GLUT window'''

	def __init__ ( self, title="title", width=640, height=480, pos_x=50, pos_y=50, 
					vertex_shader='''''', fragment_shader='''''' ):
	 
		self.width = width
		self.height = height

		glutInit( sys.argv )
		self.window = self.init_window( title, pos_x, pos_y )
		self.register_callbacks()

		glClearColor( 0.0, 0.0, 0.0, 0.0 )	# clear background color
		glClearDepth( 1.0 )					# enable depth buffer clearing
		glShadeModel( GL_SMOOTH )			# enable smooth color shading

		glMatrixMode( GL_PROJECTION )
		glLoadIdentity()                   	# reset projection matrix
											# calculate window's aspect ratio
		gluPerspective( 45.0, float(width) / float(height), 0.1, 100.0 )
		glMatrixMode( GL_MODELVIEW )

		self.shader = shaders.compileProgram ( # uses OpenGL.GL.shaders
						shaders.compileShader( vertex_shader, GL_VERTEX_SHADER ),
						shaders.compileShader( fragment_shader, GL_FRAGMENT_SHADER ) )
		glUseProgram( self.shader )
	
	def init_window ( self, title, pos_x=0, pos_y=0 ):
		'''Create a window object'''
		
		glutInitDisplayMode( GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH ) # select display mode
		glutInitWindowPosition( pos_x, pos_y )			# set upper left corner on screen
		glutInitWindowSize( self.width, self.height )
		return glutCreateWindow( title )

	def register_callbacks( self ):
		'''Register a bunch of callback functions for various events'''
		
		glutDisplayFunc( self.render )		# display callback function
		# glutFullScreen()
		glutIdleFunc( self.render )
		glutReshapeFunc( self.resize )		# window resize event
		glutKeyboardFunc( self.keyboard )
		glutMouseFunc( self.mouse )

	def resize ( self, width, height ):
		glViewport( 0, 0, width, height )	# reset current viewport and perspective transformation
		glMatrixMode( GL_PROJECTION )
		glLoadIdentity()
		gluPerspective( 45.0, float(width) / float(height), 0.1, 100.0 )
		glMatrixMode( GL_MODELVIEW )

	def render ( self ):
		'''For subclass to implement their rendering behavior.'''
		raise NotImplementedError
		
	def keyboard ( self, *args ):
		# pass in ( key, x, y ) tuples
		'''For subclass to implement their keyboard behavior.'''
		raise NotImplementedError

	def mouse ( *args ):
		'''For subclass to implement their mouse behavior.'''
		raise NotImplementedError

	@staticmethod
	def run ():
		glutMainLoop()		# start the event processing engine