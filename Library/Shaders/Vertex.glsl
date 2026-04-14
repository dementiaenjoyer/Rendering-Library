#version 430 core

out vec2 TextureCoordinates;
in vec2 Position;

void main( ) {
    TextureCoordinates = ( Position * .5 ) + .5; gl_Position = vec4( Position, 0, 1 );
}
