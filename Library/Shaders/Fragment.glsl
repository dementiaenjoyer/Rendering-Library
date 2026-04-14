#version 430 core

in vec2 TextureCoordinates;
uniform sampler2D Buffer;

out vec4 Color;

void main() {
    Color = texture( Buffer, TextureCoordinates );
}
