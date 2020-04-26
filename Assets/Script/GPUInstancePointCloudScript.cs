using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[ExecuteInEditMode]
public class GPUInstancePointCloudScript : MonoBehaviour
{
    [SerializeField]
    Texture mainTexture;

    [SerializeField]
    Texture depthTexture;

    [SerializeField]
    ComputeShader computeShader;

    [SerializeField]
    Material material;

    private Vector3 objectPosition;
    public float range;
    private Bounds bounds;

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

    private int textureSize = 512;
    int bufferSize => textureSize * textureSize;

    ComputeBuffer _positionBuffer;
    ComputeBuffer _normalBuffer;
    ComputeBuffer _colorBuffer;
    ComputeBuffer _indicesBuffer;
    ComputeBuffer argsBuffer;



    private void Start()
    {
        //Vector3
        //_positionBuffer = new ComputeBuffer(textureSize * textureSize, floatSize * 3);
        //_normalBuffer = new ComputeBuffer(textureSize * textureSize, floatSize * 3);
        //_colorBuffer = new ComputeBuffer(textureSize * textureSize, floatSize * 4);
        //_indicesBuffer = new ComputeBuffer(textureSize * textureSize, floatSize);
    }

    private void InitMesh()
    {
        mesh = new Mesh();
        mesh.SetVertices(new Vector3[1]);
        mesh.SetIndices(new[] { 0 }, MeshTopology.Points, 0);

        meshFilter.mesh = mesh;
        mesh.UploadMeshData(true);
    }

    private RenderTexture CreateRTexture(int width, int height, Texture rawTexture) {
        RenderTexture mainRenderTexture = new RenderTexture(width, height, 8);
        mainRenderTexture.enableRandomWrite = true;
        mainRenderTexture.Create();

        Graphics.Blit(rawTexture, mainRenderTexture);

        return mainRenderTexture;
    }

    private ComputeBuffer SetComputeBuffer<T>(ComputeBuffer computeBuffer, T[] emptyArray, int size, ComputeBufferType bufferType = ComputeBufferType.Default) {
        computeBuffer = new ComputeBuffer(bufferSize, size, bufferType);
        computeBuffer.SetData(emptyArray);
        return computeBuffer;
    }

    private void InitArgBuffer() {
        uint[] args = new uint[4] { 0, 0, 0, 0 };
        // Arguments for drawing mesh.
        // 0 == number of triangle indices, 1 == population, others are only relevant if drawing submeshes.
        args[0] = (uint)0;
        args[1] = (uint)1;
        args[2] = (uint)0;
        args[3] = (uint)0;
        argsBuffer = new ComputeBuffer(4, sizeof(uint), ComputeBufferType.IndirectArguments);
        argsBuffer.SetData(args);
    }

    void InitData()
    {
        bounds = new Bounds(transform.position, Vector3.one * (range + 1));

        positions = new Vector3[bufferSize];
        colors = new Color[bufferSize];
        indicies = new int[bufferSize];
        normals = new Vector3[bufferSize];
    }

    void Update()
    {

        objectPosition = transform.localPosition;
        if (mainTexture == null || depthTexture == null)
            return;

        //if (positions == null || mesh == null)

        if (isUpdate)
        {
            InitData();
            //InitMesh();
            //InitArgBuffer();

            int kernelHandle = computeShader.FindKernel("GetMesh");

            computeShader.SetInt("TexWidth", textureSize);
            int floatSize = sizeof(float);

            _positionBuffer = SetComputeBuffer(_positionBuffer, positions, floatSize * 3, ComputeBufferType.Default);
            _normalBuffer = SetComputeBuffer(_normalBuffer, normals, floatSize * 3, ComputeBufferType.Default);
            _colorBuffer = SetComputeBuffer(_colorBuffer, colors, floatSize * 4, ComputeBufferType.Default);
            _indicesBuffer = SetComputeBuffer(_indicesBuffer, indicies, floatSize, ComputeBufferType.Default);

            mainRenderTexture = CreateRTexture(textureSize, textureSize, mainTexture);
            depthRenderTexture = CreateRTexture(textureSize, textureSize, depthTexture);

            computeShader.SetTexture(kernelHandle, "MainTex", mainRenderTexture);
            computeShader.SetTexture(kernelHandle, "DepthTex", depthRenderTexture);

            computeShader.SetBuffer(kernelHandle, "PositionBuffer", _positionBuffer);
            computeShader.SetBuffer(kernelHandle, "ColorBuffer", _colorBuffer);
            computeShader.SetBuffer(kernelHandle, "IndicesBuffer", _indicesBuffer);
            computeShader.SetBuffer(kernelHandle, "NormalBuffer", _normalBuffer);

        //    Debug.Log(textureSize / 16);
            computeShader.Dispatch(kernelHandle, textureSize / 16, textureSize / 16, 1);


            //Graphics.DrawMeshInstancedIndirect(mesh, 0, material, bounds, argsBuffer);

            isUpdate = false;
        }
    }

    private void OnRenderObject()
    {
        material.SetPass(0);

        material.SetVector("_ObjectPosition", objectPosition);

        material.SetBuffer("_PositionBuffer", _positionBuffer);

        material.SetBuffer("_ColorBuffer", _colorBuffer);

        Graphics.DrawProceduralNow(MeshTopology.Points, bufferSize, 1);

        //ResetData();
    }


    void ResetData() {
        _positionBuffer.Dispose();
        _colorBuffer.Dispose();
        _indicesBuffer.Dispose();
        _normalBuffer.Dispose();
    }
}
