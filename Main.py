from bresenham import ( bresenham as Bresenham );
from scipy.spatial.transform import ( Rotation );

from numpy import ( array as Array );
from time import ( time as Time );

from Library import ( Renderer );

Vertices = Array( [
    ( -1, -1, -1 ), ( 1, -1, -1 ), ( 1, 1, -1 ), ( -1, 1, -1 ),
    ( -1, -1, 1 ), ( 1, -1, 1 ), ( 1, 1, 1 ), ( -1, 1, 1 ),
], dtype = "f4" );

Edges = [
    ( 0, 1 ), ( 1, 2 ), ( 2, 3 ), ( 3, 0 ),
    ( 4, 5 ), ( 5, 6 ), ( 6, 7 ), ( 7, 4 ),
    ( 0, 4 ), ( 1, 5 ), ( 2, 6 ), ( 3, 7 ),
];

Width, Height = 1344, 720;

LibraryObject = Renderer( Height = Height, Width = Width );
Angle, Epsilon = 0, ( 1 * .01 );

CenterY = Height * .5;
CenterX = Width * .5

while ( LibraryObject.Stepper( ) ):
    LibraryObject.Clear( );
    Angle += Epsilon;

    Rotated = Vertices @ Rotation.from_euler( "xy", [ Angle, Angle ] ).as_matrix().T;
    Projection = ( Rotated[ :, : 2 ] / ( Rotated[ :, 2 : 3 ] + 4 ) * CenterY + [ CenterX, CenterY ] ).astype( int );

    for Origin, Destination in Edges:
        for X, Y in Bresenham( * Projection[ Origin ], * Projection[ Destination ] ):
            LibraryObject.WriteQuad( X, Y, 1, 1, 255, 255, 255, 255 );

    LibraryObject.Update( );
