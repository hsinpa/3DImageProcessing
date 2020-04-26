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

    public RenderTexture mainRenderTexture;
    public RenderTexture depthRenderTexture;

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

    private int textureSize = 256;
    int bufferSize => textureSize * textureSize;

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

        //if (positions == null || mesh == null)
            InitData();

        if (isUpdate)
        {
            int kernelHandle = computeShader.FindKernel("GetMesh");

            computeShader.SetInt("TexWidth", textureSize);
            int floatSize = sizeof(float);

            _positionBuffer = new ComputeBuffer(bufferSize, floatSize * 3);
            _positionBuffer.SetData(positions);

            _normalBuffer = new ComputeBuffer(bufferSize, floatSize * 3);
            _normalBuffer.SetData(normals);

            _colorBuffer = new ComputeBuffer(bufferSize, floatSize * 4);
            _colorBuffer.SetData(colors);

            _indicesBuffer = new ComputeBuffer(bufferSize, floatSize);
            _indicesBuffer.SetData(indicies);

            mainRenderTexture = new RenderTexture(textureSize, textureSize, 8);
            mainRenderTexture.enableRandomWrite = true;
            mainRenderTexture.Create();

            depthRenderTexture = new RenderTexture(textureSize, textureSize, 8);
            depthRenderTexture.enableRandomWrite = true;
            depthRenderTexture.Create();

            Graphics.Blit(mainTexture, mainRenderTexture);
            Graphics.Blit(depthTexture, depthRenderTexture);

            computeShader.SetTexture(kernelHandle, "MainTex", mainTexture);
            computeShader.SetTexture(kernelHandle, "DepthTex", depthTexture);
            //computeShader.SetTexture(kernelHandle, "Result", depthRenderTexture);

            computeShader.SetBuffer(kernelHandle, "PositionBuffer", _positionBuffer);
            computeShader.SetBuffer(kernelHandle, "ColorBuffer", _colorBuffer);
            computeShader.SetBuffer(kernelHandle, "IndicesBuffer", _indicesBuffer);
            computeShader.SetBuffer(kernelHandle, "NormalBuffer", _normalBuffer);

            computeShader.Dispatch(kernelHandle, textureSize / 16, textureSize / 16, 1);

            _positionBuffer.GetData(positions);
            _colorBuffer.GetData(colors);
            _indicesBuffer.GetData(indicies);
            _normalBuffer.GetData(normals);

            //Debug.Log(normals.Length);

            //mesh = new Mesh();
            //mesh.SetVertices(positions);
            
            //mesh.SetIndices(indicies, MeshTopology.Points, 0);
            //mesh.SetColors(colors);
            ////mesh.SetNormals(normals);
            //meshFilter.mesh = mesh;

            //isUpdate = false;
            //ResetData();
        }
    }

    private void LateUpdate()
    {
        if (isUpdate)
        {
            _positionBuffer.GetData(positions);
            _colorBuffer.GetData(colors);
            _indicesBuffer.GetData(indicies);
            _normalBuffer.GetData(normals);

            Debug.Log(normals.Length);

            mesh = new Mesh();
            mesh.SetVertices(positions);

            mesh.SetIndices(indicies, MeshTopology.Points, 0);
            mesh.SetColors(colors);
            //mesh.SetNormals(normals);
            meshFilter.mesh = mesh;

            isUpdate = false;

        }
    }

    void InitData() {
        positions = new Vector3[bufferSize];
        colors = new Color[bufferSize];
        indicies = new int[bufferSize];
        normals = new Vector3[bufferSize];

        mesh = new Mesh();
        
    }

    void ResetData() {
        _positionBuffer.Dispose();
        _colorBuffer.Dispose();
        _indicesBuffer.Dispose();
        _normalBuffer.Dispose();
    }
}
