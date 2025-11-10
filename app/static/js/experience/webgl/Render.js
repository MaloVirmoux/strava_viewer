import * as THREE from "three";
import { MapControls } from "three/examples/jsm/controls/MapControls.js";

import Tile from "./object/Tile";
import RenderPass from "./pass/RenderPass";
import Camera from "./setup/Camera";
import CanvaSize from "./setup/CanvaSize";
import Composer from "./setup/Composer";
import Renderer from "./setup/Renderer";
import Scene from "./setup/Scene";

/** Class used to create the render */
export default class Render {
    /**
     * Creates the render
     * @param {Element} container HTML Element to display the scene in
     */
    constructor(container) {
        this.container = container;

        this.canvaSize = new CanvaSize();
        this.scene = new Scene();
        this.camera = new Camera(this.canvaSize);
        this.camera.up.set(0, 0, 1);
        this.scene.add(this.camera);
        this.controls = new MapControls(this.camera, this.container);

        // Tmp lights
        const pointLight1 = new THREE.PointLight("#ff9000", 50),
            pointLight2 = new THREE.PointLight("#0090ff", 50),
            pointLight3 = new THREE.PointLight("#90ff90", 50);
        pointLight1.position.set(3, 2, 3);
        pointLight2.position.set(-3, 2, 3);
        pointLight3.position.set(0, -3, 3);
        this.scene.add(pointLight1, pointLight2, pointLight3);

        const pointLightHelper1 = new THREE.PointLightHelper(pointLight1, 1),
            pointLightHelper2 = new THREE.PointLightHelper(pointLight2, 1),
            pointLightHelper3 = new THREE.PointLightHelper(pointLight3, 1);
        this.scene.add(pointLightHelper1, pointLightHelper2, pointLightHelper3);

        const tile = new Tile();
        const axisHelper = new THREE.AxesHelper(3);
        this.scene.add(tile, axisHelper);

        this.renderer = new Renderer(this.canvaSize, this.container);
        this.composer = new Composer(this.canvaSize, this.renderer);
        this.renderPass = new RenderPass(this.scene, this.camera);
        this.composer.addPass(this.renderPass);

        this.createListener();
    }

    /** Creates the listeners to update the render */
    createListener() {
        window.addEventListener("resize", () => {
            this.canvaSize.update();
            this.camera.update(this.canvaSize);
            this.renderer.update(this.canvaSize);
            this.composer.update(this.canvaSize);
        });
    }

    /** Updates the render */
    update() {
        this.composer.render();
    }
}
