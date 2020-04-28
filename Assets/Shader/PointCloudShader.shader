// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

Shader "Hsinpa/PointCloudShader"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _PointSize ("Point Size", Range(0.001, 0.1)) = 1
        _Threshold("Threshold", Range(0.0001, 0.1)) = 1
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
            #pragma geometry geom
            #pragma fragment frag

            #include "UnityCG.cginc"

 
            struct v2g{
                float4 vertex : SV_POSITION;
                float2 uv : TEXCOORD0;
                float3 normal : NORMAL;
                fixed4 color : COLOR;
                uint id : NUMBER;
            };
 
            struct g2f{
                float4 worldPos : SV_POSITION;
                float3 normal : NORMAL;
                fixed4 color : COLOR;
                //float2 uv : TEXCOORD0;
                //fixed4 col : COLOR;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;

            float _PointSize;
            float _Threshold;

            StructuredBuffer<float3> _PositionBuffer;
            StructuredBuffer<float4> _ColorBuffer;
            StructuredBuffer<int> _Triangle;

            uniform float3 _ObjectPosition;
            uniform int _Width;
            uniform int _TotalVertex;


            v2g vert (uint id : SV_VertexID)
            {
                v2g o;

                float3 objectPosition = _ObjectPosition + _PositionBuffer[id];

                o.vertex = fixed4((objectPosition),0);
                o.color = _ColorBuffer[id];
                o.id = id;

                return o;
            }

            [maxvertexcount(12)]
            void geom(point v2g IN[1], inout TriangleStream<g2f> triStream) {
                int id = IN[0].id;
                if (id + _Width > _TotalVertex && id <= 0) return;

                g2f o;

                int rightId = id - 1;
                int leftId = id + 1;
                int topId = id + _Width + 1;

                float3 topDir = float3(0, 1, 0);
                float3 rightDir = float3(1, 0, 0);
                float3 frontDir = float3(0, 0, 1);

                float3 nor = IN[0].normal;

                o.normal = nor;
                o.color = IN[0].color;

                //Front
                float3 basePos = _ObjectPosition + _PositionBuffer[id];
                float3 basePosTop = basePos + _PointSize * topDir;

                o.worldPos = UnityObjectToClipPos(basePos - rightDir * _PointSize * 0.5);
                triStream.Append(o);          
               
                o.worldPos = UnityObjectToClipPos(basePos + rightDir * _PointSize * 0.5);
                triStream.Append(o);    

                o.worldPos = UnityObjectToClipPos(basePosTop - rightDir * _PointSize * 0.5);
                triStream.Append(o);

                o.worldPos = UnityObjectToClipPos(basePosTop + rightDir * _PointSize * 0.5);
                triStream.Append(o);

                //Left Side
                if (_Threshold < length(_PositionBuffer[id] - _PositionBuffer[rightId])) {
                    o.worldPos = UnityObjectToClipPos(basePos - rightDir * 0.5 * _PointSize - (frontDir * _PointSize));
                    triStream.Append(o);

                    o.worldPos = UnityObjectToClipPos(basePosTop - rightDir * 0.5 * _PointSize - (frontDir * _PointSize));
                    triStream.Append(o);

                    o.worldPos = UnityObjectToClipPos(basePos - rightDir * 0.5 * _PointSize);
                    triStream.Append(o);

                    o.worldPos = UnityObjectToClipPos(basePosTop - rightDir * 0.5 * _PointSize);
                    triStream.Append(o);
                }

                //Top Side
                if (_Threshold < length(_PositionBuffer[id] - _PositionBuffer[topId])) {
                    o.worldPos = UnityObjectToClipPos(basePosTop - rightDir * _PointSize * 0.5);
                    triStream.Append(o);

                    o.worldPos = UnityObjectToClipPos(basePosTop + rightDir * _PointSize * 0.5);
                    triStream.Append(o);

                    o.worldPos = UnityObjectToClipPos(basePosTop - rightDir * 0.5 * _PointSize - (frontDir * _PointSize));
                    triStream.Append(o);

                    o.worldPos = UnityObjectToClipPos(basePosTop + rightDir * 0.5 * _PointSize - (frontDir * _PointSize));
                    triStream.Append(o);
                }



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

