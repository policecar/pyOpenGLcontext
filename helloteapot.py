#!/usr/bin/env python
# -*- coding: utf-8 -*-

# adapted from http://www.seethroughskin.com/blog/?p=771
# which modified http://www.pygame.org/wiki/GLSLExample

from context import *

class HelloTeapot ( Context ):

	def __init__ ( self ):

		vertex_shader = '''
				// Application to vertex shader
				varying vec3 P;
				varying vec3 N;
				varying vec3 I;
	 
				void main()
				{
					// transform vertex by modelview and projection matrices
					gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	 
					// position in clip space
					P = vec3(gl_ModelViewMatrix * gl_Vertex);
	 
					// normal transform (transposed model-view inverse)
					N = gl_NormalMatrix * gl_Normal;
	 
					// Incident vector
					I = P;
	 
					// Forward current color and texture coordinates after applying texture matrix
					gl_FrontColor = gl_Color;
					gl_TexCoord[0] = gl_TextureMatrix[0] * gl_MultiTexCoord0;
				}
				'''
		fragment_shader = '''
				varying vec3 P;
				varying vec3 N;
				varying vec3 I;
	 
				uniform float edgefalloff;
	 
				void main()
				{
					float opacity = dot(normalize(N), normalize(-I));
					opacity = abs(opacity);
					opacity = 1.0 - pow(opacity, edgefalloff);
	 
					gl_FragColor = opacity * gl_Color;
				}
				'''
		
		super ( HelloTeapot, self ).__init__ ( "Nu?", 680, 480, 50, 50, 
			vertex_shader, fragment_shader )

		self.rotY = 0.0						# set defaults
		self.falloffValue = 1.0

	def render ( self ):

		self.mod_falloff(0.0)				# trigger a fall-off modify to update shader
											# clear screen and depth buffer
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		glLoadIdentity()					# reset view

	 	# draw something
		glTranslatef( -1.0, -0.5, -5.0 )		# define position wrt view
		glRotatef( self.rotY, 1.0, 0.0, 0.0 )	# make it spin
	 
		glEnable( GL_BLEND )				# enable blending
		glDepthMask( GL_FALSE )				# disable depth masking 
		glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA ) # x-ray shader applies opacity falloff
	 
	 	glutWireTeapot( 1.0 )				# load a teapot
	 
		glScalef( 0.423, 0.423, 0.423 )		# scale it
		# glutSolidDodecahedron()			# add a dodecahedron
		# glutSolidIcosahedron()
		glutSolidSphere( 4.2, 5, 3 )

		glutSwapBuffers()					# 
	 
		self.rotY += .5

	def mod_falloff ( self, val ):
		self.falloffValue
		if self.shader:
			edgefalloff = glGetUniformLocation( self.shader, "edgefalloff" )
			if not edgefalloff in ( None, -1 ):
				self.falloffValue = self.falloffValue + val
				glUniform1f( edgefalloff, self.falloffValue )

	def keyboard ( self, *args ):
		# pass in ( key, x, y ) tuples
		if args[0] == '\x1b':				# exit on esc
			sys.exit()
		elif args[0] == 'c':
			print "decreasing falloff"
			self.mod_falloff( 1.0 )
		elif args[0] == 'x':
			print "increasing falloff"
			self.mod_falloff( -1.0 )

if __name__ == '__main__':
	print "Hit ESC key to quit."
	print "x - increase shader falloff"
	print "c - decrease shader falloff"
	HelloTeapot().run()