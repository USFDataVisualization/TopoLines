package usf.dvl.signal.filters;

import java.util.Arrays;

import processing.core.PApplet;
import usf.dvl.signal.Signal;

public class MedianFilter extends FilteredSignal {

	public MedianFilter( Signal graph, int filterWidth ) {
		super( graph, filterWidth );

		float [] vals = new float[filterWidth];
		for (int i = 0; i < graph.size(); i++) {
			for ( int j = 0; j < filterWidth; j++ ) {
				int idx = PApplet.constrain( i+j-filterWidth/2, 0, graph.size()-1 );
				vals[j] = graph.get(idx);
			}
			Arrays.sort( vals );
			addPoint( vals[filterWidth/2] );
		}
	}

	@Override public String graphType( ) {
		return filterType();
	}
	
	public static String filterType( ) {
		return "Median";
	}

}
