"""Codigo GLSL dos shaders (explicados no README / na apresentacao).

Atributos de vertice : vertexPosition(loc 0), vertexNormal(loc 1), vertexUV(loc 2)
Uniforms (vertex)    : modelMatrix, viewMatrix, projectionMatrix, normalMatrix, lightMatrix, repeatUV
Uniforms (fragment)  : baseColor, useTexture, tex, shininess, specularStrength, ambientColor,
                       lightColor, lightDir, viewPos, shadowOn, shadowMap, shadowStrength, shadowBias
Passe de sombra      : so modelMatrix e lightMatrix; o fragment shader e vazio (grava so a profundidade).
"""

VERTEX_PRINCIPAL = """
#version 330 core
layout(location = 0) in vec3 vertexPosition;
layout(location = 1) in vec3 vertexNormal;
layout(location = 2) in vec2 vertexUV;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform mat3 normalMatrix;      // transposta da inversa de mat3(modelMatrix)
uniform mat4 lightMatrix;       // projecao * visao da camera da LUZ
uniform vec2 repeatUV;
out vec3 vWorldPos;
out vec3 vNormal;
out vec2 vUV;
out vec4 vLightPos;
void main() {
    vec4 mundo = modelMatrix * vec4(vertexPosition, 1.0);
    vWorldPos = mundo.xyz;
    vNormal = normalMatrix * vertexNormal;
    vUV = vertexUV * repeatUV;
    vLightPos = lightMatrix * mundo;      // posicao do fragmento no espaco da luz (shadow map)
    gl_Position = projectionMatrix * viewMatrix * mundo;
}
"""

FRAGMENT_PRINCIPAL = """
#version 330 core
in vec3 vWorldPos;
in vec3 vNormal;
in vec2 vUV;
in vec4 vLightPos;
uniform vec3 baseColor;
uniform bool useTexture;
uniform sampler2D tex;
uniform float shininess;
uniform float specularStrength;
uniform vec3 ambientColor;
uniform vec3 lightColor;
uniform vec3 lightDir;          // direcao em que a luz VIAJA (do sol para a cena)
uniform vec3 viewPos;
uniform bool shadowOn;
uniform sampler2D shadowMap;
uniform float shadowStrength;
uniform float shadowBias;
out vec4 fragColor;

// SOMBRA PROJETADA: compara a profundidade do fragmento (vista da luz) com o shadow map.
float calcSombra(vec3 N, vec3 L) {
    vec3 p = vLightPos.xyz / vLightPos.w * 0.5 + 0.5;
    if (p.z > 1.0) return 0.0;
    float bias = max(shadowBias * (1.0 - dot(N, L)), shadowBias * 0.25);
    vec2 texel = 1.0 / vec2(textureSize(shadowMap, 0));
    float s = 0.0;
    for (int x = -1; x <= 1; x++)
        for (int y = -1; y <= 1; y++) {
            float d = texture(shadowMap, p.xy + vec2(x, y) * texel).r;
            s += (p.z - bias > d) ? 1.0 : 0.0;      // PCF 3x3: bordas suaves
        }
    return s / 9.0;
}

void main() {
    vec3 N = normalize(vNormal);
    vec3 L = normalize(-lightDir);
    vec3 V = normalize(viewPos - vWorldPos);
    // SOMBREAMENTO da superficie (depende do angulo entre normal e luz)
    float difusa = max(dot(N, L), 0.0);
    vec3 R = reflect(-L, N);
    float espec = (difusa > 0.0) ? pow(max(dot(R, V), 0.0), shininess) : 0.0;
    float sombra = shadowOn ? calcSombra(N, L) * shadowStrength : 0.0;
    vec3 albedo = baseColor * (useTexture ? texture(tex, vUV).rgb : vec3(1.0));
    vec3 cor = albedo * (ambientColor + (1.0 - sombra) * difusa * lightColor)
             + (1.0 - sombra) * espec * specularStrength * lightColor;
    fragColor = vec4(cor, 1.0);
}
"""

VERTEX_PROFUNDIDADE = """
#version 330 core
layout(location = 0) in vec3 vertexPosition;
uniform mat4 modelMatrix;
uniform mat4 lightMatrix;
void main() { gl_Position = lightMatrix * modelMatrix * vec4(vertexPosition, 1.0); }
"""

FRAGMENT_PROFUNDIDADE = """
#version 330 core
void main() { }
"""
