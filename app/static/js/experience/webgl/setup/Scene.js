import * as THREE from "three";
import { params } from "../../params";

/** Class used to create the scene */
export default class Scene extends THREE.Scene {
    /** Creates the scene */
    constructor() {
        super();
        this.background = new THREE.Color(params.setup.scene.background);
    }
}
