


function load_filters_fig(){


    var dset = 'dataset=climate&datafile=climate_17-18';

    // approx entropy 0.49
    var filter_list = [{'cutoff': '0.625', 'gaussian': '0.041', 'median' : '0.545', 'subsample': '0.5', 'rdp': '0.465'},
    // approx entropy 0.195
                        {'cutoff': '0.882', 'gaussian': '0.4', 'median' : '0.81', 'subsample': '0.88', 'rdp': '0.72'} ];

    var filter_keys = ['median', 'gaussian', 'cutoff', 'subsample', 'rdp'];

	function load_dataset( i, j ){
            d3.json( "data?" + dset + "&filter=" + filter_keys[j] + "&level=" + filter_list[i][filter_keys[j]], function( dinput ) {
                //console.log(filter_keys[j] + "_fig_filter");
                add_linechart( "#fig_fitlers", dinput['input'], dinput['output'], [5+335*j,5+155*i], [320,153], filter_keys[j] + "_fig_filter"  );

                var teaser_svg = d3.select("#fig_fitlers");
                var text_group = teaser_svg.append("g");

                 text_group.append("text")
                  .style("fill", "gray")
                  .style("font-size", "18px")
                  .attr("dy", ".35em")
                  .attr("font-family", "Arial")
                  .attr("text-anchor", "start")
                  .attr("transform", "translate("+ (5+335*j+15) +","+ (5+155*i+123) +")")
                  .text( "approx entropy: " + dinput['metrics']['approx entropy'].toFixed(3) );


                    document.getElementById("filter_approx_ent_value_" + j + "_" + i).innerHTML = dinput['metrics']['approx entropy'].toFixed(3);
                    document.getElementById("filter_l1_norm_value_" + j + "_" + i).innerHTML = dinput['metrics']['L1 norm'].toFixed(3);
                    document.getElementById("filter_linf_norm_value_" + j + "_" + i).innerHTML = dinput['metrics']['L_inf norm'].toFixed(3);
                    document.getElementById("filter_wass_value_" + j + "_" + i).innerHTML = dinput['metrics']['peak wasserstein'].toFixed(3);
                    document.getElementById("filter_bott_value_" + j + "_" + i).innerHTML = dinput['metrics']['peak bottleneck'].toFixed(3);

            });

	}


	$('#fig_fitlers').empty();


    for( i = 0; i < filter_list.length; i++ ){
        for( j = 0; j < filter_keys.length; j++ ){
            load_dataset(i,j);
        }
    }

 }
