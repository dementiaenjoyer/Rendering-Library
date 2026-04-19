import Library;

LibraryObject = Library.Renderer( Name = "Window", Width = 144, Height = 64 );
Buffer = LibraryObject.Buffer( );

while ( LibraryObject.Stepper( ) ):
    LibraryObject.Clear( );

    Buffer.WriteVector2( 20, 20 );
    Buffer.WriteColor( 255, 0, 0 );

    LibraryObject.Push( Buffer );

LibraryObject.Exit( );
