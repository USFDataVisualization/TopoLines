



function load_teaser(){


    var dsets = ['dataset=astro&datafile=astro_115_128', 'dataset=climate&datafile=climate_17-18',
                 'dataset=eeg&datafile=eeg_chan07', 'dataset=stock&datafile=stock_goog' ];
    var flevel = ['0.40','0.85'];

        function stringize( v ){
            if( v == 'nan' ) return 'NaN';
            return v.toFixed(3);
        }

	function load_dataset( i, j ){
            //console.log("data?" + dsets[i] + "&filter=tda&level=" + flevel[j]);
            d3.json( "data?" + dsets[i] + "&filter=tda&level=" + flevel[j], function( dinput ) {
                //console.log( dsets[i] );
                //console.log( dinput );
                if( j == 0 )
                    add_linechart( "#fig_teaser", dinput['input'], dinput['input'], [5+335*i,5+155*j], [320,153], "orig_fig_filter" );
                add_linechart( "#fig_teaser", dinput['input'], dinput['output'], [5+335*i,5+155*(j+1)], [320,153], "tda_fig_filter" );

                var teaser_svg = d3.select("#fig_teaser");
                var text_group = teaser_svg.append("g");
                if(i == 0 || i==1){
                     text_group.append("text")
                      .style("fill", "gray")
                      .style("font-size", "16px")
                      .attr("dy", ".35em")
                      .attr("font-family", "Arial")
                      .attr("text-anchor", "start")
                      .attr("transform", "translate("+ (5+335*i+15) +","+ (5+155*(j+1)+125) +")")
                      .text( "approx entropy: " + dinput['metrics']['approx entropy'].toFixed(3) );
                }
                if(i == 2 || i==3){
                     text_group.append("text")
                      .style("fill", "gray")
                      .style("font-size", "16px")
                      .attr("dy", ".35em")
                      .attr("font-family", "Arial")
                      .attr("text-anchor", "start")
                      .attr("transform", "translate("+ (5+335*i+166) +","+ (5+155*(j+1)+125) +")")
                      .text( "approx entropy: " + dinput['metrics']['approx entropy'].toFixed(3) );
                }


                    document.getElementById("teaser_approx_ent_value_" + i + "_" + j).innerHTML = stringize(dinput['metrics']['approx entropy']);
                    document.getElementById("teaser_l1_norm_value_" + i + "_" + j).innerHTML = stringize(dinput['metrics']['L1 norm']);
                    document.getElementById("teaser_linf_norm_value_" + i + "_" + j).innerHTML = stringize(dinput['metrics']['L_inf norm']);
                    document.getElementById("teaser_wass_value_" + i + "_" + j).innerHTML = stringize(dinput['metrics']['peak wasserstein']);
                    document.getElementById("teaser_bott_value_" + i + "_" + j).innerHTML = stringize(dinput['metrics']['peak bottleneck']);


            });

	}


	$('#fig_teaser').empty();

    for( i = 0; i < 4; i++ ){
        for( j = 0; j < 2; j++ ){
            load_dataset(i,j);
        }
    }

 }