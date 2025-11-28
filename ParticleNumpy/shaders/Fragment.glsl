#version 410 core

layout(location =0) out vec4 fragment_colour;
in vec3 out_colour;
void main()
{
    fragment_colour.rgb = out_colour;
}
