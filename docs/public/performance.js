

        var datasets = {};
        var filter_list = [ "median", "gaussian", "cutoff", "subsample", "rdp", "tda" ]
        var metrics_data = null;


        function updateMetrics(){
			var active_filters = filter_list.filter( function(f){
			    return document.getElementById("metric_"+f).checked;
			});

            dinput = metrics_data.filter( function(d){
                return active_filters.includes(d['info']['filter name']);
            });

            func_class = function(d){ return d['info']['filter name'] + "_filter"; };
            func_level = function(d){ return d['info']['filter level']; };
            func_time = function(d){ return d['info']['processing time']; };

            log_scatterplot( "#info_perf",   dinput, func_level, func_time, func_class );
        }


        function reloadMetrics(){
            d3.json( "metric?" + $('#parameterForm').serialize(), function( dinput ) {
                metrics_data = dinput['metric'];
                updateMetrics();
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
            reloadMetrics();
        }


        function changeDatafile(){
            reloadMetrics();
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
