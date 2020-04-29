using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.Barracuda;

public class MachineLearningTest : MonoBehaviour
{
    public NNModel stupidModel;

    public RenderTexture emptyTexture;

    private Model nnModel;

    // Start is called before the first frame update
    void Start()
    {
        InitModel(stupidModel);

        ExecuteModel(nnModel, emptyTexture);
    }

    private void InitModel(NNModel onnxModel) {
        nnModel = ModelLoader.Load(onnxModel);
        emptyTexture = PrepareInput(12, 12 , 8);
    }

    private void ExecuteModel(Model precomputeModel, RenderTexture inputTexture) {
        IWorker worker = WorkerFactory.CreateWorker(WorkerFactory.Type.ComputePrecompiled, precomputeModel);
        var tensor = new Tensor(inputTexture, 1);

        worker.Execute(tensor);

        var outputTensor = worker.PeekOutput();
        Debug.Log(outputTensor[0]);
    }

    private RenderTexture PrepareInput(int width, int height, int depth) {
        RenderTexture renderTexture = new RenderTexture(width, height, depth);
        renderTexture.enableRandomWrite = true;
        renderTexture.Create();

        return renderTexture;
    }
}
