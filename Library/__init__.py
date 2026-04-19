from moderngl import ( NEAREST as Nearest, TRIANGLE_STRIP as TriangleStrip, create_context as CreateContext );
from numpy import ( zeros as Zeros, uint8 as UInt8, array as Array );

import glfw as Graphics;

class Renderer:
    def __init__( Self, Name = "Program", Width = 1224, Height = 612 ):
        if ( not Graphics.init( ) ):
            return;

        Window = Graphics.create_window( Width, Height, Name, None, None );
        Self.Window = Window;

        if ( not Window ):
            return Graphics.terminate( );

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

        Self.Canvas = Zeros( ( Height, Width, 4 ), dtype = UInt8 );
        Self.MemoryView = memoryview( Self.Canvas );

        Self.VertexArray = Context.vertex_array(
            Program,
            [ ( Buffer, "2f", "Position" ) ]
        );

        BufferGPU = Context.texture( ( Width, Height ), 4 );
        BufferGPU.filter = ( Nearest, Nearest );

        Self.Texture = BufferGPU;
        BufferGPU.use( 0 );

        Program[ "Buffer" ] = 0;

    def WriteQuad( Self, PositionX, PositionY, SizeX, SizeY, R, G, B, A ):
        Self.Canvas[ max( 0, PositionY ) : ( PositionY + SizeY ), max( 0, PositionX ) : ( PositionX + SizeX ) ] = ( R, G, B, A );

    def Update( Self ):
        Self.Texture.write( Self.MemoryView );

    def Stepper( Self ):
        Window = Self.Window;

        if ( Graphics.window_should_close( Window ) ):
            return;

        Self.Context.clear( 0, 0, 0 );
        Self.VertexArray.render( TriangleStrip );

        Graphics.swap_buffers( Window );
        Graphics.poll_events( );

        return 1;

    def Clear( Self ):
        Self.Canvas.fill( 0 );

    def Exit( Self ):
        Graphics.terminate( );
