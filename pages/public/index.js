

        var datasets = {};
        var filter_list = [ "median", "gaussian", "cutoff", "subsample", "rdp", "tda" ]


		function reloadChart(){
			d3.json( "data?" + $('#parameterForm').serialize(), function( dinput ) {

			    document.getElementById("approx_ent_value").innerHTML = dinput['metrics']['approx entropy'].toFixed(4);
			    document.getElementById("l1_norm_value").innerHTML = dinput['metrics']['L1 norm'].toFixed(4);
			    document.getElementById("linf_norm_value").innerHTML = dinput['metrics']['L_inf norm'].toFixed(4);
			    document.getElementById("wass_value").innerHTML = dinput['metrics']['peak wasserstein'].toFixed(4);
			    document.getElementById("bott_value").innerHTML = dinput['metrics']['peak bottleneck'].toFixed(4);

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


		d3.json( "datasets", function( dinput ) {
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



