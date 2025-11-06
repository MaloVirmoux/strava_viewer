import * as THREE from "three";

/**
 * Subdivises faces into smaller faces
 * @param {list} faces List of nine values, or list of list of nine values, each representing a face to subdivise
 * @param {int} n_divisions Number of division to process (/!\ Exponential)
 * @returns {list} List of values representing the faces
 */
export function subdiviseFaces(faces, n_divisions) {
    //          v1
    //          ⟋⟍
    //  edge3 ⟋    ⟍ edge1
    //      ⟋        ⟍
    // v3 ⟋_____________⟍ v2
    //         edge2
    if (typeof faces[0] === "number") {
        faces = [faces];
    }

    for (let division = 0; division < n_divisions; division++) {
        let newFaces = [];
        faces.forEach((face) => {
            const vertices = computeVertices(face);
            const edges = computeEdges(vertices);
            const [newVertex, longestEdge] = computeDivision(edges);
            newFaces.push(
                ...computeNewFaces(vertices, newVertex, edges, longestEdge)
            );
        });
        faces = newFaces;
    }
    return faces;
}

/**
 * Computes the vertices from the provided list of values
 * @param {list} face List of 9 floats representing a face ([v1.x, v1.y, v1.z, ...])
 * @returns {list} List of three THREE.Vector3 vertices
 */
function computeVertices(face) {
    const vertex1 = new THREE.Vector3(face[0], face[1], face[2]);
    const vertex2 = new THREE.Vector3(face[3], face[4], face[5]);
    const vertex3 = new THREE.Vector3(face[6], face[7], face[8]);
    return [vertex1, vertex2, vertex3];
}

/**
 * Computes the edges from the provided list of vertices
 * @param {list} vertices List of three THREE.Vector3 vertices
 * @returns {list} List of three THREE.Vector3 edges
 */
function computeEdges(vertices) {
    const edge1 = {
        fromVertex: vertices[0],
        toVertex: vertices[1],
        edge: new THREE.Vector3(
            vertices[1].x - vertices[0].x,
            vertices[1].y - vertices[0].y,
            vertices[1].z - vertices[0].z
        ),
    };
    const edge2 = {
        fromVertex: vertices[1],
        toVertex: vertices[2],
        edge: new THREE.Vector3(
            vertices[2].x - vertices[1].x,
            vertices[2].y - vertices[1].y,
            vertices[2].z - vertices[1].z
        ),
    };
    const edge3 = {
        fromVertex: vertices[2],
        toVertex: vertices[0],
        edge: new THREE.Vector3(
            vertices[0].x - vertices[2].x,
            vertices[0].y - vertices[2].y,
            vertices[0].z - vertices[2].z
        ),
    };
    return [edge1, edge2, edge3];
}

/**
 * Creates a vertex in the middle of the longest of the provided edges
 * @param {list} edges List of three THREE.Vector3 edges
 * @returns {list} Returns both the newly created vertex and the splitted edge
 */
function computeDivision(edges) {
    // const longestEdge = Math.max(
    //     ...[edges[0], edges[1], edges[2]].map((edge) => edge.edge.length())
    // );

    const longestEdge = edges.reduce(
        (edge, previous) =>
            edge.edge.length() > previous.edge.length() ? edge : previous,
        { edge: new THREE.Vector3(0, 0, 0) }
    );

    const newVertex = new THREE.Vector3(
        (longestEdge.fromVertex.x + longestEdge.toVertex.x) / 2,
        (longestEdge.fromVertex.y + longestEdge.toVertex.y) / 2,
        (longestEdge.fromVertex.z + longestEdge.toVertex.z) / 2
    );
    return [newVertex, longestEdge];
}

/**
 * Splits the face in two
 * @param {list} vertices List of three THREE.Vector3 vertices
 * @param {THREE.Vector3} newVertex Newly created vertex
 * @param {list} edges List of three THREE.Vector3 edges
 * @param {THREE.Vector3} longestEdge Splitted edge
 * @returns {list} List of values representing the splitted faces
 */
function computeNewFaces(vertices, newVertex, edges, longestEdge) {
    switch (longestEdge) {
        case edges[0]:
            return [
                createNewFace(newVertex, vertices[0], vertices[2]),
                createNewFace(vertices[1], newVertex, vertices[2]),
            ];
        case edges[1]:
            return [
                createNewFace(vertices[1], vertices[0], newVertex),
                createNewFace(newVertex, vertices[0], vertices[2]),
            ];
        case edges[2]:
            return [
                createNewFace(vertices[1], vertices[0], newVertex),
                createNewFace(vertices[1], newVertex, vertices[2]),
            ];
    }
}

/**
 * Creates a face from three vertex
 * @param {THREE.Vector3} vertex1 First vertex of the face
 * @param {THREE.Vector3} vertex2 Second vertex of the face
 * @param {THREE.Vector3} vertex3 Third vertex of the face
 * @returns {list} List of values representing a face
 */
function createNewFace(vertex1, vertex2, vertex3) {
    return [
        ...[vertex1.x, vertex1.y, vertex1.z],
        ...[vertex2.x, vertex2.y, vertex2.z],
        ...[vertex3.x, vertex3.y, vertex3.z],
    ];
}
