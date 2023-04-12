// Code based on example : https://embed.plnkr.co/i2eLwxweLJhuUgTuOS4x/

function generateIndiaViz( stat = 'confirmed' ) {

    var statText = ""
    if ( stat.substring(0, 5) == "delta") {
        statText = capitalizeFirstLetter(stat.substring(5,stat.length)) + " (delta)"
        } else {
        statText = capitalizeFirstLetter(stat)
        }

    var w = '100%';
    var h = '100%';
    var proj = d3.geo.mercator();
    var path = d3.geo.path().projection(proj);
    var t = proj.translate(); // the projection's default translation
    var s = proj.scale() // the projection's default scale

    var buckets = 9,
      colors = ["#ffffd9", "#edf8b1", "#c7e9b4", "#7fcdbb", "#41b6c4", "#1d91c0", "#225ea8", "#253494", "#081d58"]; // alternatively colorbrewer.YlGnBu[9]

    d3.select("#india-d3").selectAll('*').remove();

    var map = d3.select("#india-d3").append("svg:svg")
      .attr("width", w)
      .attr("height", h)
      //.call(d3.behavior.zoom().on("zoom", redraw))
      .call(initialize);

    var india = map.append("svg:g")
      .attr("id", "india");

    var div = d3.select("body").append("div")
      .attr("class", "tooltip")
      .style("opacity", 0);

    //d3.json("/app/data/states.json", function (json) {
    d3.json("/app/data/covid_geo_india.json", function (json) {

      var maxTotal = d3.max(json.features, function (d) {
            return d.properties[stat] });
      //return d.confirmed });

      console.log(maxTotal);


      var colorScale = d3.scale.quantile()
        .domain(d3.range(buckets).map(function (d) { return (d / buckets) * maxTotal }))
        .range(colors);

      var y = d3.scale.sqrt()
        .domain([0, maxTotal])
        .range([0,300]);

      var yAxis = d3.svg.axis()
          .scale(y)
          .tickValues(colorScale.domain())
          .orient("left");

      // create a tooltip
      var Tooltip = d3.select("#india-d3")
        .append("div")
        .style("opacity", 0)
        .attr("class", "tooltip")
        .style("background-color", "white")
        .style("border", "solid")
        .style("border-width", "2px")
        .style("border-radius", "5px")
        .style("padding", "5px")


       var mousemove = function(d,i) {
        Tooltip
        .html("<b style='color:#FF0000'>" + d.properties[stat].toLocaleString("en-US") + "</b> "+ stat +
                    "<br> cases in <b>" + d.id +"</b>" )
        .style("font-size", "12px")
        .style("left", (d3.mouse(this)[0]) + "px")
        .style("top", (d3.mouse(this)[1]+25) + "px")
        }
      var mouseover = function(d,i) {
        Tooltip
        .style("opacity", 1);
          d3.select(this).transition().duration(300)
            .style("opacity", 0.8)
            .style("stroke-width", 1.25);
          div.transition().duration(300)
            .style("opacity", 0);
        }

      var mouseleave = function(d) {
        Tooltip
        .style("opacity", 0);
          d3.select(this).transition().duration(300)
            .style("opacity", 0.65)
            .style("stroke-width", 0.6);
          div.transition().duration(300)
            .style("opacity", 0);
        }

      india.selectAll("path")
        .data(json.features)
        .enter().append("path")
        .attr("d", path)
        .style("fill", colors[0])
        .style("opacity", 0.65)
        .on("mouseover", mouseover)
        .on("mousemove", mousemove)
        .on("mouseleave", mouseleave)

/*
        .on('click', function (d, i) {
          d3.select(this).transition().duration(300).style("opacity", 0.8);
          div.transition().duration(300)
            .style("opacity", 1)
          div.text(capitalizeFirstLetter(stat) + ' : ' + d.properties[stat].toLocaleString("en-US"))
            .style("left", (d3.event.pageX) + "px")
            .style("top", (d3.event.pageY - 30) + "px");
        })

        .on('mouseleave', function (d, i) {
          d3.select(this).transition().duration(300)
            .style("opacity", 0.5);
          div.transition().duration(300)
            .style("opacity", 0);
        })
        .on('mouseenter', function (d, i) {
          d3.select(this).transition().duration(300)
            .style("opacity", 0.5);
          div.transition().duration(300)
            .style("opacity", 0);

        }) */
;

      india.selectAll("path").transition().duration(1000)
        .style("fill", function (d) { return colorScale(d.properties[stat]); });

      //Adding legend for our Choropleth
      var g = india.append("g")
                .attr("class", "key")
                .attr("transform", "translate(445, 305)")
                .call(yAxis);

            g.selectAll("rect")
                .data(colorScale.range().map(function(d, i) {
                    return {
                        y0: i ? y(colorScale.domain()[i - 1]) : y.range()[0],
                        y1: i < colorScale.domain().length ? y(colorScale.domain()[i]) : y.range()[1],
                        z: d
                    };
                }))
                .enter().append("rect")
                    .attr("width", 7)
                    .attr("y", function(d) { return d.y0; })
                    .attr("height", function(d) { return d.y1 - d.y0; })
                    .style("fill", function(d) { return d.z; });

      india.append("g")
            .append("text")
            .attr("x", 650)
            .attr("y", 60)
            .attr("font-weight-bold", 700 )
            .attr("font-family", "Nunito")
            .style('fill','#4e73df')
            .style('stroke','none')
            .style("font-size", "28px")
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text( statText + " cases in India" );


    });

    function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
    }

    function initialize() {
      proj.scale(6700);
      proj.translate([-1240, 720]);
    }
    }

    generateIndiaViz() // Initial load (default : 'confirmed')