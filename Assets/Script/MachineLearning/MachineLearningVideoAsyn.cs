using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.Barracuda;
using System.Threading.Tasks;

public class MachineLearningVideoAsyn : MonoBehaviour
{
    public NNModel stupidModel;

    public RenderTexture targetTexture;

    public RenderTexture inputTexture;

    private Model nnModel;

    private CustomFixedUpdate FU_instance;

    private IWorker worker;
    private Tensor outputTensor;
    private Tensor inputTensor;

    private int i = 0;
    private int calculateStep = 40;
    private bool isProcessing = false;

    // Start is called before the first frame update
    void Start()
    {
        InitModel(stupidModel);
    }

    private void InitModel(NNModel onnxModel) {
        nnModel = ModelLoader.Load(onnxModel);
        worker = WorkerFactory.CreateWorker(WorkerFactory.Type.ComputePrecompiled, nnModel);
    }

    private void Update()
    {
        ExecuteModel(nnModel, inputTexture);
    }

    private void ExecuteModel(Model precomputeModel, RenderTexture inputTexture) {
        if (isProcessing) return;

        isProcessing = true;

        inputTensor = new Tensor(inputTexture, 3);

        StartCoroutine(Calculate((Tensor outputTensor) => {
            outputTensor.ToRenderTexture(targetTexture);

            isProcessing = false;
        }));
    }

    private IEnumerator Calculate(System.Action<Tensor> Callback) {

        using (inputTensor = new Tensor(inputTexture, 3)) {
            var enumerator = this.worker.ExecuteAsync(inputTensor);

            while (enumerator.MoveNext())
            {
                i++;
                if (i >= calculateStep)
                {
                    i = 0;
                    yield return null;
                }

            };
            var output = this.worker.PeekOutput();

            if (Callback != null)
                Callback(output);

        }
    }


    private void OnApplicationQuit()
    {
        worker.Dispose();
    }
}
