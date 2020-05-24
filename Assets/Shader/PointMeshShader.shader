// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

Shader "Hsinpa/PointMeshShader"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _Parallax ("Parallax", Range(0, 0.3)) = 0
        _Threshold ("Threshold", Range(0.00001, 2)) = 1
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
            #pragma geometry geom
            #pragma target 5.0

            #include "UnityCG.cginc"

            struct v2g {
                float4 vertex : SV_POSITION;
                //float2 uv : TEXCOORD0;
                //float3 normal : NORMAL;
                fixed4 color : COLOR;
                uint id : NUMBER;
            };

            struct g2f {
                float4 worldPos : SV_POSITION;
                fixed4 color : COLOR;
                //float2 uv : TEXCOORD0;
                //fixed4 col : COLOR;
            };

            uniform float3 _WorldCameraPosition;
            uniform float3 _ObjectPosition;
            uniform int _Width;
            uniform int _TotalVertex;

            sampler2D _MainTex;
            float4 _MainTex_ST;

            float _Parallax;
            float _Threshold;

            StructuredBuffer<float3> _PositionBuffer;
            StructuredBuffer<float4> _ColorBuffer;
            StructuredBuffer<int> _Triangle;

            float CrossProductFourPoint(float3 point1, float3 point2, float3 point3, float3 point4) {
                return length(cross(point1, point2) + cross(point2, point3) + cross(point3, point4) + cross(point4, point1)) / 2;
            }

            v2g vert (uint id : SV_VertexID)
            {
                v2g o;

                float4 objectPosition = fixed4(_ObjectPosition + _PositionBuffer[id], 0);
                //objectPosition.z = objectPosition.z + (viewDir.z * _Parallax)

                o.vertex = objectPosition;
                o.color = _ColorBuffer[id];
                //o.color = objectPosition.x + (viewDir.x * _Parallax);
                o.id = id;

                return o;
            }

            [maxvertexcount(4)]
            void geom(point v2g IN[1], inout TriangleStream<g2f> triStream) {
                int id = IN[0].id;
                if (IN[0].id + _Width > _TotalVertex) return;

                g2f o;

                float3 topAngle = float3(0, 1, 0);
                float3 rightAngle = float3(1, 0, 0);
                o.color = IN[0].color;

               float3 basePos1 =  _ObjectPosition + _PositionBuffer[id];
                float3 basePos2 = _ObjectPosition + _PositionBuffer[id+1];
               float3 basePos3 = _ObjectPosition + _PositionBuffer[id + _Width];
                float3 basePos4 = _ObjectPosition + _PositionBuffer[id + _Width +1];
                
                //if (_Threshold < CrossProductFourPoint(basePos1, basePos2, basePos3, basePos4)) return;

                if (_Threshold < length(basePos1 - basePos2) || _Threshold < length(basePos2 - basePos3) ||
                    _Threshold < length(basePos3 - basePos4) || _Threshold < length(basePos4 - basePos1)) return;

                o.worldPos = UnityObjectToClipPos(basePos1);
                triStream.Append(o);

                o.worldPos = UnityObjectToClipPos(basePos2);
                triStream.Append(o);

                o.worldPos = UnityObjectToClipPos(basePos3);
                triStream.Append(o);
                
               o.worldPos = UnityObjectToClipPos(basePos4);
                triStream.Append(o);

                triStream.RestartStrip();
            }

            fixed4 frag (g2f i) : SV_Target
            {
                // sample the texture
                fixed4 col = i.color;

                return col;
            }
            ENDCG
        }
    }
}
