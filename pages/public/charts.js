
function update_linechart( chart_name, dinput ){
	
	$(chart_name).empty();
	
	var lc_svg = d3.select(chart_name);
	var lc_svg_width  = +lc_svg.attr("width");
	var lc_svg_height = +lc_svg.attr("height");

	var lc_margin = {left: 10, right: 15, top: 10, bottom: 15},
		lc_width  = lc_svg_width  - lc_margin.left - lc_margin.right,
		lc_height = lc_svg_height - lc_margin.top  - lc_margin.bottom;

	orig_data = dinput['input'];
	filt_data = dinput['output'];

	xExt = [0,orig_data.length-1];
	yExt = d3.extent( orig_data, function(d){ return d[1]; });

	var xAxis = d3.scaleLinear().domain( xExt ).range([ 0, lc_width ]);
	var yAxis = d3.scaleLinear().domain( yExt ).range([ lc_height, 0]);

	lc_svg.append("path")
		.attr("transform", "translate(" + lc_margin.left + "," + lc_margin.top + ")")
		  .datum( orig_data )
		  .attr("class", "input_line")
		  .attr("d", d3.line()
			.x(function(d) { return xAxis(d[0]); })
			.y(function(d) { return yAxis(d[1]); })
			);

	lc_svg.append("path")
		.attr("transform", "translate(" + lc_margin.left + "," + lc_margin.top + ")")
		  .datum( filt_data )
		  .attr("class", "output_line")
		  .attr("d", d3.line()
			.x(function(d) { return xAxis(d[0]); })
			.y(function(d) { return yAxis(d[1]); })
			);
	
}




function update_scatterplot( doc_id, data, func_x, func_y, func_class ){
    $(doc_id).empty();

    var sp_svg = d3.select(doc_id);
    var sp_svg_width  = +sp_svg.attr("width");
    var sp_svg_height = +sp_svg.attr("height");

    var sp_margin = {left: 45, right: 15, top: 20, bottom: 15},
        sp_width  = sp_svg_width  - sp_margin.left - sp_margin.right,
        sp_height = sp_svg_height - sp_margin.top  - sp_margin.bottom;

    /*
    data = dinput.map( function(d){
        return [ d[d0[0]][d0[1]], d[d1[0]][d1[1]], d['info']['filter name'] ];
    });
    */

    var sp_xTmp = d3.extent( data, func_x );
    var sp_xExt = [ Math.min(0,sp_xTmp[0]), Math.max(0,sp_xTmp[1]) ];
    var sp_yTmp = d3.extent( data, func_y );
    var sp_yExt = [ Math.min(0,sp_yTmp[0]), Math.max(0,sp_yTmp[1]) ];

    var xAxis = d3.scaleLinear().domain( sp_xExt ).range([ 0, sp_width ]);
    var yAxis = d3.scaleLinear().domain( sp_yExt ).range([ sp_height, 0]);

    if( (sp_yExt[1]-sp_yExt[0]) < 0.1 || (sp_yExt[1]-sp_yExt[0]) > 100 ){
        sp_svg.append("g")
            .attr("transform", "translate(" + sp_margin.left + "," + sp_margin.top + ")")
            .call(d3.axisLeft(yAxis).ticks(5).tickFormat(d3.format(".1e")))
     }
     else{
        sp_svg.append("g")
            .attr("transform", "translate(" + sp_margin.left + "," + sp_margin.top + ")")
            .call(d3.axisLeft(yAxis).ticks(5));
     }

    sp_svg.append('g')
        .attr("transform", "translate(" + sp_margin.left + "," + sp_margin.top + ")")
        .selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
          .attr("cx", function (d) { return xAxis( func_x(d) ); } )
          .attr("cy", function (d) { return yAxis( func_y(d) ); } )
          .attr("r", 2)
          .attr("class", function(d){ return func_class(d); } )
/*
    sp_svg.append('text')
            .attr('x',sp_svg_width/2)
            .attr('y', 13)
            .attr('text-anchor','middle')
            .text(d0[0]+":"+d0[1]+", " +d1[0]+":"+d1[1]);*/
}


