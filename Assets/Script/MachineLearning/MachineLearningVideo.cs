using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.Barracuda;
using System.Threading.Tasks;

public class MachineLearningVideo : MonoBehaviour
{
    public NNModel stupidModel;

    public RenderTexture targetTexture;

    public RenderTexture inputTexture;

    private Model nnModel;

    private CustomFixedUpdate FU_instance;

    private IWorker worker;
    private Tensor outputTensor;

    // Start is called before the first frame update
    void Start()
    {
        FU_instance = new CustomFixedUpdate(0.1f, OnFixedUpdate);
        InitModel(stupidModel);
    }

    private void InitModel(NNModel onnxModel) {
        nnModel = ModelLoader.Load(onnxModel);
        worker = WorkerFactory.CreateWorker(WorkerFactory.Type.ComputePrecompiled, nnModel);
    }

    private void Update()
    {
        FU_instance.Update();
        //ExecuteModel(nnModel, inputTexture);
    }


    // this method will be called 10 times per second
    void OnFixedUpdate(float dt)
    {
        ExecuteModel(nnModel, inputTexture);
    }

    private void ExecuteModel(Model precomputeModel, RenderTexture inputTexture) {
        var tensor = new Tensor(inputTexture, 3);

        worker.Execute(tensor);
        worker.ExecuteAsync();
        outputTensor = worker.PeekOutput();

        outputTensor.ToRenderTexture(targetTexture);

        tensor.Dispose();
        outputTensor.Dispose();
    }


    private void OnApplicationQuit()
    {
        worker.Dispose();
    }
}
