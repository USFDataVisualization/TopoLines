
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
    filt_name = dinput['info']['filter name'];

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
		  //.attr("class", "output_line")
		  .attr("class", filt_name+"_fig_filter")

		  .attr("d", d3.line()
			.x(function(d) { return xAxis(d[0]); })
			.y(function(d) { return yAxis(d[1]); })
			);
	
}





function add_linechart( chart_name, dinput, doutput, upper_left, width_height, css_class="output_line" ){

	var lc_svg = d3.select(chart_name);
	var lc_left = upper_left[0];
	var lc_top = upper_left[1];
	var lc_svg_width  = width_height[0];
	var lc_svg_height = width_height[1];

	var lc_margin = {left: 10, right: 0, top: 0, bottom: 15},
		lc_width  = lc_svg_width  - lc_margin.left - lc_margin.right,
		lc_height = lc_svg_height - lc_margin.top  - lc_margin.bottom;

	//xExt = [0,data.length-1];
	//yExt = d3.extent( data, function(d){ return d[1]; });
	xExt = [0,dinput.length-1];
	yExt = d3.extent( dinput, function(d){ return d[1]; });

	expand_range = (yExt[1]-yExt[0])*0.05;
	yExt[0] -= expand_range;
	yExt[1] += expand_range;

	data = doutput;

	var xAxis = d3.scaleLinear().domain( xExt ).range([ 0, lc_width ]);
	var yAxis = d3.scaleLinear().domain( yExt ).range([ lc_height, 0]);

    lc_svg.append("g")
        .attr("transform", "translate(" + (lc_left+lc_margin.left) + "," + (lc_top+lc_margin.top) + ")")
        .call(d3.axisLeft(yAxis).ticks(5).tickFormat(""));

    lc_svg.append("g")
            .attr("transform", "translate(" + (lc_left+lc_margin.left) + "," + (lc_top+lc_height+lc_margin.top) + ")")
            .call(d3.axisBottom(xAxis).ticks(10).tickFormat(""));

	lc_svg.append("path")
		.attr("transform", "translate(" + (lc_left+lc_margin.left) + "," + (lc_top+lc_margin.top) + ")")
		  .datum( data )
		  .attr("class", css_class)
		  .attr("d", d3.line()
			.x(function(d) { return xAxis(d[0]); })
			.y(function(d) { return yAxis(d[1]); })
			);

}




function special_round( val ){
    if( val < 0.05 ) return special_round( val*10 ) / 10;
    if( val < 0.1 ) return 0.1;
    if( val < 0.2 ) return 0.2;
    if( val < 0.5 ) return 0.5;
    if( val < 1.0 ) return 1.0;
    return special_round( val/10 ) * 10
}

function fix_range( range ){
    r0 = special_round(range/4)*4;
    r1 = special_round(range/5)*5;
    r2 = special_round(range/6)*6;
    return Math.min( r0, r1, r2 )*1.001;
}

