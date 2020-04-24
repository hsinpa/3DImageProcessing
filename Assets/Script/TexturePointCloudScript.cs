using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[ExecuteInEditMode]
public class TexturePointCloudScript : MonoBehaviour
{
    [SerializeField]
    Texture mainTexture;

    [SerializeField]
    Texture depthTexture;

    [SerializeField]
    ComputeShader computeShader;

    RenderTexture mainRenderTexture;
    RenderTexture depthRenderTexture;

    [SerializeField]
    bool isUpdate;

    [SerializeField]
    private MeshFilter meshFilter;

    private Mesh mesh;

    public Vector2 size;

    Vector3[] positions;
    int[] indicies;
    Vector3[] normals;
    Color[] colors;

    int textureSize = 512;

    ComputeBuffer _positionBuffer;
    ComputeBuffer _normalBuffer;
    ComputeBuffer _colorBuffer;
    ComputeBuffer _indicesBuffer;

    private void Start()
    {

        //Vector3
        //_positionBuffer = new ComputeBuffer(textureSize * textureSize, floatSize * 3);
        //_normalBuffer = new ComputeBuffer(textureSize * textureSize, floatSize * 3);
        //_colorBuffer = new ComputeBuffer(textureSize * textureSize, floatSize * 4);
        //_indicesBuffer = new ComputeBuffer(textureSize * textureSize, floatSize);
    }

    void Update()
    {
        if (mainTexture == null || depthTexture == null)
            return;

        if (isUpdate) {
            int kernelHandle = computeShader.FindKernel("GetMesh");

            int floatSize = sizeof(float);
            _positionBuffer = new ComputeBuffer(textureSize * textureSize, floatSize * 3);
            _normalBuffer = new ComputeBuffer(textureSize * textureSize, floatSize * 3);
            _colorBuffer = new ComputeBuffer(textureSize * textureSize, floatSize * 4);
            _indicesBuffer = new ComputeBuffer(textureSize * textureSize, floatSize);

            mainRenderTexture = new RenderTexture(textureSize, textureSize, 24);
            mainRenderTexture.enableRandomWrite = true;
            mainRenderTexture.Create();

            depthRenderTexture = new RenderTexture(textureSize, textureSize, 24);
            depthRenderTexture.enableRandomWrite = true;
            depthRenderTexture.Create();


            Graphics.Blit(mainTexture, mainRenderTexture);
            Graphics.Blit(depthTexture, depthRenderTexture);

            computeShader.SetTexture(kernelHandle, "MainTex", mainTexture);
            computeShader.SetTexture(kernelHandle, "DepthTex", depthTexture);

            computeShader.SetBuffer(kernelHandle, "PositionBuffer", _positionBuffer);
            computeShader.SetBuffer(kernelHandle, "ColorBuffer", _colorBuffer);
            computeShader.SetBuffer(kernelHandle, "IndicesBuffer", _indicesBuffer);
            computeShader.SetBuffer(kernelHandle, "NormalBuffer", _normalBuffer);


            computeShader.Dispatch(kernelHandle, textureSize / 8, textureSize / 8, 1);

            _positionBuffer.GetData(positions);
            _colorBuffer.GetData(colors);
            _indicesBuffer.GetData(indicies);
            _normalBuffer.GetData(normals);

            Debug.Log(normals.Length);

            //mesh = new Mesh();

            //mesh.SetVertices(positions);
            //mesh.SetIndices(indicies, MeshTopolWWogy.Points, 0);
            //mesh.SetColors(colors);

            //meshFilter.mesh = mesh;


            isUpdate = false;
        }
    }
}
