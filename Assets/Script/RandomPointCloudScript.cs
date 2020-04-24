using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[ExecuteInEditMode]
public class RandomPointCloudScript : MonoBehaviour
{
    [SerializeField]
    bool isUpdate;

    [SerializeField]
    int generateNum = 0;

    [SerializeField]
    private MeshFilter meshFilter;

    private Mesh mesh;

    [SerializeField]
    private float startPosition;

    [SerializeField]
    private float grassOffset;

    public int seed;
    public Vector2 size;

    List<Vector3> positions;
    int[] indicies;
    Color[] colors;    

    void Update()
    {
        if (isUpdate) {
            Random.InitState(seed);

            positions = new List<Vector3>(generateNum);
            indicies = new int[generateNum];
            colors = new Color[generateNum];

            for (int i = 0; i < generateNum; i++)
            {

                Vector3 origin = transform.position;
                origin.y = startPosition;
                origin.x += size.x * Random.Range(-0.5f, 0.5f);
                origin.z += size.y * Random.Range(-0.5f, 0.5f);

                Ray ray = new Ray(origin, Vector3.down);
                RaycastHit hit;

                if (Physics.Raycast(ray, out hit))
                {
                    origin = hit.point;
                    origin.y += grassOffset;

                    positions.Add(origin);
                    indicies[i] = i;
                    colors[i] = new Color(Random.Range(0, 1f), Random.Range(0, 1f), Random.Range(0, 1f), 1);
                }
            }

            mesh = new Mesh();

            mesh.SetVertices(positions);
            mesh.SetIndices(indicies, MeshTopology.Points, 0);
            mesh.SetColors(colors);

            meshFilter.mesh = mesh;


            isUpdate = false;
        }
    }
}
