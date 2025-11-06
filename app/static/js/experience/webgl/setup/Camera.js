import * as THREE from "three";
import CanvaSize from "./CanvaSize";

/** Class used to create the scene camera */
export default class Camera extends THREE.OrthographicCamera {
    /**
     * Creates the camera
     * @param {CanvaSize} size Size of the canva
     */
    constructor(size) {
        super(-size.ratio, size.ratio, 1, -1);
        this.position.set(0, 0, 3);
        this.lookAt(new THREE.Vector3(0, 0, 0));
        this.zoom = 0.5;

        this.updateProjectionMatrix();
    }

    /**
     * Updates the camera
     * @param {CanvaSize} size Size of the canva
     */
    update(size) {
        this.left = -size.ratio;
        this.right = size.ratio;
        this.updateProjectionMatrix();
    }
}
