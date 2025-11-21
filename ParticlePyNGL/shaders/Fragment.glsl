#version 410 core

layout(location =0) out vec4 fragment_colour;
uniform vec3 colour;
void main()
{
    fragment_colour.rgb = colour;
}
