using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.Barracuda;

public class MachineLearningTest : MonoBehaviour
{
    public NNModel stupidModel;

    public RenderTexture targetTexture;

    public RenderTexture inputTexture;

    public Texture texture;

    private Model nnModel;

    // Start is called before the first frame update
    void Start()
    {
        InitModel(stupidModel);

        Debug.Log(nnModel.layers[0].weights.Length);
        
        foreach (var input in nnModel.inputs)
        {
            Debug.Log(input.name);
        }

        foreach (var output in nnModel.outputs)
        {
            Debug.Log(output);
        }

        ExecuteModel(nnModel, inputTexture);
    }

    private void InitModel(NNModel onnxModel) {
        nnModel = ModelLoader.Load(onnxModel);

        PrepareInput(texture, inputTexture);
    }

    private void ExecuteModel(Model precomputeModel, RenderTexture inputTexture) {
        IWorker worker = WorkerFactory.CreateWorker(WorkerFactory.Type.ComputePrecompiled, precomputeModel, true);
        var textures = new[] { inputTexture }; // these textures will form a batch
        var tensor = new Tensor(textures, 3);
        print(tensor.shape);

        worker.Execute(tensor);

        var outputTensor = worker.PeekOutput();
        print(outputTensor.shape);
        outputTensor.ToRenderTexture(targetTexture);
    }

    private RenderTexture PrepareInput(Texture texture, RenderTexture targetRenderer) {
        Graphics.Blit(texture, targetRenderer);

        return targetRenderer;
    }
}
