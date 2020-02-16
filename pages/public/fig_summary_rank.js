

function build_instance( r, x, y, box_size ){
    ret = []
    Object.keys(r).forEach( function(k){
        ret.push({ 'class':k, 'x': x, 'y': y + r[k]['rank']*18, 'r': box_size })
    });
    return ret;
}

function find_links( inst0, inst1 ){
    res = []
    inst0.forEach( function(i0){
        i1 = inst1.find( function(t){
            return t.class == i0.class;
        });
        res.push( {'src':i0,'dst':i1} );
    });
    return res;
}

var lineGenerator = d3.line()
	.curve(d3.curveCardinal);

function make_path( start, end ){
    return lineGenerator([start,
                [start[0]+(end[0]-start[0])/3, start[1]+(end[1]-start[1])/8],
                [end[0]-(end[0]-start[0])/3, end[1]-(end[1]-start[1])/8],
                end]);
}

function filter_data( dinput, ds, metric ){
    data = dinput.filter( d => d.dataset==ds );
    sets = [];
    data.forEach( function(d){
        d.rank.forEach( function(r){
            sets.push( r );
        });
    });
    return sets.filter( function(a){ return a['y'] == metric } );
}




d3.json( "http://localhost:6500/all_ranks", function( dinput ) {
    datasets = ['astro','climate','eeg','stock'];
    metric_names = ["L1 norm", "L_inf norm", "peak wasserstein", "peak bottleneck"];
    filter_list = {'tda': 'TopoLines', 'cutoff': "Cutoff", 'gaussian': "Gaussian", 'median' : "Median", 'subsample': "Uniform", 'rdp': "Ramer-Douglas"};
    task_names = ['Average Case', 'Retrieve Value', 'Worst Case', '', 'Average Case', 'Find Extrema', 'Worst Case']

    instances = []
    curX = 35;
    curDS = 0;
    dinput.forEach( function(ds){
        curY = 52;
        metric_names.forEach( function(m){
            instances.push( build_instance( ds.rank[m], curX, curY, (ds['datafile']=='overall')?15:10 ) );
            curY += 125;
        });
        curX += 50
        if( (curDS%5)==4) curX -= 10;
        curDS++;
    });


    var svg = d3.select("#psets");


    links = [];
    for( i = 0; i < instances.length-4; i++ ){
        if( (i%20)>=16 ) continue;
        links = links.concat( find_links( instances[i], instances[i+4] ) );
    }

    svg.append("g").selectAll("path")
        .data(links)
        .enter().append("path")
        .attr( 'd', function(d){ return make_path( [d.src.x+15,d.src.y+7.5], [d.dst.x,d.dst.y+7.5] ); } )
        .attr("class", function(d){ return d.src.class + "_filter_light"; })
        .attr("fill", "none")
        .attr("stroke-width",10);

    var gtmp = svg.append("g");

    var curX = 39;
    var curI = 0
    dinput.forEach( function(d){
        gtmp.append("text")
          .style("fill", "black")
          .style("font-size", (d.datafile=='overall')?"17px":"14px" )
          .attr("dy", ".35em")
          .attr("font-family", "Arial")
          .attr("text-anchor", "start")
          .attr("transform", "translate("+ curX+",63) rotate(320)")
          .text(d.datafile);

          curX+=50;
          if( (curI%5)==4) curX-=10;
          curI++;
    });

    curY = 125;
    iter = 0;
    task_names.forEach( function(d){
        gtmp.append("text")
          .style("fill", "black")
          .style("font-size", ((iter%2)==1?"16px":"14px"))
          .attr("dy", ".35em")
          .attr("font-family", "Arial")
          .attr("text-anchor", "middle")
          .attr("transform", "translate("+((iter%2)==1?10:25) +","+ curY+") rotate(270)")
          .text(d);
        curY += 62.5;
        iter++;
    });

    gtmp.append("text")
      .style("fill", "gray")
      .style("font-size", "14px")
      .attr("dy", ".35em")
      .attr("font-family", "Arial")
      .attr("text-anchor", "middle")
      .attr("text-decoration", "underline")
      .attr("transform", "translate(992,123) rotate(90)")
      .text( 'rank' );

    curY = 78;
    for( j = 0; j < 3; j++ ){
        for( i = 1; i <= 6; i++ ){
            gtmp.append("text")
              .style("fill", "gray")
              .style("font-size", "12px")
              .attr("dy", ".35em")
              .attr("font-family", "Arial")
              .attr("text-anchor", "middle")
              .attr("transform", "translate(977,"+ curY+")")
              .text( i );
            curY += 18;
        }
        curY += 17;
    }


    last_inst = instances[instances.length - 1];
    for( i = 0; i < 6; i++ ){

        gtmp.append("text")
              .style("fill", "gray")
              .style("font-size", "14px")
              .attr("dy", ".35em")
              .attr("font-family", "Arial")
              .attr("text-anchor", "start")
              .attr("transform", "translate("+ (last_inst[i].x+19) +","+ (last_inst[i].y+8) +")")
              .text( filter_list[ last_inst[i].class ] );

    }


    instances.forEach( function(instance){
        svg.append("g").selectAll("rect")
            .data(instance)
            .enter().append("rect")
                        .attr("x", function(d){ return d.x+(15-d.r)/2; } )
                        .attr("y", function(d){ return d.y+(15-d.r)/2; } )
                        .attr("class", function(d){ return d.class + "_filter"; })
                        .attr("width", function(d){ return d.r; })
                        .attr("height", function(d){ return d.r; });
    });
});

