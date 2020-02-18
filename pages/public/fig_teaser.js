



function load_teaser(){


    var dsets = ['dataset=astro&datafile=astro_115_128', 'dataset=climate&datafile=climate_17-18',
                 'dataset=eeg&datafile=eeg_chan07', 'dataset=stock&datafile=stock_goog' ];
    var flevel = ['0.40','0.85'];


	function load_dataset( i, j ){
            //console.log("data?" + dsets[i] + "&filter=tda&level=" + flevel[j]);
            d3.json( "data?" + dsets[i] + "&filter=tda&level=" + flevel[j], function( dinput ) {
                console.log( dsets[i] );
                console.log( dinput );
                if( j == 0 )
                    add_linechart( "#fig_teaser", dinput['input'], dinput['input'], [5+335*i,5+165*j], [320,155], "orig_fig_filter" );
                add_linechart( "#fig_teaser", dinput['input'], dinput['output'], [5+335*i,5+165*(j+1)], [320,155], "tda_fig_filter" );
            });

	}


	$('#fig_teaser').empty();

    for( i = 0; i < 4; i++ ){
        for( j = 0; j < 2; j++ ){
            load_dataset(i,j);
        }
    }

 }