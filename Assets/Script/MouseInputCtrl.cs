using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MouseInputCtrl : MonoBehaviour
{

    [SerializeField]
    Material mouseMaterial;

    Vector2 screenSize;

    // Start is called before the first frame update
    void Start()
    {
        screenSize = new Vector2(Screen.width, Screen.height);

        Debug.Log(screenSize);
    }

    // Update is called once per frame
    void Update()
    {
        Vector3 normalizedVector = NormalizeMousePos(Input.mousePosition);

        if (mouseMaterial != null)
            mouseMaterial.SetVector("_MousePosition", normalizedVector);
    }

    Vector3 NormalizeMousePos(Vector3 rawMousePos) {

        Vector3 normalizeVector = rawMousePos;
        normalizeVector.Set( -0.5f + (normalizeVector.x / screenSize.x),
                            -0.5f +  (normalizeVector.y / screenSize.y), 0);

        normalizeVector *= 0.15f;

        return normalizeVector;
    }

}
