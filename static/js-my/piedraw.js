function drawpie(data){

// values to display
var sliceLabel = "key";
var sliceColor = "key";
var arcSize = "values";

// piechart dimensions and colors
var c = ["#33ccff","#aaff00","#ffff33","#81e4c2","#cc9966","#cc99ff","#ffcccc","#33cc33"];

var w = 600, h= 300,
      radius = Math.min(w,h)/2.5,
      color = d3.scale.ordinal().range(c),
      arc = d3.svg.arc().outerRadius(radius-10).innerRadius(50),
      pie = d3.layout.pie()
               .sort(null)
               .value(function(d){return d[arcSize]});
               
var svgpie = d3.select("#pie").append("svg")
               .attr("width", w)
               .attr("height", h)
               .append("g")
               .attr("transform","translate("+w/3+","+h/2+")");

// draw piechart   
var gp = svgpie.selectAll(".arc")       
            .data(pie(data))
            .enter()
            .append("g")
            .attr("class","arc");
    
gp.append("path")
      .attr("d", arc)
      .style("fill", function(d,i){ return color(d.data[sliceColor]); });
   
gp.append("text")
      .attr("transform",function(d){ return "translate("+arc.centroid(d)+")"; })
      .attr("dy", "0.35em")
      .style("text-anchor", "middle")
      .text(function(d,i){ return d.data[arcSize]; });
      
// draw legend
var legend = svgpie.selectAll('rect')
            .data(data)
            .enter().append('g')
            .attr("transform","translate("+w/3+","+(-h/3)+")")
            .append('g')
            .attr("class", "rect")
            .attr("transform", function (d, i) {{return "translate(0," + i * 20 + ")"}
        })
        
legend.append('rect')
            .attr("x", 0)
            .attr("y", 0)
            .attr("width", 10)
            .attr("height", 10)
            .style("fill", function (d, i) {return color(d[sliceColor])})
        
legend.append('text')
            .attr("x", 20)
            .attr("y", 10)
            //.attr("dy", ".35em")
            .text(function (d, i) {return d[sliceLabel] })
            .attr("class", "textselected")
            .style("text-anchor", "start")
            .style("font-size", 15)
   
}