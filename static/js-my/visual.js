queue()
    .defer(d3.csv, "static/data/vav.csv")    // views votes name
    .await(makeGraphs);

function makeGraphs(error, vavData) {
// buttons for view/votes
// 
    var views5 = vavData
            .map(function(d,i) {  return d; })                  //clone
            .sort(function(a,b) { return b.views - a.views;})
            .slice(0,5);
    var votes5 = vavData
            .map(function(d,i) {  return d; })                  //clone
            .sort(function(a,b) { return b.votes - a.votes;})
            .slice(0,5);
            
    console.log("vote5", votes5)
    console.log("view5", views5)
    drawbar(views5);
    
    var arcData = d3.nest()
                .key(function(d) { return d.vegan; })
                .rollup(function(v) { return v.length; })
                .entries(vavData);
    console.log("arcdata", arcData)           
    drawpie(arcData);
    
    
}

function drawbar(data){

    //extract name,views and votes 
    var views = [], rviews = [], votes = [], names = [];
    for (var i = 0; i < data.length; i++) {
        views.push(data[i]['views']);
        votes.push(data[i]['votes']);
        names.push(data[i]['name']);
    }
    console.log("views-",views);
    console.log("data-",data);
    var highest = Math.max.apply(this,views);
    
    var w = 600, wname = 300, h = 200;
    var barPadding = 1;
    var setLength = views.length;
    var rowHeight = 30;
    var ratio = (w-wname)/highest;
    for (var i = 0; i < setLength; i++) {
        rviews[i] = parseInt(ratio * views[i]);
        votes[i] = parseInt(ratio * votes[i]);
    }
    
    // bargraph area
    var svgbar = d3.select("#bar").append("svg")
        .attr("width", w)
        .attr("height", h);
        
    // views
    
    // enter data
    var bar1 =  svgbar.selectAll("rect")
        .data(rviews)                       // wont accept data - error is no length
        .enter()
        //.append("g")
        ;
    
    // draw each value    
    bar1.append("rect")
        .attr("y", function(d, i) {
            return i * rowHeight ;
        })
        .attr("x", function(d, i) {
            return w -wname - rviews[i];
        })
        .attr("height", rowHeight - barPadding)
        .attr("width", function(d) {
            return d;
        })
        .attr("fill", "green");
       
     // votes   
     /*
    var g2 = svgbar.selectAll("rect")
        .data(votes)
        .enter().append("g2");
        
        g2.append("rect")
        .attr("y", function(d, i) {
            return i * rowHeight + 250;
        })
        .attr("x", function(d) {
            return w -wname - d;
        })
        .attr("height", rowHeight - barPadding)
        .attr("width", function(d) {
            return d;
        })
        .style("fill", "blue");
        */
        
    // recipe names
    
    var text1 = svgbar.selectAll("text")
        .data(data)
        .enter()
        
    text1.append("text")
        .text(function(d) {
            return d.name;
        })
        .attr("text-anchor", "left")
        .attr("y", function(d, i) {
            return i * rowHeight + (rowHeight) / 2;
        })
        .attr("x",  w - wname + 20)
        .attr("font-family", "sans-serif")
        .attr("font-size", "13px")
        .attr("fill", "white");
        
     // recipe votes
     
    var text2 =svgbar.selectAll("text")
        .data(views)
        .enter()
        
    text1.append("text")
        .text(function(d) {
            return d.votes;
        })
        .attr("text-anchor", "left")
        .attr("y", function(d, i) {
            return i * rowHeight + (rowHeight) / 2;
        })
        .attr("x", function(d) {
            return w - wname - 20;
        })
        .attr("font-family", "sans-serif")
        .attr("font-size", "13px")
        .attr("fill", "white");
    
}