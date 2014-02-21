    #ifdef GL_ES
    precision highp float;
    #endif
    
    uniform float MyIter;
    uniform float MyTime;
    varying vec4 MyCoord4f;

    float hue2rgb( float p, float q, float t ) {

        if( t < 0.0 ) t += 1.0;
        if( t > 1.0 ) t -= 1.0;
        if( t < 1.0/6.0 ) return p + (q - p) * 6.0 * t;
        if( t < 1.0/2.0 ) return q;
        if( t < 2.0/3.0 ) return p + (q - p) * (2.0/3.0 - t) * 6.0;
        return p;
    }

    void main() {

        vec2 z, c;

        // chose b/w mandelbrot and julia set

        //c.x = MyCoord4f.x;
        //c.y = MyCoord4f.y;
        c.x = 0.3;
        c.y = 0.0;

        z.x = MyCoord4f.x;
        z.y = MyCoord4f.y;

        float i = 0.0;
        while( i < MyIter ) {

            float x = ( z.x * z.x - z.y * z.y ) + c.x;
            float y = ( z.x * z.y + z.y * z.x ) + c.y;

            if( ( x * x + y * y ) > 4.0 ) break;

            z.x = x;
            z.y = y;
            i += 1.0;
        }

        // a color scheme from the Orange Book OpenGLSL 2nd Edition
        vec3 color;
        if ( i == MyIter ) {
            color = vec3( 0.0, 0.3, 0.8 );
        } else { // i.e. z is going towards infinity, show how fast
            color = mix( vec3( 0.65, 0.25, 0.25 ), vec3( 0.7, 0.65, 0.1 ), fract( i * 0.05 ));
            // color = mix( vec3( 0.0, 0.3, 0.8 ), vec3( 0.75, 0.25, 0.25 ), fract( i * 0.1 ));
        }
        gl_FragColor = vec4( color, 1.0 );
   
    }
