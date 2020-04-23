// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

// Upgrade NOTE: replaced '_Object2World' with 'unity_ObjectToWorld'

Shader "Hsinpa/VIrutalImageShader"
{
    Properties
    {
        _MainTex ("MainTexture", 2D) = "white" {}
        _DepthTex ("DepthTexture", 2D) = "white" {}
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;

            sampler2D _DepthTex;
            float4 _DepthTex_ST;

            uniform float4 _MousePosition;

            v2f vert (appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                // sample the texture, uv + mouse*depth.r
                fixed4 depth = tex2D(_DepthTex, i.uv);

                fixed4 col = tex2D(_MainTex, i.uv + (_MousePosition * depth.r));

                return col;
            }
            ENDCG
        }
    }
}
