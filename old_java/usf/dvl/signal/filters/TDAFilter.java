package usf.dvl.signal.filters;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

import processing.core.PVector;
import usf.dvl.signal.Signal;
import usf.dvl.signal.SignalDerivative;
import usf.dvl.signal.SignalIntegral;
import usf.saav.topology.TopoGraph;
import usf.saav.topology.TopoGraph.Vertex;
import usf.saav.topology.merge.serial.JoinTree;
import usf.saav.topology.merge.serial.MergeTreeNode;


public class TDAFilter extends FilteredSignal {

	float smallestDerivative = 0.00001f;


	
	public TopoGraph<Point> topo = new TopoGraph<Point>();
	public JoinTree tt;
	public ArrayList<PVector> points = new ArrayList<PVector>();
	
	
	public TDAFilter( Signal t, float simplification_threshold ){
		super( t, simplification_threshold );

		topo.add( new Point(0,0) );
		for( int i = 1; i < t.size(); i++) {
			if( topo.get(topo.size()-1).value() == t.getPoint(i) ) 
				topo.get(topo.size()-1).expand(i);
			else
				topo.add( new Point(topo.size(),i) );
		}

		tt = new JoinTree(topo);
		tt.run();


		points.add( new PVector(0,t.get(0)) );
		points.add( new PVector(t.size()-1,t.get(t.size()-1)) );

		for(int i = 0; i < tt.size(); i++){
			MergeTreeNode curr = tt.getNode(i);
			if( tt.getNode(i).getPersistence() > simplification_threshold ) {
				Point pnt = topo.get( curr.getID() );
				points.add(  new PVector( pnt.position(), pnt.value() ) );
			}
		}

		Collections.sort( points, new Comparator<PVector>() {
			@Override public int compare( PVector p0, PVector p1 ){
				if( p0.x < p1.x ) return -1;
				if( p0.x > p1.x ) return  1;
				return 0;
			}
		});
		
		
		SignalDerivative derv = new SignalDerivative( t );
		for( int i = 0; i < points.size()-1; i++ ) {
			PVector p0 = points.get(i);
			PVector p1 = points.get(i+1);
			boolean up = p0.y < p1.y;

			float fwdProp = 0;
			float bckProp = 0;
			for( int cx = (int)p0.x; cx < p1.x; cx++ ) {
				if( up && derv.get(cx)<0 ) { 
					bckProp += (derv.get(cx)-smallestDerivative)/2;
					fwdProp += (derv.get(cx)-smallestDerivative)/2;
					derv.set(cx, +smallestDerivative); 
					bckProp = backPropagate( up, derv, cx, (int)p0.x, bckProp );
				}
				else if( !up && derv.get(cx)>=0 ) { 
					bckProp += (derv.get(cx)+smallestDerivative)/2;
					fwdProp += (derv.get(cx)+smallestDerivative)/2;
					derv.set(cx, -smallestDerivative);
					bckProp = backPropagate( up, derv, cx, (int)p0.x, bckProp );
				}
				else {
					fwdProp = forwardPropagate(up, derv, cx, cx+1, fwdProp );
				}
			}
			bckProp = forwardPropagate( up, derv, (int)p0.x, (int)p1.x, bckProp );
			fwdProp = backPropagate(    up, derv, (int)p1.x, (int)p0.x, fwdProp );
		}

		SignalIntegral integ = new SignalIntegral( derv, t.get(0) );
		for( float v : integ ) {
			addPoint( v );
		}

	}
	
	private float backPropagate( boolean up, SignalDerivative derv, int cx, int xMin, float propAmnt ) {
		for( int bx = cx-1; bx > (int)xMin && propAmnt != 0; bx-- ) {
			float curV = derv.get(bx);
			float newV;
			if( up )
				newV = Math.max(smallestDerivative, curV+propAmnt );
			else
				newV = Math.min(-smallestDerivative, curV+propAmnt );
			propAmnt += (curV-newV);
			derv.set(bx, newV);
		}
		return propAmnt;
	}
	
	
	
	private float forwardPropagate( boolean up, SignalDerivative derv, int cx, int xMax, float propAmnt ) {
		for( int bx = cx; bx < xMax && propAmnt != 0; bx++ ) {
			float curV = derv.get(bx);
			float newV;
			if( up ) 
				newV = Math.max(smallestDerivative, curV+propAmnt );
			else
				newV = Math.min(-smallestDerivative, curV+propAmnt );
			propAmnt += (curV-newV);
			derv.set(bx, newV);
		}
		return propAmnt;
	}
	
	

	@Override public String graphType( ) {
		return filterType();
	}
	
	public static String filterType( ) {
		return "TopoLines"; 
	}


	public class Point implements TopoGraph.Vertex {
		int idx;
		int rmin, rmax;
		public Point( int _idx, int pnt ) { idx = _idx; rmin=rmax=pnt; }
		public void expand( int pnt ) { rmax = Math.max(rmax, pnt); }
		public float position() { return (float)(rmax+rmin)/2; }
		@Override public float value() { return orig_graph.getPoint(rmin); }
		@Override public int getID() { return idx; }
		@Override public Vertex[] neighbors() {
			if ( idx == 0 ) return new Vertex[]{topo.get(idx+1)};
			if ( idx == topo.size()-1 ) return new Vertex[]{topo.get(idx-1)};
			return new Vertex[]{topo.get(idx-1), topo.get(idx+1)};
		}
	}
}


