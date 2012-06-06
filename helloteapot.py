#!/usr/bin/env python
# -*- coding: utf-8 -*-

# originally adapted from http://www.seethroughskin.com/blog/?p=771
# which modified http://www.pygame.org/wiki/GLSLExample

# cf. http://www.songho.ca/opengl/gl_transform.html 
# for a good explanation on transformations

from context import *

class HelloTeapot ( Context ):

	def __init__ ( self ):

		vertex_shader = '''
				varying vec3 P;
				varying vec3 N;
				varying vec3 I;
	 
				void main()
				{
					// transform vertex by modelview and projection matrices
					gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	 
					// position in clip space
					P = vec3( gl_ModelViewMatrix * gl_Vertex );
	 
					// normal transform (transposed model-view inverse)
					N = gl_NormalMatrix * gl_Normal;
	 
					// incident vector
					I = P;
	 
					// forward current color and texture coordinates after applying texture matrix
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
					float opacity = dot( normalize(N), normalize(-I) );
					opacity = abs( opacity );
					opacity = 1.0 - pow( opacity, edgefalloff );
	 
					gl_FragColor = opacity * gl_Color;
				}
				'''

		super ( HelloTeapot, self ).__init__ ( "Nu?", 680, 480, 50, 50, 
			vertex_shader, fragment_shader )

		glutIdleFunc( self.display )		# set callback for being idle

		self.rotY = 0.0						# set defaults
		self.falloffValue = 1.0


	def display ( self ):
		'''Custom display /render function. Structural sample provided.'''
		
		# clear color and depth buffer
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

		# stuff
		self.mod_falloff(0.0)				# trigger a fall-off modify to update shader
	 
		glEnable( GL_BLEND )				# enable blending
		glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA ) # x-ray shader applies opacity falloff

		# GL_MODELVIEW : transformation matrix from object to eye coordinates
		# combining MODEL ( object to world space ) and VIEW ( world to eye space ) 
		glMatrixMode( GL_MODELVIEW )		# specify matrix stack for subsequent operations
		glLoadIdentity()					# replace current matrix with identity matrix
		
		glScalef( 1.0, 1.0, 1.0 )			# listed for completion
		glTranslatef( -1.0, -0.5, -5.0  )
		glRotatef( self.rotY, 1.0, 0.0, 0.0 )
	 	glutWireTeapot( 1.0 )				# load a teapot
	 
		glScalef( 0.423, 0.423, 0.423 )		# scale it
		glutSolidSphere( 4.2, 5, 3 )

		# glFlush()
		glutSwapBuffers()					#
	 
		self.rotY += .5


	def reshape ( self, width, height ):
		'''Scale projection with window size.'''
		
		# GL_PROJECTION : transformation matrix from eye to clip coordinates
		# combining viewing frustum ( 3D to 2D ) and normalized device coordinates
		glMatrixMode( GL_PROJECTION )
		glLoadIdentity()

		# # define coordinate system
		# glOrtho( 0.0, width, 0.0, height, -1.0, 1.0 )
		
		# specify viewer's perspective into coordinate system
		gluPerspective( 45.0, float(width) / float(height), 0.1, 100.0 )

		# transformation from normalized device coordinates to window coordinates
		glViewport( 0, 0, width, height )	# define viewport, here: ALL the window


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


	def mod_falloff ( self, val ):
		self.falloffValue
		if self.shader:
			edgefalloff = glGetUniformLocation( self.shader, "edgefalloff" )
			if not edgefalloff in ( None, -1 ):
				self.falloffValue = self.falloffValue + val
				glUniform1f( edgefalloff, self.falloffValue )


if __name__ == '__main__':
	print "Hit ESC key to quit."
	print "x - increase shader falloff"
	print "c - decrease shader falloff"
	HelloTeapot().run()