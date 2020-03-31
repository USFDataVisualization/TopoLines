

        var datasets = {};
        var filter_list = [ "median", "gaussian", "cutoff", "subsample", "rdp", "tda" ]

        function stringize( v ){
            if( v == 'nan' ) return 'NaN';
            return v.toFixed(4);
        }

		function reloadChart(){

            let e = document.getElementById("dataset");
            let ds = e.options[e.selectedIndex].value;
            let f = document.getElementById("datafile");
            let df = f.options[f.selectedIndex].value;
            let g = document.getElementById("level");
            let level = g.value*100;
            let h = document.getElementById("filter");
            let filter = h.options[h.selectedIndex].value;

		    //console.log("data?" + $('#parameterForm').serialize() );
		    let file = "json/results/" + ds + "/" + df + "/" + filter + "/level" + level + ".json";
		    console.log(file);
		    d3.json( file, function( dinput ) {
			//d3.json( "data?" + $('#parameterForm').serialize(), function( dinput ) {

                console.log( dinput );
			    document.getElementById("approx_ent_value").innerHTML = stringize(dinput['metrics']['approx entropy']);
			    document.getElementById("l1_norm_value").innerHTML = stringize(dinput['metrics']['L1 norm']);
			    document.getElementById("linf_norm_value").innerHTML = stringize(dinput['metrics']['L_inf norm']);
			    document.getElementById("wass_value").innerHTML = stringize(dinput['metrics']['peak wasserstein']);
			    document.getElementById("bott_value").innerHTML = stringize(dinput['metrics']['peak bottleneck']);

                update_linechart( "#linechart", dinput );
			});
		}


        function changeDataset(){
            var e = document.getElementById("dataset");
            var dset = e.options[e.selectedIndex].value;
            datasets[dset].sort();
            html = "";
            datasets[dset].forEach( function(d){
		        html += '<option value="'+d+'">'+d+'</option>';
            });
            document.getElementById("datafile").innerHTML = html;
            reloadChart();
        }

        function changeDatafile(){
            reloadChart();
        }

        function changeFilter(){
            reloadChart();
        }

        function changeFilterLevel(){
            reloadChart();
        }


		d3.json( "json/datasets.json", function( dinput ) {
            datasets = dinput;

            html = "";
            keys = Object.keys(datasets);
            keys.sort();

		    keys.forEach( function(d){
		        html += '<option value="'+d+'">'+d+'</option>';
		    });

            document.getElementById("dataset").innerHTML = html;

            changeDataset();
		});



