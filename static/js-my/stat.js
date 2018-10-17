queue()
    .defer(d3.csv, "static/data/vv.csv")
    .await(makeGraphs);

function makeGraphs(error, vav) {
console.log(vav,"======gdv");

    var ndx = crossfilter(vav);
    vav.forEach(function(d){
        d.votes = parseInt(d.votes, 10);
        console.log(d.votes,"======votes");
    });
    vav.forEach(function(d){
        d.views = parseInt(d.views, 10);
        console.log(d.views,"======v");
    });
    
    //showSelector(ndx);
    showCuisinesPie(ndx);
    showVeganPie(ndx);
    showVotesBar(ndx);
   
    dc.renderAll();
}
function showSelector(ndx) { 
    var dim = ndx.dimension(dc.pluck('vegan')); 
    var group = dim.group(); 

    dc.selectMenu("#selector")
        .width(150)
        .dimension(dim) 
        .group(group)
        .title(function (d){
            return 'Vegan?: ' + d.key + " = " + d.value + " recipes";}); 
} //cuisine or vegan=region or pop,           dollar=views or votes 

function showVeganPie(ndx) {
    var dim = ndx.dimension(dc.pluck("vegan"));
    var group = dim.group();
        
    dc.pieChart('#vegan')
            .width(250)
            .height(200)
            .radius(90)
            .transitionDuration(1500)
            .dimension(dim)
            .group(group);
}

function showCuisinesPie(ndx) {
    var dim = ndx.dimension(dc.pluck("cuisine"));
    var group = dim.group();
        
    dc.pieChart('#pie')
            .width(250)
            .height(200)
            .radius(90)
            .transitionDuration(1500)
            .dimension(dim)
            .group(group);
}
function showVotesBar(ndx) {
    var dim = ndx.dimension(dc.pluck('cuisine'));
    
    function add_item(p, v) {
        p.count++;
        p.total += v.views;
        p.average = p.total / p.count;
        return p;
    }
    function remove_item(p, v) {
        p.count--;
        if(p.count == 0) {
            p.total = 0;
            p.average = 0;
        } else {
            p.total -= v.views;
            p.average = p.total / p.count;
        }
        return p;
    }
    function initialise() {
        return {count: 0, total: 0, average: 0};
    }

    var views = dim.group().reduce(add_item, remove_item, initialise);
    
    dc.barChart("#bar")
        .width(400)
        .height(300)
        .margins({top: 10, right: 50, bottom: 30, left: 50})
        .dimension(dim)
        .group(views)
        .valueAccessor(function(d){
             return d.value.total;
        })
        .transitionDuration(500)
        .x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .elasticY(true)
        .xAxisLabel("Cuisines")
        .yAxisLabel("views")
        .yAxis().ticks(5);
}
