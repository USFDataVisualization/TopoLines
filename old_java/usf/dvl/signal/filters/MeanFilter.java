package usf.dvl.signal.filters;

import usf.dvl.signal.Signal;

public class MeanFilter extends FilteredSignal {

	public MeanFilter( Signal graph, int filterWidth ) {
		super(graph,filterWidth);

		for (int i = 0; i < graph.size(); i++) {
			float total = 0;
			int totalW = 0;
			for ( int j = 0; j < filterWidth; j++ ) {
				int idx = i+j-filterWidth/2;
				if ( idx >= 0 && idx < graph.size() ) {
					total += graph.get(idx);
					totalW++;
				}
			}
			addPoint( total / (float)totalW );
		}
	}

	@Override public String graphType( ) {
		return filterType();
	}
	
	public static String filterType( ) {
		return "Mean";
	}
	
}
