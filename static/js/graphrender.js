
var redraw, renderer;

function graphrender() {
    this.gr = new Graph();

    var width = $(document).width() - 20;
    var height = $(document).height() - 60;

    this.gr.addNode("foo");
    this.gr.addNode("bar");
    
    this.gr.addEdge("foo", "bar");
    this.layouter = new Graph.Layout.Spring(this.gr);
    this.renderer = new Graph.Renderer.Raphael('canvas', this.gr, width, height);

    this.addNode = function(data) {
        this.gr.addNode(data.name);
        this.layouter.layout();
        this.renderer.draw();
    };
        
    this.redraw = function() {
        this.layouter.layout();
        this.renderer.draw();
    };
    this.hide = function(id) {
        this.g.nodes[id].hide();
    };
    this.show = function(id) {
        this.g.nodes[id].show();
    };

}