function update_scatterplot( doc_id, data, func_x, func_y, func_class, rank_data=null, active_filters=null ){
    $(doc_id).empty();

    var sp_svg = d3.select(doc_id);
    var sp_svg_width  = +sp_svg.attr("width");
    var sp_svg_height = +sp_svg.attr("height");

    var sp_margin = {left: 45, right: 7, top: 5, bottom: 20},
        sp_width  = sp_svg_width  - sp_margin.left - sp_margin.right,
        sp_height = sp_svg_height - sp_margin.top  - sp_margin.bottom;


    var sp_xTmp = d3.extent( data, func_x );
    var sp_xExt = [ 0, Math.max(0,sp_xTmp[1]) ];
    //var sp_xExt = sp_xTmp;
    var sp_yTmp = d3.extent( data, func_y );
    var sp_yExt = [ 0, Math.max(0,sp_yTmp[1]) ];

    sp_yExt[1] = sp_yExt[0] + fix_range(sp_yExt[1]-sp_yExt[0]);

    var xAxis = d3.scaleLinear().domain( sp_xExt ).range([ 0, sp_width ]);
    var yAxis = d3.scaleLinear().domain( sp_yExt ).range([ sp_height, 0]);
    //var yAxis = d3.scaleLog().domain( sp_yExt ).range([ sp_height, 0]);

    if( (sp_yExt[1]-sp_yExt[0]) < 0.1 || (sp_yExt[1]-sp_yExt[0]) > 10000 ){
        sp_svg.append("g")
            .attr("transform", "translate(" + sp_margin.left + "," + sp_margin.top + ")")
            .call(d3.axisLeft(yAxis).ticks(5).tickFormat(d3.format(".1e")))
     }
     else{
        sp_svg.append("g")
            .attr("transform", "translate(" + sp_margin.left + "," + sp_margin.top + ")")
            .call(d3.axisLeft(yAxis).ticks(5));
     }

    sp_svg.append("g")
            .attr("transform", "translate(" + sp_margin.left + "," + (sp_height+sp_margin.top) + ")")
            .call(d3.axisBottom(xAxis).ticks(5));


    sp_svg.append('g')
        .attr("transform", "translate(" + sp_margin.left + "," + sp_margin.top + ")")
        .selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
          .attr("cx", function (d) { return xAxis( func_x(d) ); } )
          .attr("cy", function (d) { return yAxis( func_y(d) ); } )
          .attr("r", 2)
          .attr("class", function(d){ return func_class(d)+"_light"; } )

    if( rank_data != null && active_filters != null ){

        sp_svg.append("clipPath")       // define a clip path
                            .attr("id", "boxclip") // give the clipPath an ID
                            .append("rect")          // shape it as an ellipse
                                .attr("x", 0)         // position the x-centre
                                .attr("y", 0)         // position the y-centre
                                .attr("width", sp_width)         // set the x radius
                                .attr("height", sp_height);

        svg_grp = sp_svg.append("g")
                        .attr("transform", "translate(" + sp_margin.left + "," + sp_margin.top + ")");

        //Object.keys(rank_data).forEach( function(key) {
        active_filters.forEach( function(key) {
            val = rank_data[key];
            svg_grp.append("line")
                         .attr("clip-path", "url(#boxclip)")
                         .attr("x1", xAxis(val['points'][0][0]) )
                         .attr("y1", yAxis(val['points'][0][1]) )
                         .attr("x2", xAxis(val['points'][1][0]) )
                         .attr("y2", yAxis(val['points'][1][1]) )
                         .attr("class", key+"_filter regression");
        });
    }

}




function log_scatterplot( doc_id, data, func_x, func_y, func_class ){
    $(doc_id).empty();

    var sp_svg = d3.select(doc_id);
    var sp_svg_width  = +sp_svg.attr("width");
    var sp_svg_height = +sp_svg.attr("height");

    var sp_margin = {left: 45, right: 7, top: 5, bottom: 20},
        sp_width  = sp_svg_width  - sp_margin.left - sp_margin.right,
        sp_height = sp_svg_height - sp_margin.top  - sp_margin.bottom;


    var sp_xTmp = d3.extent( data, func_x );
    var sp_xExt = [ 0, Math.max(0,sp_xTmp[1]) ];
    var sp_yExt = d3.extent( data, func_y );

    //console.log( sp_yExt );
    sp_yExt[0] = Math.exp( ( Math.ceil( Math.log( sp_yExt[0] )/Math.log(10))-1 ) * Math.log(10) );
    sp_yExt[1] = Math.exp( ( Math.floor( Math.log( sp_yExt[1] )/Math.log(10) )+1 ) * Math.log(10) );

    //sp_yExt[1] = sp_yExt[0] + fix_range(sp_yExt[1]-sp_yExt[0]);

    var xAxis = d3.scaleLinear().domain( sp_xExt ).range([ 0, sp_width ]);
    var yAxis = d3.scaleLog().domain( sp_yExt ).range([ sp_height, 0]);

    sp_svg.append("g")
        .attr("transform", "translate(" + sp_margin.left + "," + sp_margin.top + ")")
        .call(d3.axisLeft(yAxis).ticks(4).tickFormat(d3.format(".1e")))

    sp_svg.append("g")
            .attr("transform", "translate(" + sp_margin.left + "," + (sp_height+sp_margin.top) + ")")
            .call(d3.axisBottom(xAxis).ticks(5));

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


}
