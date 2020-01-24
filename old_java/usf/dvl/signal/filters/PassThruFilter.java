package usf.dvl.signal.filters;

import usf.dvl.signal.Signal;

public class PassThruFilter extends FilteredSignal {

	public PassThruFilter( Signal graph, float interval ) {
		super( graph, interval );
		
		for(int i = 0; i < graph.countPoints(); i++ ) {
			addPoint( graph.get(i) );
		}
	}

	@Override public String graphType( ) {
		return filterType();
	}
	
	public static String filterType( ) {
		return "Original";
	}

}
