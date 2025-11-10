import Render from "./webgl/Render";

/** Class used to run the experience */
export default class Experience {
    /**
     * Creates the experience
     * @param {Element} container HTML Element to display the scene in
     */
    constructor(container) {
        this.container = container;
        this.render = new Render(this.container);
        this.tick();
    }

    /** Computes the next frame */
    tick() {
        this.render.update();
        window.requestAnimationFrame(() => this.tick());
    }
}
