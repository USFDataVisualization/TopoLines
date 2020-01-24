package usf.dvl.signal.filters;

import java.util.ArrayList;
import java.util.Comparator;

import processing.core.PApplet;
import processing.core.PVector;
import usf.dvl.signal.Signal;

public class DouglasPeuckerFilter extends FilteredSignal {

	public DouglasPeuckerFilter( Signal _orig_graph, float _simpl_level ) {
		super( _orig_graph, _simpl_level );

		
		ArrayList<PVector> pnts = new ArrayList<PVector>();
		pnts.add( new PVector(0,_orig_graph.get(0)) );
		pnts.add( new PVector(_orig_graph.size()-1,_orig_graph.get( _orig_graph.size()-1 ) ) );
		
		Comparator<PVector> cmp = new Comparator<PVector>() {
				@Override public int compare(PVector o1, PVector o2) {
					if( o1.x < o2.x ) return -1;
					if( o1.x > o2.x ) return  1;
					return 0;
				}
			};
		
			
			//int cnt = 0;
		float maxErr = 0;
		do {
			maxErr = 0;
			int sel = -1;
			
			int curP = 0;
			for( int i = 0; i < _orig_graph.size(); i++ ) {
				if( pnts.get(curP+1).x < i ) curP++;
				
				float yp = PApplet.map( i, pnts.get(curP).x, pnts.get(curP+1).x, pnts.get(curP).y, pnts.get(curP+1).y );
				float curErr = Math.abs( yp - _orig_graph.get(i) );
				
				if( curErr > maxErr ) {
					sel = i;
					maxErr = curErr;
				}
				
			}
			//System.out.println( sel +" " + maxErr + " " + _simpl_level );
			
			if( maxErr <= _simpl_level || sel == -1 ) break;
			
			pnts.add( new PVector( sel, _orig_graph.get(sel) ) );
			pnts.sort( cmp );
			
			//if( cnt++ > 100 ) break;
		
		} while( maxErr > _simpl_level );
		
		int curP = 0;
		for( int i = 0; i < _orig_graph.size(); i++ ) {
			if( pnts.get(curP+1).x < i ) curP++;
			
			float yp = PApplet.map( i, pnts.get(curP).x, pnts.get(curP+1).x, pnts.get(curP).y, pnts.get(curP+1).y );
			
			addPoint( yp );
		}
		
	}
	
	public static String filterType( ) {
		return "Douglas-Peucker";
	}
	
	

}
