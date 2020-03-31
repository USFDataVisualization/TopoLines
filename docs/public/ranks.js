
        var datasets = {};
        var filter_list = [ "median", "gaussian", "cutoff", "subsample", "rdp", "tda" ]


        var metrics_data = null;
        var rank_data = null;

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
            func_entropy = function(d){ return d['metrics']['approx entropy']; };
            func_l1 = function(d){ return d['metrics']['L1 norm']; };
            func_linf = function(d){ return d['metrics']['L_inf norm']; };
            func_wasserstein = function(d){ return d['metrics']['peak wasserstein']; };
            func_bottleneck = function(d){ return d['metrics']['peak bottleneck']; };


            update_scatterplot( "#entropy_l1", dinput, func_entropy, func_l1, func_class, rank_data.filter( d => d['x']=='approx entropy' && d['y']=='L1 norm' )[0]['result'], active_filters );
            update_scatterplot( "#entropy_linf", dinput, func_entropy, func_linf, func_class, rank_data.filter( d => d['x']=='approx entropy' && d['y']=='L_inf norm' )[0]['result'], active_filters );
            update_scatterplot( "#entropy_wass", dinput, func_entropy, func_wasserstein, func_class, rank_data.filter( d => d['x']=='approx entropy' && d['y']=='peak wasserstein' )[0]['result'], active_filters );
            update_scatterplot( "#entropy_bott", dinput, func_entropy, func_bottleneck, func_class, rank_data.filter( d => d['x']=='approx entropy' && d['y']=='peak bottleneck' )[0]['result'], active_filters );


            update_ranking( "entropy_l1_rank",   rank_data.filter( d => d['x']=='approx entropy' && d['y']=='L1 norm' )[0]['result'] )
            update_ranking( "entropy_linf_rank", rank_data.filter( d => d['x']=='approx entropy' && d['y']=='L_inf norm' )[0]['result'] );
            update_ranking( "entropy_wass_rank", rank_data.filter( d => d['x']=='approx entropy' && d['y']=='peak wasserstein' )[0]['result'] );
            update_ranking( "entropy_bott_rank", rank_data.filter( d => d['x']=='approx entropy' && d['y']=='peak bottleneck' )[0]['result'] );


        }

        function reloadMetrics(){
            d3.json( "metric?" + $('#parameterForm').serialize(), function( dinput ) {
                metrics_data = dinput['metric'];
                rank_data = dinput['rank'];
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

        function changeFilter(){
            reloadMetrics();
        }

        function changeFilterLevel(){
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


        function update_ranking( doc_id, rank_data ){
            html = '<span class="ranktext" style="text-decoration: underline;"><underline>Ranking</underline></span><br>'
                    + '<span class="ranktext" style="color: darkgrey; font-size: small; ">Best</span><br>';

            keys = Object.keys(rank_data)
            keys.sort( (a,b) => rank_data[a]['rank'] - rank_data[b]['rank'] );
            keys.forEach( function(key) {
                val = rank_data[key];
                switch( key ){
                    case 'tda':       html += '<span class="rankbox tda_background"></span><span class="ranklabel">TopoLines</span><br>';     break;
                    case 'median':    html += '<span class="rankbox median_background"></span><span class="ranklabel">Median</span><br>';     break;
                    case 'gaussian':  html += '<span class="rankbox gaussian_background"></span><span class="ranklabel">Gaussian</span><br>'; break;
                    case 'cutoff':    html += '<span class="rankbox cutoff_background"></span><span class="ranklabel">Cutoff</span><br>';     break;
                    case 'subsample': html += '<span class="rankbox subsample_background"></span><span class="ranklabel">Uniform</span><br>'; break;
                    case 'rdp':       html += '<span class="rankbox rdp_background"></span><span class="ranklabel">Douglas-Peucker</span><br>'; break;
                }
            });

            html += '<span class="ranktext" style="color: darkgrey; font-size: small; ">Worst</span>';

            document.getElementById(doc_id).innerHTML = html;
        }
