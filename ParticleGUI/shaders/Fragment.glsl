#version 410 core

layout(location =0) out vec4 fragment_colour;
uniform sampler2D tex;

in vec3 out_colour;
void main()
{


// vec2 circle_cord = 2.0 * gl_PointCoord - 1.0;
// if(dot(circle_cord,circle_cord) > 1.0)
// {
//     discard;
// }


fragment_colour.rgb=normalize(out_colour * texture(tex,gl_PointCoord).rgb);
fragment_colour.a = texture(tex,gl_PointCoord).a;


    // fragment_colour.rgb = out_colour;
}
