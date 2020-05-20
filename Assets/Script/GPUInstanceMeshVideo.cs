using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using DepthImgPrc;

[ExecuteInEditMode]
public class GPUInstanceMeshVideo : MonoBehaviour
{

    [SerializeField]
    ComputeShader computeShader;

    [SerializeField]
    Material material;

    [SerializeField, Range(1, 10)]
    private float DepthPower = 1;

    [SerializeField]
    private bool isDepthRevert;

    private Vector3 objectPosition;
    public float range;
    private Bounds bounds;

    [SerializeField]
    private RenderTexture mainRenderTexture;

    [SerializeField]
    private RenderTexture depthRenderTexture;

    [SerializeField]
    bool isUpdate;

    [SerializeField]
    private MeshFilter meshFilter;

    #region Compute Shader Parameter
    Vector3[] positions;
    int[] indicies;
    Vector3[] normals;
    Color[] colors;

    int kernelHandle;

    private int depthTxtSize = 128;
    private int mainTxtSize = 256;
    private float targetEndDiff;

    int bufferSize => mainTxtSize * mainTxtSize;

    ComputeBuffer _positionBuffer;
    ComputeBuffer _normalBuffer;
    ComputeBuffer _colorBuffer;
    ComputeBuffer _indicesBuffer;
    #endregion

    private void Start()
    {

    }

    private ComputeBuffer SetComputeBuffer<T>(ComputeBuffer computeBuffer, T[] emptyArray, int size, ComputeBufferType bufferType = ComputeBufferType.Default) {
        computeBuffer = new ComputeBuffer(bufferSize, size, bufferType);
        computeBuffer.SetData(emptyArray);
        return computeBuffer;
    }

    void InitData()
    {
        bounds = new Bounds(transform.position, Vector3.one * (range + 1));

        positions = new Vector3[bufferSize];
        colors = new Color[bufferSize];
        indicies = new int[bufferSize];
        normals = new Vector3[bufferSize];

        targetEndDiff = ((float) depthTxtSize / mainTxtSize);

        Debug.Log(targetEndDiff);
    }

    void InitComputeShader() {
        int floatSize = sizeof(float);
        kernelHandle = computeShader.FindKernel("GetMesh");
        
        computeShader.SetInt("TexWidth", mainTxtSize);
        computeShader.SetInt("DepthTxtWidth", depthTxtSize);
        computeShader.SetFloat("TargetEndDiff", targetEndDiff);

        _positionBuffer = SetComputeBuffer(_positionBuffer, positions, floatSize * 3, ComputeBufferType.Default);
        _normalBuffer = SetComputeBuffer(_normalBuffer, normals, floatSize * 3, ComputeBufferType.Default);
        _colorBuffer = SetComputeBuffer(_colorBuffer, colors, floatSize * 4, ComputeBufferType.Default);
        _indicesBuffer = SetComputeBuffer(_indicesBuffer, indicies, floatSize, ComputeBufferType.Default);
    }

    void Update()
    {
        objectPosition = transform.localPosition;

        if (mainRenderTexture == null || depthRenderTexture == null)
            return;

        if (positions == null || _positionBuffer == null || isUpdate) {
            InitData();
            InitComputeShader();

            isUpdate = false;
        }

        computeShader.SetFloat("DepthPower", DepthPower);
        computeShader.SetInt("DepthMapRevertFlag", isDepthRevert ? -1 : 1);

        computeShader.SetTexture(kernelHandle, "MainTex", mainRenderTexture);
        computeShader.SetTexture(kernelHandle, "DepthTex", depthRenderTexture);

        computeShader.SetBuffer(kernelHandle, "PositionBuffer", _positionBuffer);
        computeShader.SetBuffer(kernelHandle, "ColorBuffer", _colorBuffer);
        computeShader.SetBuffer(kernelHandle, "IndicesBuffer", _indicesBuffer);
        computeShader.SetBuffer(kernelHandle, "NormalBuffer", _normalBuffer);

        computeShader.Dispatch(kernelHandle, mainTxtSize / 16, mainTxtSize / 16, 1);
    }

    private void OnRenderObject()
    {
        material.SetPass(0);

        material.SetVector("_ObjectPosition", objectPosition);

        material.SetBuffer("_PositionBuffer", _positionBuffer);

        material.SetBuffer("_ColorBuffer", _colorBuffer);

        material.SetFloat("_Width", mainTxtSize);

        material.SetFloat("_TotalVertex", bufferSize);

        Graphics.DrawProceduralNow(MeshTopology.Points, bufferSize, 1);
    }

    private void OnApplicationQuit()
    {
        ResetData();
    }

    void ResetData() {
        _positionBuffer.Dispose();
        _colorBuffer.Dispose();
        _indicesBuffer.Dispose();
        _normalBuffer.Dispose();
    }
}
