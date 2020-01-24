package usf.dvl.signal;

import java.io.IOException;

import usf.dvl.topology.distance.HeraTopologicalDistance;
import usf.dvl.topology.distance.TopologicalDistance;
import usf.dvl.topology.ph.PersistenceDiagram;
import usf.dvl.topology.ph.PersistenceFeature;
import usf.saav.topology.TopoGraph;
import usf.saav.topology.TopoGraph.Vertex;
import usf.saav.topology.merge.AbstractMergeTreeNode;
import usf.saav.topology.merge.serial.JoinTree;

public class SignalMergeTree extends PersistenceDiagram<PersistenceFeature> {

	public static TopologicalDistance topo_dist;
	static {
		try {
			topo_dist = new HeraTopologicalDistance();
			//topo_dist.setVerbose(true);
		}
		catch( IOException e ) {
			e.printStackTrace();
		}
	}
	
	private TopoGraph<Point> topo = new TopoGraph<Point>();
	private JoinTree tt;
	private Signal orig_graph;
	
	public SignalMergeTree( Signal t ){
		orig_graph = t;
		
		
		topo.add( new Point(0,0) );
		for( int i = 1; i < t.size(); i++) {
			if( topo.get(topo.size()-1).value() == t.getPoint(i) ) 
				topo.get(topo.size()-1).expand(i);
			else
				topo.add( new Point(topo.size(),i) );
		}

		tt = new JoinTree(topo);
		tt.run();
		
		for( int i = 0; i < tt.size(); i++ ) {
			AbstractMergeTreeNode n = tt.getNode(i);
			AbstractMergeTreeNode p = tt.getNode(i).getPartner();
			if( p == null || n.getValue() < p.getValue() )
				this.add( new PersistenceFeature(0, tt.getBirth(i), tt.getDeath(i) ) );
		}

	}
	
	public static double BottleneckDistance( SignalMergeTree p0, SignalMergeTree p1 ) {
		return topo_dist.bottleneckDistance( p0, p1, 0 );
	}
	public static double WassersteinDistance( SignalMergeTree p0, SignalMergeTree p1 ) {
		return topo_dist.wassersteinDistance( p0, p1 );
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
			if( idx == 0 && topo.size() == 1 ) return new Vertex[] {};
			if ( idx == 0 ) return new Vertex[]{topo.get(idx+1)};
			if ( idx == topo.size()-1 ) return new Vertex[]{topo.get(idx-1)};
			return new Vertex[]{topo.get(idx-1), topo.get(idx+1)};
		}
	}
	
	
}
