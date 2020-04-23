// Upgrade NOTE: replaced '_Object2World' with 'unity_ObjectToWorld'

Shader "Hsinpa/MouseImageShader"
{
    Properties
    {
        _MainTex ("MainTexture", 2D) = "white" {}
        _DepthTex ("DepthTexture", 2D) = "white" {}
        _Strength("DepthStregth", Range(0, 5)) = 0
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
            float _Strength;


            v2f vert (appdata v)
            {
                v2f o;

                float4 worldPos = mul(unity_ObjectToWorld, v.vertex);

                float4 tex = tex2Dlod (_DepthTex, float4(v.uv.xy,0,0));

                worldPos.z += tex.r* (pow(_Strength, 2));

                o.vertex = mul(UNITY_MATRIX_VP, worldPos);

                o.uv = TRANSFORM_TEX(v.uv, _MainTex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                // sample the texture
                fixed4 col = tex2D(_MainTex, i.uv);
                return col;
            }
            ENDCG
        }
    }
}
