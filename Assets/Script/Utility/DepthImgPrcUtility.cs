using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace DepthImgPrc
{
    public class DepthImgPrcUtility
    {
        public static RenderTexture CreateRTexture(int width, int height, Texture rawTexture)
        {
            RenderTexture mainRenderTexture = new RenderTexture(width, height, 8);
            mainRenderTexture.enableRandomWrite = true;
            mainRenderTexture.Create();

            Graphics.Blit(rawTexture, mainRenderTexture);

            return mainRenderTexture;
        }
    }
}