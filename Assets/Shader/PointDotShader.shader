// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

Shader "Hsinpa/PointDotShader"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _PointSize ("Point Size", Range(0.01, 0.1)) = 1
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100
        Cull off

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma target 5.0

            #include "UnityCG.cginc"

            struct v2f{
                float4 vertex : SV_POSITION;
                float2 uv : TEXCOORD0;
                float3 normal : NORMAL;
                fixed4 color : COLOR;
            };

            uniform float3 _ObjectPosition;

            sampler2D _MainTex;
            float4 _MainTex_ST;

            float _PointSize;

            StructuredBuffer<float3> _PositionBuffer;
            StructuredBuffer<float4> _ColorBuffer;

            v2f vert (uint id : SV_VertexID)
            {
                v2f o;

                float3 objectPosition = _ObjectPosition + _PositionBuffer[id];

                o.vertex = UnityObjectToClipPos(objectPosition);
                o.color = _ColorBuffer[id];
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                // sample the texture
                fixed4 col = i.color;

                return col;
            }
            ENDCG
        }
    }
}
