
var redraw, renderer;

function GraphWatchRender() {
    this.gr = new Graph();

    this.render = function(r, n) {
        /* the Raphael set is obligatory, containing all you want to display */
        var set = r.set().push(
            /* custom objects go here */
            r.rect(n.point[0], n.point[1], 86, 62)
            .attr({"fill": "#88ff88", "stroke-width": 1, r : "4px"}))
        .push(r.text(n.point[0], n.point[1], n.label)
              .attr({"font-size":"20px"}));
        /* custom tooltip attached to the set */
        //set.items.forEach(
        //    function(el) {
        //        el.tooltip(r.set().push(r.rect(0, 0, 30, 30)
        //                                .attr({"fill": "#fec", "stroke-width": 1, r : "9px"})))});
        return set;
    };

    var width = $(document).width() - 20;
    var height = $(document).height() - 60;

    this.renderer = new Graph.Renderer.Raphael('canvas', this.gr, width, height);
    this.addNode = function(data) {
        this.gr.addNode(data.name, {label: data.name,
                                    render: this.render });
        this.layouter.layout();
    };
        
    this.addEdge = function(from, to) {
        this.gr.addEdge(from, to);
    }

    this.redraw = function() {
        this.layouter.layout();
        this.renderer.draw();
    };
    this.hide = function(id) {
        this.gr.nodes[id].hide();
    };
    this.show = function(id) {
        this.gr.nodes[id].show();
    };

    this.layouter = new Graph.Layout.Spring(this.gr);
    this.addNode({name: "foo"});
    this.addNode({name: "bar"});
    
    this.addEdge("foo", "bar");

    this.redraw();
}
