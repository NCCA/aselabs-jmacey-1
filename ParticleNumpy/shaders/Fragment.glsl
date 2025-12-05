#version 410 core

layout(location =0) out vec4 fragment_colour;
in vec3 out_colour;
void main()
{
    vec2 circle_cord = 2.0 * gl_PointCoord - 1.0;
    if(dot(circle_cord,circle_cord) > 1.0)
    {
        discard;
    }

    fragment_colour.rgb = out_colour;
}
