from moderngl import ( NEAREST as Nearest, TRIANGLE_STRIP as TriangleStrip, create_context as CreateContext );
from numpy import ( zeros as Zeros, uint8 as UInt8, array as Array, empty as Empty );

import glfw as Graphics;

class BufferObject:
    def __init__( Self ):
        Self.Pixels = [ ];
        Self.Stack = [ ];

    def WriteVector2( Self, PositionX, PositionY ):
        Self.Stack = [ PositionX, PositionY ];

    def WriteColor( Self, ColorR = 255, ColorG = 255, ColorB = 255, ColorA = 255 ):
        Pixels = Self.Pixels;
        Stack = Self.Stack;

        PositionX, PositionY = Stack;

        Pixels.append( ( PositionX, PositionY, ColorR, ColorG, ColorB, ColorA ) );
        Stack.clear( )

    def Clear( Self ):
        Self.Pixels.clear( );
        Self.Stack.clear( );

class Renderer:
    def __init__( Self, Name = "Program", Width = 1224, Height = 612 ):
        if ( not Graphics.init( ) ):
            return;

        Window = Graphics.create_window( Width, Height, Name, None, None );
        Self.Window = Window

        if ( not Window ):
            return; Graphics.terminate( );

        Graphics.make_context_current( Window );

        Context = CreateContext( );
        Self.Context = Context;

        Self.Height = Height;
        Self.Width = Width;

        FilePath = __file__;

        Separators = FilePath.split( "/" );
        Path = FilePath.replace( Separators[ len( Separators ) - 1 ], "" );

        Fragment = open( Path + "Shaders/Fragment.glsl", "r" ).read( );
        Vertex = open( Path + "Shaders/Vertex.glsl", "r" ).read( );

        Program = Context.program( vertex_shader = Vertex, fragment_shader = Fragment );
        Buffer = Context.buffer( Array( [ -1, -1, 1, -1, -1, 1, 1, 1 ], dtype = "f4" ) );

        Self.Data = Zeros( ( Height, Width, 4 ), dtype = UInt8 );
        Self.VertexArray = Context.vertex_array(
            Program,
            [ ( Buffer, "2f", "Position" ) ]
        );

        BufferGPU = Context.texture( ( Width, Height ), 4 );
        BufferGPU.filter = ( Nearest, Nearest );

        Self.Texture = BufferGPU
        BufferGPU.use( 0 );

        Program[ "Buffer" ] = 0;

    def Push( Self, Buffer ):
        Pixels = Buffer.Pixels;

        Texture = Self.Texture;
        Data = Self.Data;

        for ( PositionX, PositionY, R, G, B, A ) in Pixels:
            Data[ PositionY, PositionX ] = ( R, G, B, A );

        Texture.write( Data );
        Buffer.Clear( );

    def Stepper( Self ):
        Window = Self.Window;

        if ( Graphics.window_should_close( Window ) ):
            return;

        VertexArray = Self.VertexArray;
        Context = Self.Context;

        Context.clear( 0, 0, 0 );
        VertexArray.render( TriangleStrip );

        Graphics.swap_buffers( Window );
        Graphics.poll_events( );

        return 1;

    def Buffer( Self ):
        return BufferObject( );

    def Clear( Self ):
        Self.Data = Zeros( ( Self.Height, Self.Width, 4 ), dtype = UInt8 );

    def Exit( Self ):
        Graphics.terminate( );
