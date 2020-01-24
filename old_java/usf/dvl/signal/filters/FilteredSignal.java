package usf.dvl.signal.filters;

import processing.core.PApplet;
import processing.data.JSONArray;
import usf.dvl.signal.Measures;
import usf.dvl.signal.Signal;
import usf.dvl.signal.SignalFFT;
import usf.dvl.signal.SignalMergeTree;

public abstract class FilteredSignal extends Signal {


	protected Signal orig_graph;
	protected float simpl_level; 
	
	private CachedFloat l1norm = new CachedFloat() {
		@Override protected float compute() { return (float) Measures.L1Norm( orig_graph, FilteredSignal.this ); }
	};
	private CachedFloat l2norm = new CachedFloat() {
		@Override protected float compute() { return (float) Measures.L2Norm( orig_graph, FilteredSignal.this ); }
	};
	private CachedFloat linfnorm = new CachedFloat() {
		@Override protected float compute() { return (float) Measures.LInfNorm( orig_graph, FilteredSignal.this ); }
	};
	private CachedFloat dvol = new CachedFloat() {
		@Override protected float compute() { return (float) Measures.deltaVolume( orig_graph, FilteredSignal.this ); }
	};
	
	private float peakinessbottleneck = Float.NaN;
	private float peakinesswasserstein = Float.NaN;
	private float frequencypreservation = Float.NaN;

	protected FilteredSignal( Signal _orig_graph, float _simpl_level ) {
		orig_graph = _orig_graph;
		simpl_level = _simpl_level;
	}

	public float getSimplificationLevel() { return simpl_level; }

	
	public JSONArray signalJSON( ) {
		JSONArray ret = new JSONArray();
		for( int i = 0; i < size(); i++ ) {
			ret.append( this.getPoint( i ) );
		}
		return ret;
	}


	public float L1Norm( ){ return l1norm.getValue(); }
	public float L2Norm( ){ return l2norm.getValue(); }
	public float LInfNorm( ){ return linfnorm.getValue(); }
	public float deltaVolume( ) { return dvol.getValue(); }

	
	public float peakinessBottleneck( ) {
		if( Float.isNaN(peakinessbottleneck) ) {
			SignalMergeTree m0 = new SignalMergeTree( this );
			SignalMergeTree m1 = new SignalMergeTree( orig_graph );
			peakinessbottleneck = (float)SignalMergeTree.BottleneckDistance(m1, m0);
		}
		return peakinessbottleneck;
	}

	public float peakinessWasserstein( ) {
		if( Float.isNaN(peakinesswasserstein) ) {
			SignalMergeTree m0 = new SignalMergeTree( this );
			SignalMergeTree m1 = new SignalMergeTree( orig_graph );
			if( m0.size() <= 1 ) 
				peakinesswasserstein = Float.POSITIVE_INFINITY;
			else
				peakinesswasserstein = (float)SignalMergeTree.WassersteinDistance(m1, m0);
		}
		return peakinesswasserstein;
	}

	// Calculate the L2norm of frequency domain
	public float frequencyPreservation( ) {
		if( Float.isNaN(frequencypreservation) ) {
			SignalFFT p0 = new SignalFFT( this );
			SignalFFT p1 = new SignalFFT( orig_graph );
			float sum = 0;

			int i = 0;
			for(; i < p0.size() && i < p1.size(); i++ ){
				sum += PApplet.sq( p0.get(i) - p1.get(i) );
			}
			for(; i < p0.size(); i++ ){
				sum += PApplet.sq( p0.get(i) );
			}
			for(; i < p1.size(); i++ ){
				sum += PApplet.sq( p1.get(i) );
			}
			frequencypreservation = PApplet.sqrt(sum);
		}
		return frequencypreservation;
	}
	
	public float phaseShifted( FilteredSignal phi ) {
		float tot = 0;
		for( int i = 0; i < size()-1 && i < phi.size(); i++ ) {
			float o = phi.orig_graph.get(i) - phi.get(i);
			float f = orig_graph.get(i+1) - get(i+1);
			tot += Math.pow(o-f,2);
		}
		return (float) Math.sqrt(tot);
	}
	
	public float signalToNoise( ) {
		Signal noise = new Signal();
		for( int i = 0; i < size(); i++) {
			noise.addPoint( orig_graph.get(i) - get(i) );
		}
		return (float)( Measures.getVariance(this) / Measures.getVariance(noise) );
	}
}
