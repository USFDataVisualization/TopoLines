package usf.dvl.signal.filters;

import processing.core.PApplet;
import usf.dvl.signal.Signal;

public class SubsampleFilter extends FilteredSignal {

	public SubsampleFilter( Signal graph, float interval ) {
		super( graph, interval );
		
		interval = Math.max(1, interval);

		float curPos = 0;
		float curVal = graph.interp(curPos);
		int i = 0;

		while ( i < graph.size() ) {
			float nexPos = curPos+interval;
			float nexVal = graph.interp(nexPos);
			while ( i < nexPos && i < graph.size() ) {
				addPoint( PApplet.map( i, curPos, nexPos, curVal, nexVal ) );
				i++;
			}
			curPos = nexPos;
			curVal = nexVal;
		}
	}

	@Override public String graphType( ) {
		return filterType();
	}
	
	public static String filterType( ) {
		return "Subsampling";
	}

}
