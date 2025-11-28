#version 410 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 colour;
out vec3 out_colour;
uniform mat4 MVP;
void main()
{
    out_colour=colour;
    gl_Position = MVP*vec4(position,1.0);
}
