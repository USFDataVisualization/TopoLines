


function load_filters_fig(){


    var dset = 'dataset=climate&datafile=climate_17-18';

    // approx entropy 0.49
    var filter_list = [{'cutoff': '0.62', 'gaussian': '0.04', 'median' : '0.545', 'subsample': '0.5', 'rdp': '0.455'},
    // approx entropy 0.195
                        {'cutoff': '0.885', 'gaussian': '0.4', 'median' : '0.81', 'subsample': '0.88', 'rdp': '0.72'} ];

    var filter_keys = ['median', 'gaussian', 'cutoff', 'subsample', 'rdp'];

	function load_dataset( i, j ){
            d3.json( "data?" + dset + "&filter=" + filter_keys[j] + "&level=" + filter_list[i][filter_keys[j]], function( dinput ) {
                //console.log(filter_keys[j] + "_fig_filter");
                add_linechart( "#fig_fitlers", dinput['input'], dinput['output'], [5+335*j,5+165*i], [320,155], filter_keys[j] + "_fig_filter"  );
            });

	}


	$('#fig_fitlers').empty();


    for( i = 0; i < filter_list.length; i++ ){
        for( j = 0; j < filter_keys.length; j++ ){
            load_dataset(i,j);
        }
    }

 }
